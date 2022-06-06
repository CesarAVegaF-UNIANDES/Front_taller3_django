from genericpath import exists
from django.shortcuts import render
import pandas as pd
import dataframe_image as dfi
import os

from app.main import *

def getMovieDataRequest(request):
    movie = getMovieDataApp(request.GET["title"])
    print(movie)
    return render(request, '../templates/recomendaciones.html')

def getMovieData(title):
    movie = getMovieDataApp(title)
    print(movie)
    return movie

def getMovieGenresRequest(request):
    genres = getMovieGenresApp(request.GET["title"])
    print(genres)
    return render(request, '../templates/recomendaciones.html')

def getMovieGenres(title):
    genres = getMovieGenresApp(title)
    print(genres)
    return genres

def getMovieRatingsRequest(request):
    ratings = getMovieRatingsApp(request.GET["title"])
    print(ratings)
    return render(request, '../templates/recomendaciones.html')

def getMovieRatings(title):
    ratings = getMovieRatingsApp(title)
    print(ratings)
    return ratings

def getMovieTagsRequest(request):
    tags = getMovieTagsApp(request.GET["title"])
    print(tags)
    return render(request, '../templates/recomendaciones.html')

def getMovieTags(title):
    tags = getMovieTagsApp(title)
    print(tags)
    return tags

def getMoviesByYearRequest(request):
    movies = getMoviesByYearApp(request.GET["year"])
    print(movies)
    return render(request, '../templates/recomendaciones.html')

def getMoviesByYear(year):
    movies = getMoviesByYearApp(year)
    print(movies)
    return movies

def getMovieAverageRatingRequest(request):
    avg = getMovieAverageRatingApp(request.GET["title"])
    print(avg)
    return render(request, '../templates/recomendaciones.html')

def getMovieAverageRating(title):
    avg = getMovieAverageRatingApp(title)
    print(avg)
    return avg

def getMovieTopNRequest(request):
    mvs = getMovieTopNApp(request.GET["n"])
    print(mvs)
    return render(request, '../templates/recomendaciones.html')

def getMovieTopN(n = "10"):
    mvs = getMovieTopNApp(n)
    print(mvs)
    return mvs

def getMovieNMostRatedRequest(request):
    mvs = getMovieNMostRatedApp(request.GET["n"])
    print(mvs)
    return render(request, '../templates/recomendaciones.html')

def getMovieNMostRated(n = "10"):
    mvs = getMovieNMostRatedApp(n)
    print(mvs)
    return mvs

def getUserRatingsRequest(request):
    ratings = getUserRatingsApp(request.GET["user_id"]) 
    print(ratings)
    return render(request, '../templates/recomendaciones.html')

def getUserRatings(userIDGlobal):
    ratings = getUserRatingsApp(userIDGlobal) 
    print(ratings)
    return ratings

def getUserTagsRequest(request):
    tags = getUserTagsApp(request.GET["user_id"])
    print(tags)
    return render(request, '../templates/recomendaciones.html')

def getUserTags(user_id):
    tags = getUserTagsApp(user_id)
    print(tags)
    return tags

def getUserAverageRatingRequest(request):
    avg = getUserAverageRatingApp(request.GET["user_id"])
    print(avg)
    return render(request, '../templates/recomendaciones.html')

def getUserAverageRating(user_id):
    avg = getUserAverageRatingApp(user_id)
    print(avg)
    return avg

def getRecContentRequest(request):
    avg = getRecContentApp(request.GET["title"], request.GET["n"])
    print(avg)
    return render(request, '../templates/recomendaciones.html')

def getRecContent(title, n = "10"):
    avg = getRecContentApp(title, n)
    print(avg)
    return avg

def getRecCollabRequest(request):
    rec = getRecCollabApp(request.GET["user_id"], request.GET["n"])
    print(rec)
    return render(request, '../templates/recomendaciones.html')

def getRecCollab(user_id, n = "10"):
    rec = getRecCollabApp(user_id, n)
    print(rec)
    return rec

def getRecCollabGenderRequest(request):
    rec = getRecCollabGenderApp(request.GET["user_id"], request.GET["n"])
    print(rec)
    return render(request, '../templates/recomendaciones.html')
                    
def getRecCollabGender(user_id, n = "10"):
    rec = getRecCollabGenderApp(user_id, n)
    print(rec)
    return rec

def loginView(request):
    return render(request, '../templates/recomendaciones.html')

