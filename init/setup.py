import os
import psycopg2
import argparse
from sqlalchemy.engine.url import make_url


def executeScriptsFromFile(filename, cu):
    fd = open(filename, 'r')
    print('Reading Setup SQL Queries File')
    sql_file = fd.read()
    fd.close()
    sql_commands = sql_file.split(';')
    print('Start Applying Setup SQL Queries')
    for command in sql_commands:
        try:
            if not command == '':
                cu.execute(command)
            else:
                continue
        except psycopg2.OperationalError as msg:
            print("Command skipped: " + str(msg))
    print('Finish Applying Setup SQL Queries')


def main():
    if os.environ.get('SETUP_STATE') == 'True':
        dispatcher = {1: 'reset.sql', 2: 'setup.sql'}

        parser = argparse.ArgumentParser()
        parser.add_argument("mode", help="setup mode", type=int)
        args = parser.parse_args()

        db_url = 'localhost'
        db_name = 'ranking'
        db_user = 'lazypanda'
        db_pwd = ''
        db_port = '5432'

        if os.environ.get('DATABASE_URL') is not None:
            db_remote_url = make_url(os.environ.get('DATABASE_URL'))
            db_url = db_remote_url.host
            db_name = db_remote_url.database
            db_user = db_remote_url.username
            db_pwd = db_remote_url.password
            db_port = db_remote_url.port

        conn_string = "dbname=%s user=%s password=%s host=%s port=%s" % (db_name, db_user, db_pwd, db_url, db_port)
        conn = psycopg2.connect(conn_string)
        print('Postgres Connection Created')
        conn.autocommit = True
        cursor = conn.cursor()
        executeScriptsFromFile(dispatcher[args.mode], cursor)
        conn.close()
        print('Postgres Connection Closed')


main()
