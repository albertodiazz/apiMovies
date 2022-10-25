from django.views import View
from django.http import HttpResponse
from .models import Keys
import requests
import re
import json


cx = '014793692610101313036:vwtjajbclpq'
callback = 'google.search.cse.api6737'


# Create your views here.
class MoviesSearch(View):
    '''
    Endpoinst:
        [GET]
            - /<nameMovie> : Aqui es donde buscamos la pelicula
    '''
    def __init__(self):
        self.getKey = getattr(Keys.objects.first(), 'Key')
        self.numpages = 500  # Cantidad de resultados en una sola peticion
        self.actualpage = 0  # Pagina en la cual empezamos a buscar

    def get(self, request, search=None):
        # TODO: Pendiente
        # [x] Meter la opcion de buscar, opncion de cantidad de resultados
        # [x] Hay que manejar el error de cuando no es valida la api
        # [] Hay que comprobar que las url de las peliculas funcionen
        # [] Contemplar la idea de si o no almacenar la info en mongo
        url = [
            'https://cse.google.com/cse/element/v1?',
            f'rsz=filtered_cse&num={self.numpages}&hl=es&source=gcsc&gss=.es',
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
        # Aqui debo levantar una excepcion
        if statusKey:
            res = 'API key no es valida'
        else:
            res = 'API key es valida'

        # TODO: IMPORTANTE
        # [] Hay que ultilizar asyncio y concurrencia para hacelerar esto
        # Aqui buscamos los dominios de las peliculas
        regex = f'(?<="url": ")[^"]*gnula[^"]*{search}[^"]*'
        getUrlMovies = re.findall(regex, curl.text)
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
        # TODO : SECURITY revisar que tan seguro es requests
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
        'body': f'Generando nueva Key {get_res}'
    }
    return HttpResponse(json.dumps(data, indent=4),
                        content_type='application/json')


def statusKey(request):
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
    statusKey = re.search('Unauthorized access to internal API', curlGet.text)

    if statusKey:
        res = 'No es valida'
    else:
        res = 'Es valida'
    data = {
        'result':  200,
        'body': res
    }
    return HttpResponse(json.dumps(data, indent=4),
                        content_type='application/json')
