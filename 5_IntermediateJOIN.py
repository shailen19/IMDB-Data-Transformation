import sqlite3
import pandas as pd
import time



"""
This step is our JOIN step. We create an intermediate table called MovieOverview which
will contain columns from our Movie_basics, Rating_basics and Name_flattened table. We use an intermediate CTE
to JOIN our tables and INSERT it into the MoviewOverview table.

If we run the queries:
q = r"SELECT COUNT(DISTINCT tconst) as count FROM Title_basics"
q2= r"SELECT COUNT(DISTINCT tconst) as count FROM Name_flattened"
q2= r"SELECT COUNT(DISTINCT tconst) as count FROM Rating_basics"

We get:
Title_basics
    - DISTINCT tconst values: 11,351,606
Name_flattened
    - DISTINCT tconst values: 2,073,621
Rating_basics
    - DISTINCT tconst values: 1,519,068

This means that on our INNER JOIN table the MAX possible join values we can achive is
1,519,068. 
"""

con = sqlite3.connect("Movies.db")

mycursor = con.cursor()

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS MovieOverview (
        tconst TEXT PRIMARY KEY,
        PrimaryActor TEXT,
        MovieTitle TEXT,
        averageRating FLOAT,
        titleType TEXT,
        runTimeMinutes INTEGER
        )
    """)



query = r"""
-- We use INGORE INTO to avoid any ERRORS when running into duplicate tconst values, as we
-- INSERT columns from the Title_basics, Rating_basics, and Name_flattened tables
INSERT or IGNORE INTO MovieOverview (tconst, PrimaryActor, MovieTitle, averageRating, titleType, runTimeMinutes)
WITH MovieTitles AS(
    SELECT tconst,
        primaryTitle as MovieTitle,
        titleType,
        runTimeMinutes
    FROM 
        Title_basics

), 

MovieRatings AS(
    SELECT tconst,
        averageRating
    FROM
        Rating_basics
),

ActorNames AS(
    SELECT tconst,
        PrimaryActor
    FROM
        Name_flattened
)
SELECT
    MovieTitles.tconst,
    ActorNames.PrimaryActor,
    MovieTitles.MovieTitle,
    MovieRatings.averageRating,
    MovieTitles.titleType,
    MovieTitles.runTimeMinutes
    
From 
    MovieTitles
-- We perform an INNER JOIN so that only matches between both of our
-- tables are mapped onto the MovieOverview table
JOIN ActorNames ON MovieTitles.tconst = ActorNames.tconst
JOIN MovieRatings ON MovieTitles.tconst = MovieRatings.tconst
"""
start = time.time()
mycursor.execute(query)
end = time.time()
con.commit()

print(f"Time it took to INSERT and JOIN our tables in the MovieOverview table: {end - start:.2f} seconds.")
"""
This test query will show that 
"""
q = r"SELECT * FROM MovieOverview"

df = pd.read_sql_query(q, con)
print(f"The length of our table is: {len(df)}")

q2 = r"SELECT * FROM MovieOverview LIMIT 10"
df = pd.read_sql_query(q2, con)
print(df)




con.close()