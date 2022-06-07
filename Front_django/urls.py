"""Front_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Front_django.view import *

urlpatterns = [
    path('', loginView), 
    path('recomendaciones/', recomendacionesView),
    path('recomendacionesN/', recomendacionesNView),
    path('recomendacionesUser/', recomendacionesUserView),
    path('recomendacionesMovie/', recomendacionesMovieView),
    path('movies/', moviesView),
    path('moviesTitle/', moviesTitleView),
    path('moviesAnio/', moviesAnioView), 
    path('user/', userView),
    # path('movie_details/', getMovieDataRequest),
    # path('movie_genres/', getMovieGenresRequest),
    # path('movie_ratings/', getMovieRatingsRequest),
    # path('movie_tags/', getMovieTagsRequest),
    # path('movie_year/', getMoviesByYearRequest),
    # path('movie_average_rating/', getMovieAverageRatingRequest),
    # path('top/movie_top_n/', getMovieTopNRequest),
    # path('top/movie_n_most_rated/', getMovieNMostRatedRequest),
    # path('user_ratings/', getUserRatingsRequest),
    # path('user_tags/', getUserTagsRequest),
    # path('user_average_rating/', getUserAverageRatingRequest),
    # path('rec_engine_content/', getRecContentRequest),
    # path('rec_engine_collab/', getRecCollabRequest)
]

