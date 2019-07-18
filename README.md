# Udacity Data Engineer Nanodegree: Data Modeling with PostgreSQL
This is the first project in the course and it involves using Python to create and loading a data warehouse with data for the startup music streaming service 'Sparkify'. The project involves:
* creating a PostgreSQL data warehouse 
* develop normalised tables for the data warehouse in a star schema to eliminate data redundancy
* populate the tables with data loaded from JSON files

Creating and loading this database with the song and log data means that the data is more easily queried and used by Sparkify for analytical purposes.

# How to run the python scripts
### Step 1
run create_tables.py to create the database and tables in it.
 - creates and connects to the sparkifydb database
 - creates the 5 tables: songs, artists, songplays, users, time 
### Step 2
run etl.py to process the song and log files.
 - processes the song file data into the songs and artist tables
 - processes the log files into each table

# Explanation of the files in the repository
process_song_file function loads song file details into the nomalised songs and artists tables.
process_log_file function loads log file details into the normalised songplays, users, and time tables.