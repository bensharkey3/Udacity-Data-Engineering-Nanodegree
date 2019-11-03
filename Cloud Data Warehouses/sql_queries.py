import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = "drop table if exists staging_events"
staging_songs_table_drop = "drop table if exists staging_songs"
songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES
staging_events_table_create= ("""
create table staging_events (
    artist varchar,
    auth varchar,
    firstName varchar,
    gender varchar,
    itemInSession int,
    lastName varchar,
    length float,
    level varchar,
    location varchar,
    method varchar,
    page varchar,
    registration varchar,
    sessionId int, 
    song varchar,
    status int,
    ts varchar,
    userAgent varchar,
    userId int);
""")

staging_songs_table_create = ("""
create table staging_songs (
    num_songs varchar,
    artist_id varchar,
    artist_latitude float,
    artist_logitude float,
    artist_location varchar,
    artist_name varchar,
    song_id varchar,
    title varchar,
    duration float,
    year int);
""")



songplay_table_create = ("""
create table songplays (
    songplay_id int identity(0,1) PRIMARY KEY, 
    start_time timestamp SORTKEY DISTKEY, 
    user_id int NOT NULL, 
    level varchar, 
    song_id varchar NOT NULL, 
    artist_id varchar NOT NULL, 
    session_id int, 
    location varchar,
    user_agent varchar
)
""")

user_table_create = ("""
create table users (
    user_id int SORTKEY PRIMARY KEY, 
    first_name varchar NOT NULL, 
    last_name varchar NOT NULL, 
    gender varchar, 
    level varchar
)
""")

song_table_create = ("""
create table songs (
    song_id varchar SORTKEY PRIMARY KEY, 
    title varchar NOT NULL, 
    artist_id varchar NOT NULL, 
    year int, 
    duration float  
)
""")

artist_table_create = ("""
create table artists (
    artist_id varchar SORTKEY PRIMARY KEY, 
    name varchar NOT NULL, 
    location varchar, 
    lattitude float, 
    longitude float
)
""")

time_table_create = ("""
create table time (
    start_time varchar DISTKEY SORTKEY PRIMARY KEY, 
    hr int, 
    day varchar, 
    week varchar, 
    month varchar, 
    year int, 
    weekday varchar
)
""")


# STAGING TABLES
staging_events_copy = ("""
copy staging_events
from {log_data}
iam_role {arn}
region 'us-west-2'    -- try change to 'us-west-2' as it seems that thats the region the s3 buckets are in
-- compupdate off
format as json {log_jsonpath};
""").format(log_data=config.get('S3', 'LOG_DATA'), 
            arn=config.get('IAM_ROLE', 'ARN'), 
            log_jsonpath=config.get('S3', 'LOG_JSONPATH'))


staging_songs_copy = ("""
copy staging_songs
from {song_data}
iam_role {arn}
region 'us-west-2'    -- try change to 'us-west-2' as it seems that thats the region the s3 buckets are in
-- compupdate off
format as json 'auto';
""").format(song_data=config.get('S3', 'SONG_DATA'), 
            arn=config.get('IAM_ROLE', 'ARN'))


# FINAL TABLES
songplay_table_insert = ("""
insert into songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
select 
    distinct (e.ts) start_time,
    e.userId user_id,
    e.level,
    s.song_id,
    s.artist_id,
    e.sessionId session_id,
    e.location,
    e.userAgent user_agent
from staging_events e
join staging_songs s on s.title = e.song and s.artist_name = e.artist
    
""")

user_table_insert = ("""
insert into users (user_id, first_name, last_name, gender, level)
select 
    distinct (userId) user_id,
    firstName first_name,
    lastName last_name,
    gender,
    level
from staging_events
where user_id is not null;
""")

song_table_insert = ("""
insert into songs (song_id, title, artist_id, year, duration)
select 
    distinct (song_id) song_id, 
    title, 
    artist_id, 
    year, 
    duration 
from staging_songs
where song_id is not null;
""")

artist_table_insert = ("""
insert into artists (artist_id, name, location, lattitude, longitude)
select
    distinct (artist_id) artist_id, 
    artist_name, 
    artist_location, 
    artist_latitude, 
    artist_logitude
from staging_songs
where artist_id is not null;
""")

time_table_insert = ("""
insert into time (start_time, hr, day, week, month, year, weekday)
select 
    start_time, 
    extract(hour from start_time) as hr, 
    extract(day from start_time) as day, 
    extract(week from start_time) as week, 
    extract(month from start_time) as month, 
    extract(year from start_time) as year, 
    extract(weekday from start_time) as weekday
from songplays
where start_time is not null
""")

# QUERY LISTS
create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]

drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
