import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def get_files(filepath):
    '''This function can be used to create a list with all files in the filepath.
    Arguments: 
        filepath: filepath of the folder containing the files 
    Returns: 
        all_files
    '''
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))
    return all_files


def process_song_file(cur, filepath):
    '''This function inserts records into the songs and artists tables.
    Arguments: 
        filepath: filepath of the folder containing the files 
        cur: the cursor object
    Returns:
        none
    '''
    df = pd.read_json(filepath, lines=True)
    
    # insert song record
    song_data = list(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0,])  
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0,])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    '''This function  writes a log file into the tables.
    Arguments: 
        filepath: filepath of the folder containing the files 
        cur: the cursor object
    Returns:
        none
    '''
    df = pd.read_json(filepath, lines=True)
    
    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # timestamp, hour, day, week of year, month, year, and weekday
    hour = t.dt.hour
    day = t.dt.day
    week_of_year = t.dt.week
    month = t.dt.month
    year = t.dt.year
    weekday = t.dt.weekday
    
    # insert time data records
    time_data = list(zip(t, hour, day, week_of_year, month, year, weekday)) 
    column_labels = ('timestamp', 'hour', 'day', 'week_of_year', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''This function processes data from the given filepath,
    Arguments: 
        filepath: filepath of the folder containing the files 
        cur: the cursor object
        conn: the connection object
        func: the function used
    Returns:
        none
    '''
    # get all files matching extension from directory 
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))
    
    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    '''This function creates database connection and runs the process_data function for song and log data
    Arguments: 
        none
    Returns:
        none
    '''
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()