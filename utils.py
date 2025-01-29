import psycopg2 as pg
from configparser import ConfigParser
import pandas as pd

def loadConfig(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]

    return config


config = loadConfig()

def dbTOdf(query, tablename):

    with pg.connect(**config) as conn:
        cur = conn.cursor()

        cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='{}'".format(tablename))

        columns = cur.fetchall()
        columns = [column[0] for column in columns]

        cur.execute(query)

        rows = cur.fetchall()

        rows = list(rows)
        rows = [list(row) for row in rows]

    data = pd.DataFrame(rows, columns=columns)

    return data