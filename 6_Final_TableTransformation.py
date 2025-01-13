import sqlite3
import pandas as pd
import time

con = sqlite3.connect("Movies.db")
mycursor = con.cursor()

"""
In our final transformation we want to create a Table that has a column for every movie
type such as tvSeries, movie, short, etc. This is done so we can map the runTimeMinutes
values into the movie type column so we no longer need the runTimeMinutes column.
"""

q = """CREATE TABLE IF NOT EXISTS MovieTypeRunTime (
    tconst TEXT PRIMARY KEY,
    MovieTitle TEXT,
    PrimaryActor TEXT,
    shortMinutes TEXT,
    movieMinutes TEXT,
    tvMovieMinutes TEXT,
    tvSeriesMinutes TEXT,
    tvShortMinutes TEXT,
    tvMiniSeriesMinutes TEXT,
    tvSpecialMinutes TEXT,
    videoMinutes TEXT,
    videoGameMinutes TEXT,
    averageRating FLOAT
)
"""

mycursor.execute(q)

"""
We create a list of our movie types that will be used in our runTimeMinutes mapping and 
for our new columns. 
We use as Max CASE WHEN statement to select each one of our titles in our title_types list
to map the runTimeMinute to its column. All other movie types will receive a NULL value.
We use a for loop to iterate through our list everytime our statement is called.
"""
title_types = ['short', 'movie', 'tvMovie', 'tvSeries', 'tvShort', 'tvMiniSeries', 'tvSpecial', 'video', 'videoGame']

# https://www.interviewquery.com/p/sql-max-case-when
select = ','.join([f"MAX(CASE WHEN titleType ='{title}' THEN runTimeMinutes ELSE NULL END) AS {title}" for title in title_types])


"""
We INSERT our values INTO the final Table, MovieTypeRunTime, by passing tconst, MovieTitle,
Primary,Actor, and averageRating from our MovieOverview Table. We also call our {select} statement
from above to map our runTimeMinutes into the correct columns.
"""
query = f"""INSERT INTO MovieTypeRunTime (tconst,
    MovieTitle,
    PrimaryActor,
    shortMinutes,
    movieMinutes,
    tvMovieMinutes,
    tvSeriesMinutes,
    tvShortMinutes,
    tvMiniSeriesMinutes,
    tvSpecialMinutes,
    videoMinutes,
    videoGameMinutes,
    averageRating)
    SELECT tconst, MovieTitle, PrimaryActor, {select}, averageRating 
    FROM MovieOverview 
    GROUP BY MovieTitle, PrimaryActor"""

start = time.time()
mycursor.execute(query)
end = time.time()
print(f"Time it took to INSERT INTO Final Table: {end - start:.2f} seconds")


con.commit()
"""
Our final transformation gives us a table that includes the MovieTitle, PrimaryActor, averageRating
and a column for each movieType. We have mapped the runTime onto each movieType column as show in
the example below:
                 MovieTitle   PrimaryActor movieMinutes  averageRating
0     !Women Art Revolution   B. Ruby Rich           83            6.9
1                  "Giliap"  Albert Vernon          137            6.3
2  "Has Anyone Seen Viljo?"  Aake Kalliala           87            4.4
3          #1 Serial Killer      Al Pierre           87            5.5
4                #1915House  Justin DiPego           55            3.4

As we can see from this query we no longer need the runTimeMinutes column as each value is stored
in each of our title type. By mapping our runTimeMinutes onto our movie types columns we can
conducted analytical tasks such as average runtime by movie type, with respect to their
indivudal columns. This final transformation helps us better visualize the aggregated data. 
"""

"""
To best visualize our Table we call ONLY ONE of our movie type columns at a time per query
and set the movie type column to NOT NULL to only include the times of each movie in that
column. We can SELECT all other columns at our prefered choosing. 
"""

df = pd.read_sql_query("SELECT MovieTitle, PrimaryActor, tvSeriesMinutes, averageRating FROM MovieTypeRunTime WHERE tvSeriesMinutes IS NOT NULL  ORDER BY averageRating DESC LIMIT 5", con)
print(df)

con.close()