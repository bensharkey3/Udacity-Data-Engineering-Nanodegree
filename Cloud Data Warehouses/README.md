# Udacity Data Engineer Nanodegree: Cloud Data Warehouses
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

The objective of this project is to build an ETL pipeline that extracts the data from S3, stages them in Redshift, and then transforms data into a set of dimensional tables that can be used by Sparkify for analytics purposes.

Loading to Redshift is done by running SQL copy commands from S3 to the Redshift staging tables. Records are then loaded into the dimensional tables from the staging tables using SQL commands.

The ETL process is run by executing the following Python code in order:
    - create_tables.py
    - etl.py
    
Python is used to connect to the S3 data sources, to Redshift and to trigger the execution of SQL queries that do the following:
    - drop any existing tables
    - create the staging and dimensional tables
    - populate the staging tables
    - populate the dimanstional tables

The AWS console is used to launch a Redshift cluster.