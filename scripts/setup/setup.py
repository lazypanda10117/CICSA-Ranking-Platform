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


def setup():
    if os.environ.get('SETUP_STATE') == 'TRUE':
        dispatcher = {
            1: 'scripts/setup/queries/reset.sql',
            2: 'scripts/setup/queries/setup.sql'
        }

        parser = argparse.ArgumentParser()
        parser.add_argument("mode", help="setup mode", type=int)
        args = parser.parse_args()

        user = os.environ.get("DB_USER", "robot")
        password = os.environ.get("DB_PASS", "rootpwd")
        host = os.environ.get("DB_HOST", "localhost")
        port = os.environ.get("DB_PORT", "5432")
        name = os.environ.get("DB_NAME", "ranking")

        postgresURL = os.environ.get("DATABASE_URL", "None")

        if postgresURL == "None":
            postgresURL = "postgresql://%s:%s@%s:%s/%s" % (
                user, password, host, port, name
            )

        db_url = make_url(postgresURL)
        db_host = db_url.host
        db_name = db_url.database
        db_user = db_url.username
        db_pwd = db_url.password
        db_port = db_url.port

        conn_string = "dbname=%s user=%s password=%s host=%s port=%s" % (db_name, db_user, db_pwd, db_host, db_port)
        conn = psycopg2.connect(conn_string)

        print('Postgres Connection Created')

        conn.autocommit = True
        cursor = conn.cursor()
        executeScriptsFromFile(dispatcher[args.mode], cursor)
        conn.close()

        print('Postgres Connection Closed')


setup()
