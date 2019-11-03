import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    '''
    Drops all tables in database using drop_table_queries
    '''
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    '''
    Creates all tables in database using create_table_queries
    '''
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    '''
    Runs the drop_tables and create_tables functions. Uses config file 'dwh.cfg' to build connection
    '''
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    print('drop_tables - All Completed')
    create_tables(cur, conn)
    print('create_tables - All Completed')

    conn.close()


if __name__ == "__main__":
    main()