from py2neo import Graph, Node, NodeMatcher

# Online
uri = "neo4j+s://608fe23b.databases.neo4j.io"
user = "neo4j"
password = "hmIjUUeSo9q9N_OhaHUJSe9CdK0WEYSGgrnZTX3VoK0"

# Online
# uri = "bolt://localhost:7687"
# user = "neo4j"
# password = "taller3"

#print("Graph")
graph = Graph(uri, auth=(user, password))
#print("Cargado")

# Detalles de una pelicula
def getMovieDataApp(title):
    matcher = NodeMatcher(graph)
    movie = matcher.match("Movie", title={title}).first()
    return movie

# Generos de una pelicula
def getMovieGenresApp(title):
    genres = graph.run('MATCH (genres)-[:HAS_GENRE]->(m:Movie {title: $title}) RETURN genres.name', title=title)
    return list(genres)

# calificaciones de una pelicula
def getMovieRatingsApp(title):
    ratings = graph.run(
        'MATCH (u: User)-[r:RATED]->(m:Movie {title: $title}) RETURN u.id AS user, r.rating AS rating', title = title)
    return ratings.data()

# tags de una pelicula
def getMovieTagsApp(title):
    tags = graph.run(
        'MATCH (u: User)-[t:TAGGED]->(m:Movie {title: $title}) RETURN u.id AS user, t.tag AS tag', title = title)
    return list(tags)

# peliculas de un año en especifico
def getMoviesByYearApp(year):
    movies = graph.run(
        'MATCH (m:Movie {year: $year}) RETURN m.title AS title, m.year AS year LIMIT 25', year = year)
    return movies.data()

# promedio de calificaciones de una pelicula
def getMovieAverageRatingApp(title):
    avg = graph.run(
        'MATCH (u: User)-[r:RATED]->(m:Movie {title: $title}) RETURN m.title AS title, avg(toFloat(r.rating)) AS averageRating', title = title)
    return avg.data()

# top de n peliculas
def getMovieTopNApp(n):
    mvs = graph.run(
        'MATCH (u: User )-[r:RATED]->(m:Movie) RETURN m.title AS title, avg(toFloat(r.rating)) AS averageRating order by averageRating desc limit toInteger($n)', n = n)
    return mvs.data()

# top de peliculas con mas nunmero de calificaciones recibidas 
def getMovieNMostRatedApp(n):
    mvs = graph.run(
        'MATCH (u: User )-[r:RATED]->(m:Movie) RETURN m.title AS title, count(r.rating) as NumberOfRatings order by NumberOfRatings desc limit toInteger($n)', n = n)
    return mvs.data()

# calificaciones de un usuario dado
def getUserRatingsApp(user_id):
    ratings = graph.run(
        'MATCH (u:User {id: $user_id})-[r:RATED ]->(movies) RETURN movies.title AS movie, r.rating AS rating', user_id = user_id)
    return ratings.data()

# tags de un usuario dado
def getUserTagsApp(user_id):
    tags = graph.run(
        'MATCH (u:User {id: $user_id})-[t:TAGGED ]->(movies) RETURN movies.title AS title, t.tag AS tag', user_id = user_id)
    return list(tags)

# promedio de calificaciones de un usuario dado
def getUserAverageRatingApp(user_id):
    avg = graph.run(
        'MATCH (u: User {id: $user_id})-[r:RATED]->(m:Movie) RETURN u.id AS user, avg(toFloat(r.rating)) AS averageRating', user_id = user_id)
    return avg.data()

##### Queries de recomendación

# recomendacion de contenido
def getRecContentApp(title, n):
    avg = graph.run('MATCH (m:Movie {title: $title})<-[:HAS_GENRE]-(g:Genre)-[:HAS_GENRE]->(rec:Movie) '
                    'WITH rec, COLLECT(g.name) AS genres, COUNT(*) AS numberOfSharedGenres '
                    'RETURN rec.title as title, genres, numberOfSharedGenres '
                    'ORDER BY numberOfSharedGenres DESC LIMIT toInteger($n)', title = title, n = n)
    return avg.data()

# Recomendación de película kNN usando similitud de Pearson
def getRecCollabApp(user_id, n):
    rec = graph.run('MATCH (u1:User {id: $user_id})-[r:RATED]->(m:Movie) '
                    'WITH u1, avg(toFloat(r.rating)) AS u1_mean '
                    'MATCH (u1)-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2) '
                    'WITH u1, u1_mean, u2, COLLECT({r1: r1, r2: r2}) AS ratings '
                    'MATCH (u2)-[r:RATED]->(m:Movie) '
                    'WITH u1, u1_mean, u2, avg(toFloat(r.rating)) AS u2_mean, ratings '
                    'UNWIND ratings AS r '
                    'WITH sum( (toFloat(r.r1.rating) - u1_mean) * (toFloat(r.r2.rating) - u2_mean) ) AS nom, '
                    'sqrt( sum( (toFloat(r.r1.rating) - u1_mean)^2) * sum( (toFloat(r.r2.rating) - u2_mean) ^2)) AS denom, u1, u2 WHERE denom <> 0 '
                    'WITH u1, u2, nom/denom AS pearson '
                    'ORDER BY pearson DESC LIMIT 10 '
                    'MATCH (u2)-[r:RATED]->(m:Movie) WHERE NOT EXISTS( (u1)-[:RATED]->(m) ) '
                    'RETURN m.title AS title, SUM( pearson * toFloat(r.rating)) AS score '
                    'ORDER BY score DESC LIMIT toInteger($n)', user_id = user_id, n = n)
    return rec.data()