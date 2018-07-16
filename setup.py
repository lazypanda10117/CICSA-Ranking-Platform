import os
import psycopg2
from sqlalchemy.engine.url import make_url


def executeScriptsFromFile(filename, cu):
    fd = open(filename, 'r');
    print('Reading Setup SQL Queries File');
    sql_file = fd.read();
    fd.close();
    sql_commands = sql_file.split(';');
    print('Start Applying Setup SQL Queries');
    for command in sql_commands:
        try:
            if not command == '':
                cu.execute(command)
            else:
                continue;
        except psycopg2.OperationalError as msg:
            print("Command skipped: " + msg);
    print('Finish Applying Setup SQL Queries');


if os.environ.get('SETUP_STATE') == 'True':
    db_remote_url = None;
    db_url = 'localhost';
    db_name = 'ranking';
    db_user = 'lazypanda';
    db_pwd = '';
    db_port = '5432';

    if os.environ.get('DATABASE_URL') is not None:
        db_remote_url = make_url(os.environ.get('DATABASE_URL'));
        db_url = db_remote_url.host;
        db_name = db_remote_url.database;
        db_user = db_remote_url.username;
        db_pwd = db_remote_url.password;
        db_port = db_remote_url.port;

    connection_string = "dbname=%s user=%s password=%s host=%s port=%s" % (db_name, db_user, db_pwd, db_url, db_port)
    conn = psycopg2.connect(connection_string);
    print('Postgres Connection Created');
    conn.autocommit = True;
    cursor = conn.cursor();
    executeScriptsFromFile('setup.sql', cursor);
    conn.close();
    print('Postgres Connection Closed');
