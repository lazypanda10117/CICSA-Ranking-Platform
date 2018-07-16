import os
import psycopg2
from sqlalchemy.engine.url import make_url


def executeScriptsFromFile(filename, cursor):
    fd = open(filename, 'r');
    sql_file = fd.read();
    fd.close();
    sql_commands = sql_file.split(';');
    for command in sql_commands:
        try:
            print(command);
            cursor.execute(command);
        except psycopg2.OperationalError as msg:
            print("Command skipped: " + msg);


if os.environ.get('SETUP_STATE') == 'TRUE':
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

    conn = psycopg2.connect({
        'database': db_name,
        'user': db_user,
        'password': db_pwd,
        'host': db_url,
        'port': db_port
    });
    cursor = conn.cursor();
    executeScriptsFromFile('setup.sql', cursor);
    conn.close();