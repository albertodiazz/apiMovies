import time
import concurrent
import asyncio
import requests
import aiohttp


# Esto tarda 3 segundos
async def pokemonGetData():
    data, res = [], []
    async with aiohttp.ClientSession() as session:
        for i in range(1, 50):
            url = f'https://pokeapi.co/api/v2/pokemon/{i}'
            async with session.get(url) as response:
                data = await response.json()
                res.append(data['species']['name'])
    print(res)
    return res


# Esto tarda de 15 a 20 segundos
def pokemonGetDataSync():
    data = []
    for i in range(1, 50):
        url = f'https://pokeapi.co/api/v2/pokemon/{i}'
        res = requests.get(url)
        data.append(res.json()['species']['name'])
    return data


# TODO: PENDIENTE
# [] Hacer esta prueba de velocidad on Go
async def main():
    '''Con la libreria de aiohttp no tendria que hacer esto,
    es similar pero tiene su manera de hacer las cosas'''
    startTime = time.time()
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=60) as pool:
        futures = [
            await loop.run_in_executor(pool, pokemonGetData)
            # await loop.run_in_executor(pool, pokemonGetDataSync)
        ]
        results = await asyncio.gather(*futures, return_exceptions=False)
        print(results)
        endTime = time.time() - startTime
        print(endTime)


async def newWayThread():
    futures = []
    futures.append(asyncio.ensure_future(pokemonGetData()))
    results = await asyncio.gather(*futures, return_exceptions=False)
    print(results)

if __name__ == '__main__':
    # asyncio.run(main())
    startTime = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pokemonGetData())
    # newWayThread()
    endTime = time.time() - startTime
    print(endTime)
