import sqlite3
import mmap
import time

"""
This project incorporates three imdb tsv files titled name_basics (865 MB), title_basics (978 MB),
and title_ratings (26 MB). We start by connecting to our sqlite3 database, Movies.db, and we use 
the function read_tsv() to read our 3 tsv files into a python object. Finally, we create a table
for each of our tsv read each of thethree objects into three sql tables named, Title_basics, 
Name_basics, and Title_ratings.
"""

# we connect to our sql database
con = sqlite3.connect("Movies.db")

mycursor = con.cursor()


# https://towardsdatascience.com/processing-large-data-files-with-python-multithreading-dbb916f6b58d
def read_tsv(filename):
    with open(filename, 'rb') as fp:
        # map the entire file into memory
        mm = mmap.mmap(fp.fileno(), 0, access=mmap.ACCESS_READ)
        data = []
        # iterate over the block, until next newline
        for line in iter(mm.readline, b""):
            # convert the bytes to a utf-8 string and split the fields
            term = line.decode("utf-8").split("\t")
            # Replace '\N' with None for the entire row at once
            term = [None if value == '\\N' else value for value in term]
            data.append(tuple(term))
        return data

# start time when we begin to read tsv files
start = time.time()
title_basics_table = read_tsv("title_basics.tsv")
name_basics_table = read_tsv("name_basics.tsv")
rating_basics_table = read_tsv("title_ratings.tsv")
# end time after we've read the tsv files in
end = time.time()
print(f"Total time to read our TSV files: {end - start:.2f} seconds.")
print('')


"""
In this section we create our tables for our objects title_basics_table, title_ratings_table,
and name_basics_table.
"""

mycursor.execute("""
    CREATE TABLE if NOT EXISTS Title_basics
        (ID INTEGER PRIMARY KEY,
        tconst TEXT,
        titleType TEXT,
        primaryTitle TEXT,
        originalTitle TEXT,
        isAdult BOOL,
        startYear INT,
        endYear INT,
        runTimeMinutes FLOAT,
        genres TEXT
        )
""")

mycursor.execute("""
    CREATE TABLE if NOT EXISTS Name_basics
        (ID INTEGER PRIMARY KEY,
        nconst TEXT,
        primaryName TEXT,
        birthYear INT,
        deathYear INT,
        primaryProfession TEXT,
        knownForTitles TEXT
        )
""")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Rating_basics
        (ID INTEGER PRIMARY KEY,
        tconst TEXT,
        averageRating FLOAT,
        numVotes INT)
""")



# https://docs.python.org/3/library/sqlite3.html#sqlite3.Cursor.executemany
# executemany(sql, parameters, /)
# rows = [
#     ("row1",),
#     ("row2",),
# ]
# # cur is an sqlite3.Cursor object
# cur.executemany("INSERT INTO data VALUES(?)", rows)

# https://www.w3schools.com/python/python_mysql_insert.asp
# INSERT INTO



""""
In this final section, we read our objects into our three sql tables.  
"""
start = time.time()
mycursor.executemany("""
    INSERT INTO Title_basics (tconst,
        titleType,
        primaryTitle,
        originalTitle,
        isAdult,
        startYear,
        endYear,
        runTimeMinutes,
        genres) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", title_basics_table)

mycursor.executemany("""
    INSERT INTO Name_basics (nconst,
        primaryName,
        birthYear,
        deathYear,
        primaryProfession,
        knownForTitles) VALUES (?, ?, ?, ?, ?, ?)
""", name_basics_table)

mycursor.executemany("""
    INSERT INTO Rating_basics (tconst,
        averageRating,
        numVotes) VALUES (?, ?, ?)
""", rating_basics_table)

end = time.time()


con.commit()
con.close()

print(f"Total time to insert TSV data into SQL tables: {end - start:.2f} seconds")
print("Tsv data successfully INSERT INTO tables.")

""""
To recap, our database Movies has the three tables Title_basics, Name_basics, and Rating_basics.
Each of these three tables contain the data from our three imdb tsv files. 
"""