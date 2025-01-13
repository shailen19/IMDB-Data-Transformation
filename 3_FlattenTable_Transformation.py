import sqlite3
import pandas as pd
import time

con = sqlite3.connect("Movies.db")


r"""
Our Title_basics table stores each tconst as a unique identifier. However, the Name_basics
table stores each of these tconsts in a column called knownForTitles. This column may contain
multiple tconsts such as tt0137523,tt0356910,tt1210166,tt0114746\n. We want each of these
tconst values to be represented as individual rows. To do this we use a recursive splitter
CTE that will go through each row of our multi 'part' tconsts and seperate them. The workflow
will look like this:

ID   knownForTitles
1.   tt0137523,tt0356910,tt1210166,tt0114746\n

This transforms to:
ID   knownForTitles                        ID  tconst           
1.   tt0356910,tt1210166,tt0114746\n       1.  tt0137523

ID   knownForTitles                        ID  tconst     
1.   tt1210166,tt0114746\n                 1.  tt0137523
                                           2.  tt0356910

ID   knownForTitles                        ID  tconst
1.   tt0114746\n                           1.  tt0137523
                                           2.  tt0356910
                                           3.  tt1210166

ID  knownForTitles                         ID  tconst
                                           1. tt0137523
                                           2. tt0356910
                                           3. tt1210166
                                           4. tt0114746\n 

This step will thus seperate the knownForTitles values into seperate tcosnt values.
This may create duplicates, and as we can see in the last recusive call our value is
'tt0114746\n'. We will need to reomve the '\n' in the data cleaning step along with any
NULL values.                                           
"""

mycursor = con.cursor()

"""
We first create a new table called Name_flattened, which will store all of our individual
tconst values and the PrimaryActor that belongs to each tconst value. 
"""

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS Name_flattened (
        ID INTEGER,
        PrimaryActor TEXT,
        tconst TEXT
        )
    """)

"""
Since sqlite3 doesn't have a built in UNNEST() function liek PostgreSQL, we will need to do
a recursive call to flatten our list. We implement a similar recursive CTE to the one describe
on geeks for geeks.
"""

# https://www.geeksforgeeks.org/how-to-split-a-delimited-string-to-access-individual-items-in-sqlite/
# 2. Using the Recursive Common Table Expression (CTE)
query = r"""
WITH RECURSIVE Splitter AS (
    -- Base case -- Initial split of knownForTitles tt0137523,tt0356910,tt1210166,tt0114746\n 
    -- part - tt0137523
    -- remainder - tt0356910,tt1210166,tt0114746\n
    SELECT ID,
        primaryName,
        SUBSTR(knownForTitles, 1, INSTR(knownForTitles || ',', ',') - 1) AS part,
        SUBSTR(knownForTitles, INSTR(knownForTitles || ',', ',') + 1) AS remainder
    FROM
        Name_basics
    -- exclude NULL or NULL placeholder '\N' in our Splitter CTE
    WHERE knownForTitles IS NOT NULL OR knownForTitles != '\N'

    UNION ALL 
    -- Recursive Case -- as we split the first part, now we split the remainder
    SELECT
        ID,
        primaryName,
        SUBSTR(remainder, 1, INSTR(remainder || ',', ',') - 1) AS part,
        SUBSTR(remainder, INSTR(remainder || ',', ',') + 1) AS remainder
    FROM
        Splitter
    WHERE
        -- 
        remainder !='' 
        AND remainder != '\N' 
        AND remainder != '\n'
        AND remainder != '\N\n'
)

INSERT INTO Name_flattened (
    ID,
    PrimaryActor,
    tconst)
SELECT ID,
    primaryName,
    part
FROM 
    Splitter;
"""
start = time.time()
mycursor.execute(query)
end = time.time()
print(f"Time to recursively flatten and read INTO our Name_flattened table: {end - start:.2f} seconds")
print('')

start = time.time()
querypandas = ("SELECT * FROM Name_flattened WHERE PrimaryActor LIKE 'John Wayne'")
df = pd.read_sql_query(querypandas, con)
end = time.time()

r""""
As we can see, the knownForTitles column has be flattened into our tconst column. From our
SELECT example we can see that some ttconst vlaues contain '\n' at the end of the string. 
Additionally, we have empty tconst values denoted by '\N\n'.In the next step we will remove
these values so we can better JOIN our Tilte_basics and Name_flattened tables. 
"""

print(df)
print(f"Time to execute SQL query: {end - start:.2f} seconds")


con.commit()
con.close()