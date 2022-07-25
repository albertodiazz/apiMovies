from django.shortcuts import render
from django.views import View 
from django.http import HttpResponse
import json

# Create your views here.
class MoviesServices(View):
    '''
    Endpoinst:
        [GET]
            - /<nameMovie>
    '''

    def get(self, request):
        data = {
            'result': 200,
            'body': 'Hola mundo'
        }
        return HttpResponse(json.dumps(data, indent=4), 
                            content_type='application/json')
