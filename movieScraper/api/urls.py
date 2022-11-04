from django.urls import path
from .views import MoviesSearch
from .views import statusKey
from .views import getApiKey
from .views import newApiKey
from .views import concurrency

urlpatterns = [
    path('movies/', MoviesSearch.as_view(), name='info-movies'),
    path('movies/<str:search>/<int:numresults>', MoviesSearch.as_view(),
         name='search-movies'),
    path('key/', getApiKey, name='apiKey-gnula'),
    path('key/status', statusKey, name='status-apiKey'),
    path('key/new', newApiKey, name='new-apiKey'),
    path('test/<str:search>/<int:numresults>', concurrency,
         name='search-test'),
]
