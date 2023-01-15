import argparse
import requests
import json
import re
from celery.result import AsyncResult
from celery import Celery

art = '''
                   _
  __ _ _ __  _   _| | __ _
 / _` | '_ \| | | | |/ _` |
| (_| | | | | |_| | | (_| |
 \__, |_| |_|\__,_|_|\__,_|
 |___/

 ___  ___ _ __ __ _ _ __   ___ _ __
/ __|/ __| '__/ _` | '_ \ / _ \ '__|
\__ \ (__| | | (_| | |_) |  __/ |
|___/\___|_|  \__,_| .__/ \___|_|
                   |_|


https://linktr.ee/albertodiazz

'''
print(art)

# Unicode icone
checkIcon = u'\u2705'
error = u'\u274C'
moviesIcon = '🍿'
linkIcon = '🔗'
waitIcon = '⌛'

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-s', '--search',
                    metavar='\b',
                    help='Put the name of the movie you want to search')
parser.add_argument('-n', '--num',
                    type=int,
                    metavar='\b',
                    help='Size of result by request')

args = parser.parse_args()

app = Celery('api',
             broker='amqp://127.0.0.1:5672',
             backend='redis://127.0.0.1:6379/0')


def printPretty(getRes):
    '''Funcion para imprimir de forma bonita los nombres y url
       ARGS:
        getRes dict = Es el resultado de nuestra tarea en celery
    '''
    for i in range(len(list(getRes))):
        names = re.findall('[^/]+(?=/$|$)', str(list(getRes)[i]))
        for ns in range(len(names)):
            # print(f'{names[ns]}')
            print(f'{moviesIcon} {names[ns]}')
            try:
                for x in range(len(list(getRes)[i])):
                    links = getRes[list(getRes)[i]][x]
                    # print(f'{links}')
                    print(f'{linkIcon} {links}')
            except IndexError:
                pass


def searchMovies(search: str,
                 num: int):
    try:
        msg = f'{checkIcon} Searching links...'
        print(msg)
        res = requests.get(f'http://localhost/api/movies/{search}/{num}')

        print(f'{waitIcon} {"Wait..."}')
        getcelery = AsyncResult(res.json()['id'], app=app)
        # print(getcelery.get())
        getResult = getcelery.get()
        printPretty(getResult)

    except json.JSONDecodeError:
        msgDontFound = f'{error} Timeout Exceeded try with less results...'
        print(msgDontFound)


# Meter esto como variable de docker
if args.search:
    status = requests.get('http://localhost/api/key/status')
    if re.fullmatch('Es valida', status.json()['body']):
        # Es valida nos sirve para hacer la paticion
        msg = f'{checkIcon} Valid Key'
        print(msg)
        # print(args.num)
        if args.num:
            searchMovies(args.search, int(args.num))
        else:
            searchMovies(args.search, int(5))

    else:
        # La llave no es valida hay que generar una nueva
        key = requests.get('http://localhost/api/key/new')
        if re.fullmatch('Key generada', key.json()['body'][0]):
            msg = f'{checkIcon} Key generate'
            print(msg)
            searchMovies(args.search, int(args.num))
else:
    parser.print_help()
