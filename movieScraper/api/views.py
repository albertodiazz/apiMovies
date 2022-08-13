from django.shortcuts import render
from django.views import View 
from django.http import HttpResponse
from background_task import background
import subprocess
import re
import json
import logging

# Create your views here.
class MoviesServices(View):
    '''
    Endpoinst:
        [GET]
            - /<nameMovie> : Aqui es donde buscamos la pelicula
    '''

    def get(self, request):
        # TODO: Pendiente
        # [] Meter la opcion de buscar, al buscar debemos setear cuantos resultados
        #    queremos obtener y este solo nos debe regresar los links con url que si tengan videos
        # [] Hay que meter la logica de que si me marca error por falta de apiKey hay que generar una
        #    en automatico
        # TODO: Opcional
        # [] En caso de que no me deje hacer los curl a los links del video es debido al bloqueo
        #    de su servidor hay que ocupar proxychain con sock5 (Tor) para las peticiones 
        data = {
            'result': 200,
            'body': 'Hola mundo'
        }
        return HttpResponse(json.dumps(data, indent=4), 
                            content_type='application/json')

@background(schedule=0)
def getApiKey():
    '''
    Esta tarea se corre en un segungo plano para no paralizar la api
    '''
    # The Programmable Search Engine ID to use for this request.
    cx = "014793692610101313036:vwtjajbclpq"
    # TODO : SECURITY el problema con esto es que me podrian insertar comandos
    curlGet = subprocess.check_output("curl -X GET https://cse.google.es/cse.js\?sa\=G\&hpg\=1\&cx\={}".format(cx), shell=True)
    getKey = re.search('(?<="cse_token": ")[^"]*',str(curlGet))
    res = getKey.group(0)
    print('APIkeyGnula: {}'.format(res), flush = True)


class APIkeyGnula(View):
    '''
    Aqui obtenemos el key de la API de cse.google gnula para buscar
    '''
    def get(self, request):
        # logging.info('solo quiero saber si esto funciona')
        getApiKey.now()
        try:
            data = {
                'result': 200,
                'body': 'Wait a moment...' 
            }
        except TypeError:
            data = {
                'result': 400,
                'body': 'No se pudo obtener el Key del serch de Gnula' 
            }
        return HttpResponse(json.dumps(data, indent=4), 
                            content_type='application/json')
