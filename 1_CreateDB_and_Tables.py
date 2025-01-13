import sqlite3

"""
 We start by connecting to our sqlite3 database, Movies.db, and we use 
the function read_tsv() to read our 3 tsv files into a python object. Finally, we create a table
for each of our tsv read each of thethree objects into three sql tables named, Title_basics, 
Name_basics, and Title_ratings.
"""

# https://docs.python.org/3/library/sqlite3.html
# we pass our database to sqlite3.connect() to create a connection to the database
# in the current working directory, **implicitly creating it if it does not exist**
con = sqlite3.connect("Movies.db")

# In order to execute SQL statements and fetch results from SQL queries,
#  we will need to use a database cursor.
# 
# https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor
# A Cursor object represents a database cursor which is used to execute SQL statements,
#  and manage the context of a fetch operation. Cursors are created using Connection.cursor()
mycursor = con.cursor()




# we auto increment our primary key sop that anytime we add a new person
# to our table we automatically generate a UNIQUE primary key
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Title_basics  (
        ID INT PRIMARY KEY,
        tconst,
        titleType TEXT,
        primaryTitle TEXT,
        originalTitle TEXT,
        isAdult BOOLEAN,
        startYear INT,
        endYear INT,
        runTimeMinutes INT,
        genres TEXT
        )
    """)

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Name_basics (
        ID INT PRIMARY KEY,
        nconst TEXT,
        primaryName TEXT,
        birthYear INT,
        deathYear INT,
        primaryProfession TEXT,
        knownForTitles TEXT
        )
    """)

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Rating_basics (
        ID INT PRIMARY KEY,
        tconst TEXT,
        averageRating FLOAT,
        numVotes INT
            )
    """)

print("Tables successfully created.")