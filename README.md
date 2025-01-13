# IMDB-Data-Transformation

**Overview**
Ths project focuses on cleaning and transforming raw data from three IMDB TSV files: **name_basics**, **title_basics**, and **title_ratings** 
into a structed SQLite3 database. The key aim is to restructure the tables and map movie attributes for insightful analysis. 

**Steps Taken:**
1. **Load Data into SQLite3** We begin by connect to the "Movies.db" SQL database. Three large TSV files (865 MB for Name_basics, 978 MB for
Title_basics, and 26 MB for Title_ratings) are read into python objects using ```mmap``` for efficient file handling. The data is then inserted into
the three SQL tables: ```Title_basics```, ```Name_basics```, and ```Title_ratings```. These steps are done with files ```1_CreateDB_and_Tables``` and 
```2_LoadTSV_INTO_Tables```. 

2. **Flatten Data**
The ```Name_basics``` table contains a column named ```knownForTitles```, which lists multiple movie IDs (tconst), seperated by commas ie ```tt0137523,tt0356910,
tt1210166,tt0114746\n```. A recursive SQL CTE is used to flatten the data so that each ```tconst``` from ```knownForTitles``` has its own row so we can
```join``` all three tables. This step is done in file ```3_FlattenTable_Transformation```.
3. **Data Cleaning**
   The flatten tconst values have trailing ```\n``` values ie ```tt2892264\n```, along with invalid ```\N``` values. The data cleaning step is
   performed with file ```4_Cleaning_FlattenedTable```. After this step the data just contains its tconst values ie ```tt2892264```.
4. **Joining Data**
   A CTE is used to ```JOIN``` the ```Title_basics```, ```Name_basics``` (now ```Name_flattened```), and ```Rating_basics``` tables
   using the ```tconst``` values. The result is stored on the intermediate table ```MovieOverview```. This step is performed with file ```5_IntermediateJOIN```.
5. **Mapping RunTimeMinutes by MovieType**
   A transformation is made to map the values from ```RunTimeMinutes``` onto the column for each movie type ie (movie, tvSeries, etc) on our final table. A list
   of movie types is create and a ```CASE WHEN``` sql statement is used in conjunction with a for loop to achieve this mapping technique. The final
   table ```MovieTypeRunTime``` is a much more clear table that allows efficient analysis of runtime, while retaining valuable data about the ```PrimaryActor```
   and ```averageRating```. In a seperate file, SQL commands such as ```SELECT MovieTitle, PrimaryActor, tvSeriesMinutes, averageRating
    FROM MovieTypeRunTime WHERE tvSeriesMinutes IS NOT NULL``` can be run to analyze the run time from each specific movie type. This final transformation is performed
   with file ```6_Final_TableTransformation```.

**How to Run:**
To run this project, you will need to download all of the python files in this repository and run them in order from 1 through 6. 

**1. Set Up Your Environment** Ensure you have VS Code installed.

**2. Run each file** As you run each file you should see example outputs such as: ```Total time to read our TSV files: 110.03 seconds.```, 
```,Time to recursively flatten and read INTO our Name_flattened table: 45.56 seconds.```, and 
```Time it took to INSERT and JOIN our tables in the MovieOverview table: 365.62 seconds.```

**3. Query Database** Once all files have been ran in order, open a seperate file and connect to the ```Movie.db``` SQLite3 database and begin
querying the table.

