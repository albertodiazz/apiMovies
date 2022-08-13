from django.urls import path
from .views import MoviesServices
from .views import APIkeyGnula 

urlpatterns = [
	path('movies/', MoviesServices.as_view(), name='get-info-movies'),
	path('cseKeyGnula/', APIkeyGnula.as_view(), name='get-apiKey-gnula-cse'),
    # path('boletas/<str:statusPayment>/<str:servicesType>', PaymentServices.as_view(), name='get_boletas_statusPayment'),
    # path('postform/', postform, name='form'),
]
