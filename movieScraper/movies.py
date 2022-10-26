import argparse
import requests
import re

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

checkIcon = u'\u2705'
error = u'\u274C'
moviesIcon = '🍿'
linkIcon = '🔗'

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-s', '--search',
                    metavar='\b',
                    help='Put the name of the movie you want to search')

args = parser.parse_args()


def searchMovies(search: str):
    msg = f'{checkIcon} Searching links...'
    print(msg)
    res = requests.get(f'http://localhost/api/movies/{search}')
    if len(res.json()[search]) == 0:
        msgDontFound = f'{error} Dont found anything...'
        print(msgDontFound)
    else:
        data = dict(res.json()[search])
        for i in range(len((data.keys()))):
            names = re.findall('[^/]+(?=/$|$)', str(list(data.keys())[i]))
            for ns in range(len(names)):
                print(f'{moviesIcon} {names[ns]}')
            for x in range(len(data[list(data.keys())[i]])):
                links = data[list(data.keys())[i]][x]
                print(f'{linkIcon} {links}')
                # print(data[list(data.keys())[i]][x])


# Meter esto como variable de docker
if args.search:
    status = requests.get('http://localhost/api/key/status')
    if re.fullmatch('Es valida', status.json()['body']):
        # Es valida nos sirve para hacer la paticion
        msg = f'{checkIcon} Key valida'
        print(msg)
        searchMovies(args.search)
    else:
        # La llave no es valida hay que generar una nueva
        key = requests.get('http://localhost/api/key/new')
        if re.fullmatch('Key generada', key.json()['body'][0]):
            msg = f'{checkIcon} Key generate'
            print(msg)
            searchMovies(args.search)
else:
    parser.print_help()
