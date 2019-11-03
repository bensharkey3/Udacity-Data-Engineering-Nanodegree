import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    '''
    Inserts data from s3 buckets to the 2x staging tables using the COPY command in Redshift
    '''
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    '''
    Loads data from the 2x staging tables to the analytics tables
    '''
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''
    Runs the load_staging_tables and insert_tables functions. Uses config file 'dwh.cfg' to build connection
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    print('load_staging_tables - All Completed')
    insert_tables(cur, conn)
    print('insert_tables - All Completed')

    conn.close()


if __name__ == "__main__":
    main()