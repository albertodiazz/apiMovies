from django.urls import path
from .views import MoviesServices

urlpatterns = [
	path('movies/', MoviesServices.as_view(), name='get-info-movies'),
    # path('boletas/<str:statusPayment>/<str:servicesType>', PaymentServices.as_view(), name='get_boletas_statusPayment'),
    # path('postform/', postform, name='form'),
]
