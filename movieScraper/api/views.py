from django.views import View
from django.http import HttpResponse
from .models import Keys
# from asgiref.sync import async_to_sync
import requests
import re
import json
import time
from .tasks import runScrapperGnula


cx = '014793692610101313036:vwtjajbclpq'
callback = 'google.search.cse.api6737'


def concurrency(request, search, numresults):
    getKey = getattr(Keys.objects.first(), 'Key')
    actualpage = 0  # Pagina en la cual empezamos a buscar
    url = [
        'https://cse.google.com/cse/element/v1?',
        f'rsz=filtered_cse&num={numresults}&hl=es&source=gcsc&gss=.es',
        f'&start={actualpage}&cselibv=3e1664f444e6eb06',
        f'&cx={cx}',
        f'&q={search}&safe=off',
        f'&cse_tok={getKey}',
        '&exp=csqr,cc&rsToken=undefined&afsExperimentId=undefined',
        f'&callback={callback}'
    ]
    startTime = time.time()
    joinUrl = ''.join(url)

    runScrapperGnula.delay(joinUrl, search)

    data = {
        'time': f'{time.time()-startTime}',
        'res': f'{201}',
    }

    return HttpResponse(json.dumps(data, indent=4),
                        content_type='application/json')


# Create your views here.
class MoviesSearch(View):
    '''
    Endpoinst:
        [GET]
            - /<nameMovie> : Aqui es donde buscamos la pelicula
    '''
    def __init__(self):
        self.getKey = getattr(Keys.objects.first(), 'Key')
        # self.numpages = 500  # Cantidad de resultados en una sola peticion
        self.actualpage = 0  # Pagina en la cual empezamos a buscar

    def get(self, request, search, numresults):
        url = [
            'https://cse.google.com/cse/element/v1?',
            f'rsz=filtered_cse&num={numresults}&hl=es&source=gcsc&gss=.es',
            f'&start={self.actualpage}&cselibv=3e1664f444e6eb06',
            f'&cx={cx}',
            f'&q={search}&safe=off',
            f'&cse_tok={self.getKey}',
            '&exp=csqr,cc&rsToken=undefined&afsExperimentId=undefined',
            f'&callback={callback}'
        ]
        joinUrl = ''.join(url)
        curl = requests.get(joinUrl)

        statusKey = re.search('Unauthorized access to internal API', curl.text)
        # Esto ocurre cuando google detecta trafico raro
        # TODO: TEST
        # [] Hay ver si esto funciona
        tr = 'Our systems have detected unusual traffic from your network'
        traffic = re.search(tr, curl.text)
        if traffic:
            res = 'Me bloquearon a nivel servidor'
        # Aqui debo levantar una excepcion
        if statusKey:
            res = 'API key no es valida'
        else:
            res = 'API key es valida'

        # Aqui buscamos los dominios de las peliculas
        # TODO: IMPORTANTE
        # Es para que lo busque ya que gnula contruye sun likns asi hola-mundo
        search = '-'.join(search.split(' '))
        regex = f'(?<="url": ")[^"]*gnula[^"]*{search}[^"]*'
        # print(regex, flush=True)
        getUrlMovies = re.findall(regex, curl.text)
        # print(getUrlMovies, flush=True)
        data, movies = {}, {}
        for i in range(len(getUrlMovies)):
            resd = requests.get(str(getUrlMovies[i]))
            # Aqui buscamos el servidor ruso de peliculas
            dt = re.findall('[^"]*ok.ru[^"]*', resd.text)
            links = []
            for urlM in range(len(dt)):
                # Aqui comprobamos la disponibilidad del link
                try:
                    resd = requests.get(dt[urlM])
                    exclude = re.findall('vp_video_stub_txt', resd.text)
                    if exclude:
                        pass
                    else:
                        links.append(str(dt[urlM]))
                        data[str(getUrlMovies[i])] = links
                except IndexError:
                    pass

        movies[search] = data

        data = {
            'result': 200,
            'body': '...{}'.format(res),
            'url': 'Get list movie...{}'.format(movies)
        }
        return HttpResponse(json.dumps(movies, indent=4),
                            content_type='application/json')


def getApiKey(request):
    '''
    Aqui generamos la api key
    '''
    existeLaKey = True if len(Keys.objects.all()) > 0 else False
    if existeLaKey:
        # Existe la Key en la base de datos
        getKey = getattr(Keys.objects.first(), 'Key')
        # request.GET()
        data = {
            'result': 200,
            'body': 'This is the Key: {}'.format(getKey)
        }
    else:
        # No existe la Key en la base de datos
        # The Programmable Search Engine ID to use for this request.
        data = {
            'result': 200,
            'body': 'No existe la Api Key en la base de datos key/new'
        }
    return HttpResponse(json.dumps(data, indent=4),
                        content_type='application/json')


def newApiKey(request):
    '''
    Aqui generamos la api key
    '''
    # No existe la Key en la base de datos
    # The Programmable Search Engine ID to use for this request.
    # TODO : SECURITY revisar que tan seguro es requests
    existeLaKey = True if len(Keys.objects.all()) > 0 else False
    curl = f"https://cse.google.es/cse.js?sa=G&hpg=1&cx={cx}"
    curlGet = requests.get(curl)
    # print(curlGet, flush=True)
    getKey = re.search('(?<="cse_token": ")[^"]*', curlGet.text)
    res = getKey.group(0)
    if existeLaKey:
        # Si existe la llave la borramos para que solo exista una
        # con el nombre de Gnula
        Keys.objects.filter(Title='Gnula').delete()
    get_res = res
    key = Keys(Title='Gnula', Key=get_res)
    key.save()
    data = {
        'result': 200,
        'body': ['Key generada', get_res]
    }
    return HttpResponse(json.dumps(data, indent=4),
                        content_type='application/json')


def statusKey(request):
    try:
        getKey = getattr(Keys.objects.first(), 'Key')
        url = [
            'https://cse.google.com/cse/element/v1?',
            'rsz=filtered_cse&num=1&hl=es&source=gcsc&gss=.es',
            '&start=40&cselibv=3e1664f444e6eb06',
            f'&cx={cx}',
            '&q=avenger&safe=off',
            f'&cse_tok={getKey}',
            '&exp=csqr,cc&rsToken=undefined&afsExperimentId=undefined',
            f'&callback={callback}'
        ]
        joinUrl = ''.join(url)

        curlGet = requests.get(joinUrl)
        statusKey = re.search('Unauthorized access to internal API',
                              curlGet.text)

        if statusKey:
            res = 'No es valida'
        else:
            res = 'Es valida'
        data = {
            'result':  200,
            'body': res
        }
    except AttributeError:
        data = {
            'result': 200,
            'body': 'No existe la Key'
        }
    return HttpResponse(json.dumps(data, indent=4),
                        content_type='application/json')
