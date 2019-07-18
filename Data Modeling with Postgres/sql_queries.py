# DROP TABLES
songplay_table_drop = "drop table if exists songplay"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists song"
artist_table_drop = "drop table if exists artist"
time_table_drop = "drop table if exists time"

# CREATE TABLES
songplay_table_create = ("""
create table songplays (
    ts varchar PRIMARY KEY, 
    userId int NOT NULL, 
    level varchar, 
    song_id varchar, 
    artist_id varchar, 
    session_id int, 
    location varchar, 
    user_agent varchar
)
""")

user_table_create = ("""
create table users (
    user_id int PRIMARY KEY, 
    first_name varchar NOT NULL, 
    last_name varchar NOT NULL, 
    gender varchar, 
    level varchar
)
""")

song_table_create = ("""
create table songs (
    song_id varchar PRIMARY KEY, 
    title varchar NOT NULL, 
    artist_id varchar NOT NULL, 
    year int, 
    duration float  
)
""")

artist_table_create = ("""
create table artists (
    artist_id varchar PRIMARY KEY, 
    name varchar NOT NULL, 
    location varchar, 
    lattitude float, 
    longitude float
)
""")

time_table_create = ("""
create table time (
    start_time varchar PRIMARY KEY, 
    hour int, 
    day int, 
    week int, 
    month int, 
    year int, 
    weekday varchar
)
""")

# INSERT RECORDS
songplay_table_insert = ("""
insert into songplays
values (%s, %s, %s, %s, %s, %s, %s, %s)
on conflict (ts) do nothing
""")

user_table_insert = ("""
insert into users
VALUES (%s, %s, %s, %s, %s)
on conflict (user_id) do nothing
""")

song_table_insert = ("""
insert into songs
VALUES (%s, %s, %s, %s, %s)
on conflict (song_id) do nothing
""")

artist_table_insert = ("""
insert into artists
VALUES (%s, %s, %s, %s, %s)
on conflict (artist_id) do nothing
""")


time_table_insert = ("""
insert into time 
values (%s, %s, %s, %s, %s, %s, %s)
on conflict (start_time) do nothing
""")

# FIND SONGS
song_select = ("""
select 
    s.song_ID,
    a.artist_ID
from songs s
inner join artists a on a.artist_id = s.artist_id

""")

# QUERY LISTS
create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]