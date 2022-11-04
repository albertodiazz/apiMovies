from celery import shared_task
import time
import aiohttp
import re
import asyncio
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
        # session.close()
    return getUrlMovies


async def get_ruso(url):
    startTime = time.time()
    okRu = []
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(url)):
            async with session.get(url[i]) as response:
                res = await response.text()
                print(f'{i} -> {time.time()-startTime}',
                      flush=True)
                # TODO: PENDIENTE
                # [] El problema es el findall, es muy lento
                dt = re.findall('[^"]+ok.ru[^"]+', res)
                okRu.append(dt)
                print(f'{i}F -> {time.time()-startTime}',
                      flush=True)
    return okRu


async def getMoviesUrl(**kwargs):
    urlGnula = await get_gnula(
        kwargs['url'],
        kwargs['search'],
    )
    okRu = await get_ruso(urlGnula)
    print(f'{kwargs["search"]}: {okRu}')
    return okRu


@shared_task
def runScrapperGnula(joinUrl, search):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getMoviesUrl(url=joinUrl,
                                         search=search))
