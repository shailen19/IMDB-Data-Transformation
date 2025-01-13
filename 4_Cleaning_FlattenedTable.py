import sqlite3
import pandas as pd

r"""
This section is our data cleaning step. We first remove any '\n' characters that end on
the right side of our tconst values ie 'tt2892264\n' or '\N\n'. These become 'tt2892264' and
'\N'. We then remove and NULL value denoted by '\N' so our table is then left with the tconst
values that appear like this example:
ID  tconst
1.  tt34614086
2.  tt1367024
3.  tt0056217
"""


con = sqlite3.connect("Movies.db")

mycursor = con.cursor()

# We UPDATE our table Name_flattened so that, We trim characters from the right on tconst, specifically,
# char(10), the ASCII value new line '\n' distinction. 
# In our WHERE clause we search for ANY character values, denoted by '%', with char(10) piped to
# the end of our char string. ie an tconst ending in '\n'
query = r"UPDATE Name_flattened SET tconst = RTRIM(tconst, char(10)) WHERE tconst LIKE '%' || char(10)"

# We then delete ANY rows that have the NULL value '\N'
query2 = r"DELETE FROM Name_flattened WHERE tconst = '\N'"
mycursor.execute(query)
mycursor.execute(query2)

con.commit()

r"""
As we can see from our query example, all of our NULL values, denoted by '\N' have been 
remove along with any trailing '\n' in our tconst value. Our next step is to join our 
Title_basics table and our Name_flattened table by its tconst value. 
"""

q = r"SELECT * FROM Name_flattened WHERE tconst LIKE '%N%'"

df = pd.read_sql_query(q, con)

print("tconst entries containing N after data clean.")
print(df)

q = r"SELECT * FROM Name_flattened WHERE tconst LIKE '%n%'"

df = pd.read_sql_query(q, con)

print("tconst entries containing m after data clean.")
print(df)

con.close()