def recomendacionesView(request):
    if os.path.exists("static/img/movieTopN.png"):
        os.remove("static/img/movieTopN.png")

    if os.path.exists("static/img/movieNMostRated.png"):
        os.remove("static/img/movieNMostRated.png")

    if os.path.exists("static/img/recContent.png"):
        os.remove("static/img/recContent.png")

    userIDGlobal = request.GET["user_id"] 
    titleGlobal = request.GET["title"]
    nGlobal = request.GET["n"]

    if( nGlobal == ""):
        nGlobal = "10"

    print("[", userIDGlobal, titleGlobal, nGlobal,"]")

    movieTopN = ""
    movieNMostRated = ""
    recContent = ""
    recCollab = ""
    recCollabGender = ""

    if (nGlobal != ""):
        movieTopN = getMovieTopN(nGlobal)
        movieNMostRated = getMovieNMostRated(nGlobal)

        if (userIDGlobal != "" or titleGlobal != ""):
            recCollab = getRecCollab(userIDGlobal, nGlobal)
            recCollabGender = getRecCollabGender(userIDGlobal, nGlobal)
            recContent = getRecContent(titleGlobal, nGlobal)

            movies = []
            genres = []
            numberOfSharedGenres = []
            for i in recContent:
                movie = i['title']
                genre = i['genres']
                numberOfSharedGenre = i['numberOfSharedGenres']
                if movie not in movies: 
                    movies.append(movie)
                    genres.append(genre)
                    numberOfSharedGenres.append(numberOfSharedGenre)
                    
            recs_imp = pd.DataFrame({'movies': movies, 'genres': genres, 'numberOfSharedGenres': numberOfSharedGenres})

            dfi.export(recs_imp, 'static/img/recContent.png')

            return render(request, '../templates/recomendaciones.html', {"recCollab": recCollab, "recCollabGender": recCollabGender}) 

        if (userIDGlobal != ""):
            recCollab = getRecCollab(userIDGlobal, nGlobal)
            recCollabGender = getRecCollabGender(userIDGlobal, nGlobal)
            return render(request, '../templates/recomendaciones.html', {"recCollab": recCollab, "recCollabGender": recCollabGender}) 

        if (titleGlobal != ""):
            recContent = getRecContent(titleGlobal, nGlobal)
            return render(request, '../templates/recomendaciones.html', {"recContent": recContent}) 

        if (userIDGlobal == "" or titleGlobal == ""):
            movies = []
            ratings = []
            for i in movieTopN:
                movie = i['title']
                nomRating = i['averageRating']
                if movie not in movies: 
                    movies.append(movie)
                    ratings.append(round(float(nomRating), 2))
                    
            recs_imp = pd.DataFrame({'movies': movies,'ratings': ratings})

            dfi.export(recs_imp, 'static/img/movieTopN.png')

            movies = []
            ratings = []
            for i in movieNMostRated:
                movie = i['title']
                nomRating = i['NumberOfRatings']
                if movie not in movies: 
                    movies.append(movie)
                    ratings.append(round(float(nomRating), 2))
                    
            recs_imp = pd.DataFrame({'movies': movies,'ratings': ratings})

            dfi.export(recs_imp, 'static/img/movieNMostRated.png')

            return render(request, '../templates/recomendaciones.html') 

    else:
        return render(request, '../templates/recomendaciones.html') 

def moviesView(request):
    if os.path.exists("static/img/movieGeneres.png"):
        os.remove("static/img/movieGeneres.png")

    if os.path.exists("static/img/movieRatings.png"):
        os.remove("static/img/movieRatings.png")

    if os.path.exists("static/img/movieYearRatings.png"):
        os.remove("static/img/movieYearRatings.png")

    titleGlobal = request.GET["title"]
    yearGlobal = request.GET["year"]

    print("[", titleGlobal, yearGlobal,"]")

    movieData = ""
    movieGenres = ""
    movieRatings = ""
    movieTags = ""
    movieAverageRating = ""
    moviesByYear = ""

    if (titleGlobal != ""):
        movieData = getMovieData(titleGlobal)
        movieGenres = getMovieGenres(titleGlobal)
        movieRatings = getMovieRatings(titleGlobal)
        movieTags = getMovieTags(titleGlobal)
        movieAverageRating = getMovieAverageRating(titleGlobal)[0]

        generes = []
        for i in movieGenres:
            movie = i.values() 
            print(i.values())
            if movie not in generes:
                generes.append(movie)

        recs_imp = pd.DataFrame({'genere': generes})

        dfi.export(recs_imp, 'static/img/movieGeneres.png')

        users = []
        ratings = []
        for i in movieRatings:
            user = i['user']
            rating = i['rating']
            if user not in users:
                users.append(user)
                ratings.append(rating)

        recs_imp = pd.DataFrame({'users': users,'ratings': ratings})

        dfi.export(recs_imp, 'static/img/movieRatings.png')

        return render(request, '../templates/movies.html', {"movieData": movieData, "movieGenres": generes, "movieTags": movieTags, "movieAverageRating": round(movieAverageRating['averageRating'], 2)}) 
    
    if (yearGlobal != ""):
        moviesByYear = getMoviesByYear(yearGlobal)
        movies = []
        ratings = []
        for i in moviesByYear:
            movie = i['title']
            movieAverageRating = getMovieAverageRating(movie)
            if movie not in movies and movieAverageRating: 
                movieAverageRating = movieAverageRating[0]
                movies.append(movie)
                ratings.append(round(movieAverageRating['averageRating'], 2))
                
        recs_imp = pd.DataFrame({'movies': movies,'ratings': ratings})

        dfi.export(recs_imp, 'static/img/movieYearRatings.png')

        return render(request, '../templates/movies.html') 

    else:
        return render(request, '../templates/movies.html') 

def userView(request):
    if os.path.exists("static/img/userRatings.png"):
        os.remove("static/img/userRatings.png")

    userIDGlobal = request.GET["user_id"]

    print("[", userIDGlobal, "]")

    userRatings = ""
    userTags = ""
    userAverageRating = ""

    if (userIDGlobal != ""):
        userRatings = getUserRatings(userIDGlobal)
        userTags = getUserTags(userIDGlobal)
        userAverageRating = getUserAverageRating(userIDGlobal)
        try:        
            movies = []
            ratings = []
            for i in userRatings:
                movie = i['movie']
                rating = round(float(i['rating']),2)
                if movie not in movies:
                    movies.append(movie)
                    ratings.append(rating)

            recs_imp = pd.DataFrame({'movies': movies,
                                'ratings': ratings})

            dfi.export(recs_imp, 'static/img/userRatings.png')

            return render(request, '../templates/user.html', {"userTags": userTags, "userAverageRating": round(float(userAverageRating[0]['averageRating']), 2)}) 
        except:
            return render(request, '../templates/user.html') 
    else:
        return render(request, '../templates/user.html') 