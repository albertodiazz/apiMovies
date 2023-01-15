from celery import shared_task
import time
import aiohttp
import re
import asyncio
import requests
# TODO:Pendiente
# [] Agregar websocket
# pero en otro proyecto
# from celery import app


# @app.task
@shared_task
def task1(msg: str):
    time.sleep(5)
    return f'task1: {msg}'


async def get_gnula(url, search):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            res = await response.text()
            search = '-'.join(search.split(' '))
            regex = f'(?<="url": ")[^"]*gnula[^"]*{search}[^"]*'
            getUrlMovies = re.findall(regex, str(res))
            names = {}
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
                            names[str(getUrlMovies[i])] = links
                    except IndexError:
                        pass
        # session.close()
    return getUrlMovies, names


# async def get_ruso(url):
#     # startTime = time.time()
#     okRu = []
#     async with aiohttp.ClientSession() as session:
#         for i in range(0, len(url)):
#             async with session.get(url[i]) as response:
#                 res = await response.text()
#                 # print(f'{i} -> {time.time()-startTime}',
#                 #       flush=True)
#                 # TODO: PENDIENTE
#                 # [] El problema es el findall, es muy lento
#                 dt = re.findall('[^"]+ok.ru[^"]+', res)
#                 okRu.append(dt)
#                 # print(f'{i}F -> {time.time()-startTime}',
#                 #       flush=True)
#       return okRu


async def getMoviesUrl(**kwargs):
    urlGnula, names = await get_gnula(
        kwargs['url'],
        kwargs['search'],
    )
    # okRu = await get_ruso(urlGnula)
    # print(f'{kwargs["search"]}: {okRu}')
    return names


@shared_task
def runScrapperGnula(joinUrl, search):
    try:
        curl = requests.get(joinUrl)
        statusKey = re.search('Unauthorized access to internal API', curl.text)
        tr = 'Our systems have detected unusual traffic from your network'
        traffic = re.search(tr, curl.text)
        if traffic:
            raise ValueError('Me bloquearon a nivel servidor')
        if statusKey:
            raise ValueError('API key no es valida')
        else:
            # raise ValueError('API key es valida')
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(getMoviesUrl(url=joinUrl,
                                                        search=search))
    except ValueError as error:
        return error
