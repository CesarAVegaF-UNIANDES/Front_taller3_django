from py2neo import Graph, Node, NodeMatcher

# Online
uri = "neo4j+s://608fe23b.databases.neo4j.io"
user = "neo4j"
password = "hmIjUUeSo9q9N_OhaHUJSe9CdK0WEYSGgrnZTX3VoK0"

# Online
# uri = "bolt://localhost:7687"
# user = "neo4j"
# password = "taller3"

print("Graph")
graph = Graph(uri, auth=(user, password))
print("Cargado")

def getMovieDataApp(title):
    matcher = NodeMatcher(graph)
    movie = matcher.match("Movie", title={title}).first()
    return movie

def getMovieGenresApp(title):
    genres = graph.run('MATCH (genres)-[:HAS_GENRE]->(m:Movie {title: $title}) RETURN genres.name', title=title)
    return list(genres)

def getMovieRatingsApp(title):
    ratings = graph.run(
        'MATCH (u: User)-[r:RATED]->(m:Movie {title: $title}) RETURN u.id AS user, r.rating AS rating', title = title)
    return ratings.data()

def getMovieTagsApp(title):
    tags = graph.run(
        'MATCH (u: User)-[t:TAGGED]->(m:Movie {title: $title}) RETURN u.id AS user, t.tag AS tag', title = title)
    return tags.data()

def getMoviesByYearApp(year):
    movies = graph.run(
        'MATCH (m:Movie {year: $year}) RETURN m.title AS title, m.year AS year LIMIT 25', year = year)
    return movies.data()

def getMovieAverageRatingApp(title):
    avg = graph.run(
        'MATCH (u: User)-[r:RATED]->(m:Movie {title: $title}) RETURN m.title AS title, avg(toFloat(r.rating)) AS averageRating', title = title)
    return avg.data()

def getMovieTopNApp(n):
    mvs = graph.run(
        'MATCH (u: User )-[r:RATED]->(m:Movie) RETURN m.title AS title, avg(toFloat(r.rating)) AS averageRating order by averageRating desc limit toInteger($n)', n = n)
    return mvs.data()

def getMovieNMostRatedApp(n):
    mvs = graph.run(
        'MATCH (u: User )-[r:RATED]->(m:Movie) RETURN m.title AS title, count(r.rating) as NumberOfRatings order by NumberOfRatings desc limit toInteger($n)', n = n)
    return mvs.data()

def getUserRatingsApp(user_id):
    ratings = graph.run(
        'MATCH (u:User {id: $user_id})-[r:RATED ]->(movies) RETURN movies.title AS movie, r.rating AS rating', user_id = user_id)
    return ratings.data()

def getUserTagsApp(user_id):
    tags = graph.run(
        'MATCH (u:User {id: $user_id})-[t:TAGGED ]->(movies) RETURN movies.title AS title, t.tag AS tag', user_id = user_id)
    return tags.data()

def getUserAverageRatingApp(user_id):
    avg = graph.run(
        'MATCH (u: User {id: $user_id})-[r:RATED]->(m:Movie) RETURN u.id AS user, avg(toFloat(r.rating)) AS averageRating', user_id = user_id)
    return avg.data()

def getRecContentApp(title, n):
    avg = graph.run('MATCH (m:Movie {title: $title})<-[:HAS_GENRE]-(g:Genre)-[:HAS_GENRE]->(rec:Movie) '
                    'WITH rec, COLLECT(g.name) AS genres, COUNT(*) AS numberOfSharedGenres '
                    'RETURN rec.title as title, genres, numberOfSharedGenres '
                    'ORDER BY numberOfSharedGenres DESC LIMIT toInteger($n)', title = title, n = n)
    return avg.data()

def getRecCollabApp(user_id, n):
    rec = graph.run('MATCH (u1:User {id: $user_id})-[r:RATED]->(m:Movie) '
                    'WITH u1, avg(toFloat(r.rating)) AS u1_mean '
                    'MATCH (u1)-[r1:RATED]->(m:Movie)<-[r2:RATED]-(u2) '
                    'WITH u1, u1_mean, u2, COLLECT({r1: r1, r2: r2}) AS ratings WHERE size(ratings) > 10 '
                    'MATCH (u2)-[r:RATED]->(m:Movie) '
                    'WITH u1, u1_mean, u2, avg(toFloat(r.rating)) AS u2_mean, ratings '
                    'UNWIND ratings AS r '
                    'WITH sum( (r.r1.rating-u1_mean) * (r.r2.rating-u2_mean) ) AS nom, '
                    'sqrt( sum( (r.r1.rating - u1_mean)^2) * sum( (r.r2.rating - u2_mean) ^2)) AS denom, u1, u2 WHERE denom <> 0 '
                    'WITH u1, u2, nom/denom AS pearson '
                    'ORDER BY pearson DESC LIMIT 10 '
                    'MATCH (u2)-[r:RATED]->(m:Movie) WHERE NOT EXISTS( (u1)-[:RATED]->(m) ) '
                    'RETURN m.title AS title, SUM( pearson * r.rating) AS score '
                    'ORDER BY score DESC LIMIT toInteger($n)', user_id = user_id, n = n)
    return rec.data()

def getRecCollabGenderApp(user_id, n):
    rec = graph.run('MATCH (u:User {id: $user_id})-[r:RATED]->(m:Movie),'
                    '(m)-[:HAS_GENRE]->(g:Genre)<-[:HAS_GENRE]-(rec:Movie) '
                    'WHERE NOT EXISTS( (u)-[:RATED]->(rec) ) '
                    'WITH rec, [g.name, COUNT(*)] AS scores '
                    'RETURN rec.title AS recommendation, rec.year AS year, '
                    'COLLECT(scores) AS scoreComponents,'
                    'REDUCE (s=0,x in COLLECT(scores) | s+x[1]) AS score '
                    'ORDER BY score DESC LIMIT toInteger($n)', user_id = user_id, n = n)
    return rec.data()