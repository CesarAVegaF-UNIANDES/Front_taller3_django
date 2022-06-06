
import csv
from neo4j import GraphDatabase
from psutil import users
from py2neo import Graph, Node
from tqdm import tqdm

N_MOVIES = 2000
N_RATINGS = 280000
N_TAGS = 13000
N_LINKS = 2000

# Online
uri = "neo4j+s://608fe23b.databases.neo4j.io"
user = "neo4j"
password = "hmIjUUeSo9q9N_OhaHUJSe9CdK0WEYSGgrnZTX3VoK0"

# Online
# uri = "bolt://localhost:7687"
# user = "neo4j"
# password = "taller3"

graph = Graph(uri, auth=(user, password))

# Todos los datos
path = "G:\\Mi unidad\\ESTUDIO\\UNIANDES\\SISTEMAS DE RECOMENDACION\\SR\\Talleres\\Taller3\\app\\dataset\\ml-latest\\"

# Pequeño
# path = "G:\\Mi unidad\\ESTUDIO\\UNIANDES\\SISTEMAS DE RECOMENDACION\\SR\\Talleres\\Taller3\\app\\dataset\\ml-latest-small\\"
ratings_file = path+'ratings.csv'
movies_file = path+'movies.csv'
tags_file = path+'tags.csv'
links_file = path+'links.csv'


def main():

    # createGenreNodes()

    print("Cargando peliculas")
    # loadMovies()

    print("Cargando relacion de calificaciones de usuarios y peliculas")
    loadRatings()

    print("Cargando los tags de usuarios")
    loadTags()

    print("actualizando informacion de links de peliculas")
    loadLinks()


def createGenreNodes():
    allGenres = ["Action", "Adventure", "Animation", "Children's", "Children", "Comedy", "Crime",
                 "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "IMAX", "Musical",
                 "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"]

    for genre in allGenres:
        gen = Node("Genre", name=genre)
        graph.create(gen)


def loadMovies():
    graph.run("CREATE CONSTRAINT ON (a:Movie) ASSERT a.movieId IS UNIQUE; ")
    graph.run("CREATE CONSTRAINT ON (a:Genre) ASSERT a.genre IS UNIQUE; ")
    with open(movies_file, encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)  # skip header
        i = 0
        for row in tqdm(readCSV):
            createMovieNodes(row)
            createGenreMovieRelationships(row)

            if i >= N_MOVIES:
                break

            i += 1

def createMovieNodes(row):
    movieData = parseRowMovie(row)
    id = movieData[0]
    title = movieData[1]
    year = movieData[2]
    mov = Node("Movie", id=id, title=title, year=year)
    graph.create(mov)


def parseRowMovie(row):
    id = row[0]
    year = row[1][-5:-1]
    title = row[1][:-7]

    return (id, title, year)


def createGenreMovieRelationships(row):
    movieId = row[0]
    movieGenres = row[2].split("|")

    for movieGenre in movieGenres:
        graph.run(
            'MATCH (g:Genre {name: $genre}), (m:Movie {id: $movieId}) CREATE (g)-[:HAS_GENRE]->(m)',
                  genre=movieGenre, movieId=movieId)


def parseRowGenreMovieRelationships(row):
    movieId = row[0]
    movieGenres = row[2].split("|")

    return (movieId, movieGenres)


def loadRatings():
    with open(ratings_file, encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)  # skip header
        i = 0
        for row in tqdm(readCSV):
            createUserNodes(row)
            createRatingRelationship(row)

            if (i >= N_RATINGS):
                break
            
            i += 1

def createUserNodes(row):
    user = Node("User", id=row[0], name="User " + row[0])
    graph.create(user)


def createRatingRelationship(row):
    ratingData = parseRowRatingRelationships(row)
    graph.run(
        'MATCH (u:User {id: $userId}), (m:Movie {id: $movieId}) CREATE (u)-[:RATED {rating: $rating, timestamp: $timestamp}]->(m)',
        userId=ratingData[0], movieId=ratingData[1], rating=ratingData[2], timestamp=ratingData[3])


def parseRowRatingRelationships(row):
    userId = row[0]
    movieId = row[1]
    rating = row[2]
    timestamp = row[3]

    return (userId, movieId, rating, timestamp)


def loadTags():
    with open(tags_file, encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)  # skip header
        i = 0
        for row in tqdm(readCSV):
            createTagRelationship(row)

            if (i >= N_TAGS):
                break

            i += 1


def createTagRelationship(row):
    tagData = parseRowTagRelationships(row)

    graph.run(
        'MATCH (u:User {id: $userId}), (m:Movie {id: $movieId}) CREATE (u)-[:TAGGED {tag: $tag, timestamp: $timestamp}]->(m)',
        userId=tagData[0], movieId=tagData[1], tag=tagData[2], timestamp=tagData[3])


def parseRowTagRelationships(row):
    # userId = "User " + row[0]
    userId = row[0]
    movieId = row[1]
    tag = row[2]
    timestamp = row[3]

    return (userId, movieId, tag, timestamp)


def loadLinks():
    with open(links_file, encoding="utf-8") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV, None)  # skip header
        i = 0
        for row in tqdm(readCSV):
            updateMovieNodeWithLinks(row)

            if i >= N_LINKS:
                break

            i += 1


def updateMovieNodeWithLinks(row):
    linkData = parseRowLinks(row)

    graph.run(
        'MATCH (m:Movie {id: $movieId}) SET m += {imdbId: $imdbId, tmdbId: $tmdbId}',
        movieId=linkData[0], imdbId=linkData[1], tmdbId=linkData[2])


def parseRowLinks(row):
    movieId = row[0]
    imdbId = row[1]
    tmdbId = row[2]

    return (movieId, imdbId, tmdbId)


if __name__ == '__main__':
    main()
