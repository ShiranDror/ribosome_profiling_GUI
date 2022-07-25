import sqlite3

import sys
sys.path.append(".")

from sqlite3 import Error
from funcs.db_tables import GetCreateTableCommands



DB_FILE = ""


def get_connection():
    """ returns conn """
    conn = None
    # DB_FILE
    try:
        conn = sqlite3.connect(DB_FILE.as_posix())
        
    except Error as err:
        print(err)
        if conn:
            conn.close()

    return conn


def get_cursor():
    """ returns cursor, conn """
    conn = get_connection()
    try:
        cursor = conn.cursor()
    except Error as e:
        conn.close()
        print(e)
    return cursor, conn


def create_database(db_file):
    """ create a database connection to a SQLite database """
    global DB_FILE
    DB_FILE = db_file
    cursor, conn = get_cursor()
    create_tables(cursor)
    print("Created SQLite database, version", sqlite3.version)
    conn.close()


def create_tables(cursor):
    for create_table_command in GetCreateTableCommands():
        try:
            cursor.execute(create_table_command)
        except Error as e:
            print(e)
            print("Failed", create_table_command)


def save_new_datasource(ds):
    """ Saves new datasource to database """

    sql = """ INSERT INTO DataSources(Name, Description, Color, IsActive)
                VALUES(?,?,?,?)
        """
    sql_tuples = """  INSERT INTO DataSourceTuples(DataFilePath, ControlDataFilePath, DataSourceId)
                        VALUES(?,?,?)
                """
    cursor, conn = get_cursor()

    with conn:
        cursor.execute(sql, ds.GetSQLTuple())
        data_source_id = cursor.lastrowid
        ds.SetId(data_source_id)
        for t in ds.GetDataPathsList():
            insert = (t[0], t[1], data_source_id)
            cursor.execute(sql_tuples, insert)


def load_datasources():
    """ Loads all datasources from database """
    from models.data_source import DataSource
    cur, conn = get_cursor()
    ds_list = []
    with conn:

        cur.execute("SELECT * FROM DataSources")

        rows = cur.fetchall()

        # this could and should be optimized...
        for row in rows:
            ds = DataSource(*row)
            cur.execute("SELECT DataFilePath,ControlDataFilePath,DataSourceId FROM DataSourceTuples WHERE DataSourceId = " + str(ds.GetId()))
            tups = cur.fetchall()
            for tup in tups:
                ds.AddData((tup[0], tup[1]))
            ds_list.append(ds)
    return ds_list

def delete_datasource(datasource_id: int):
    """ deletes datasource and related datasourcetuples from database """
    cur, conn = get_cursor()
    with conn:

        sql1 = """ DELETE FROM DataSourceTuples WHERE DataSourceId = ? """
        sql2 = """ DELETE FROM DataSources WHERE DataSourceId = ? """
        cur.execute(sql1, (str(datasource_id),))
        cur.execute(sql2, (str(datasource_id),))
        conn.commit()
             
def update_dataset_color(data_source_id: int, new_color: str):
    """ updates DataSource's color in the database """
    cur, conn = get_cursor()
    with conn:
        sql_vars = (new_color, str(data_source_id))
        sql = """ UPDATE DataSources SET Color = ? WHERE DataSourceId = ? """
        cur.execute(sql, sql_vars)
        conn.commit()
        
def toggle_dataset_active(data_source_id: int):
    cur, conn = get_cursor()
    with conn:
        sql_vars = (str(data_source_id),)
        sql = """ UPDATE DataSources
                    SET IsActive =  CASE IsActive
                                    WHEN 1 THEN 0
                                    ELSE 1
                                    END
                        
                    WHERE DataSourceId = ?
         """
        cur.execute(sql, sql_vars)
        conn.commit()
