#import sqlite3
import sqlean as sqlite3
import pandas as pd
import os.path

# get current working directory
path = os.getcwd()

path = f"{path}{os.sep}DB"
BASE_DIR = path

'''
VIEW:
v_complete_names            = official and alternative games names
v_official_names            = official games names
v_alternative_names         = alternative games names

v_agr_all                   = aggregate complete
v_agr_releases              = aggregate releases
v_agr_genres                = aggregate genres
v_agr_publishers            = aggregate publishers
v_agr_developers            = aggregate developers
v_agr_game_engines          = aggregate engine
v_agr_player_perspectives   = aggregate perspectives

t_agr_all                   = v_agr_all table
'''

class DATABASE():
    def __init__(self, db_name, db_path = BASE_DIR):
        print(f"<Info - SQL> SQLite v.{sqlite3.sqlite_version}")
        self.db_name = db_name
        self.db_path = os.path.join(db_path, db_name)
        self.db_conn, self.db_cur = self.__connect()


    def __enter__(self):
        return self


    def __exit__(self, ext_type, exc_value, traceback):
        self.db_cur.close()
        if isinstance(exc_value, Exception):
            self.db_conn.rollback()
        else:
            self.db_conn.commit()
        self.db_conn.close()


    def __connect(self):
        try:
            db_conn = sqlite3.connect(self.db_path)
            # this forces the client to load additional extensions avaible,
            # useful for multi os support
            db_conn.enable_load_extension(True)
        except Exception as e:
            print(f"<Error! - SQL> Connection: {e}")
            return

        db_cur = db_conn.cursor()
        return db_conn, db_cur


    def close(self):
        self.db_conn.close()


    def tune(self):

        try:
            self.db_cur.execute(f"PRAGMA synchronous = NORMAL") # Synchronous Commit
            self.db_cur.execute(f"PRAGMA cache_size = -4000")# Max memory cache size
            self.db_cur.execute(f"PRAGMA temp_store = MEMORY") # Temporary files location
            self.db_cur.execute(f"PRAGMA mmap_size = 30000000000") # Enable memory mapping
            self.db_cur.execute(f"PRAGMA journal_mode = WAL") # Journal Mode
        except Exception as e:
            print(f"<Error! - SQL> Tune: {e}")
            return

        self.db_conn.commit()


    def optimize(self):

        try:
            self.db_cur.execute(f"PRAGMA vacuum")
            self.db_cur.execute(f"PRAGMA optimize")
        except Exception as e:
            print(f"<Error! - SQL> Optimize: {e}")
            return

        self.db_conn.commit()


    def table_exist(self, tableName):
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'"
        listOfTables = self.db_cur.execute(query).fetchall()

        if listOfTables == []:
            return False
        else:
            return True


    def empty_table(self, tableName):
        query = f"DELETE FROM {tableName}"

        try:
            self.db_cur.execute(query)
        except Exception as e:
            print(f"<Error! - SQL> Delete: {e}")
            return

        self.db_conn.commit()


    def create_agr_table(self, platforms :str= None):
        query = ""
        query = f"{query} DROP TABLE IF EXISTS [t_agr_all];"
        try:
            self.db_cur.execute(query)
        except Exception as e:
            print(f"<Error! - SQL> Drop Table: {e}")
            return

        query = ""
        query = f"{query} CREATE TABLE [t_agr_all] AS"
        query = f"{query} select * FROM v_agr_all"
        if platforms is not None: where = f" where platform in ({platforms})"
        try:
            self.db_cur.execute(query + where)
        except Exception as e:
            print(f"<Error! - SQL> Create Table: {e}")
            return

        self.db_conn.commit()



    def list_to_db(self, inputList, tableName, emptyBefore :bool = False):

        if not self.table_exist(tableName):
            print(f"<Error! - SQL> Table '{tableName}' not found")
            return
        elif emptyBefore:
            self.empty_table(tableName)

        for row_dict in inputList:

            columns = ", ".join(row_dict.keys())
            placeholders = ":"+", :".join(row_dict.keys())

            query = f"INSERT INTO {tableName} (%s) VALUES (%s)" % (columns, placeholders)

            # transform list value in str
            for key, value in row_dict.items():
                if type(value) is list:
                    row_dict[key] = str(value).strip()

            try:
                self.db_cur.execute(query, row_dict)
            except Exception as e:
                print(f"<Error! - SQL> Insert: {e}")
                return

        self.db_conn.commit()
        print(f"<DONE - SQL> Table '{tableName}' populated")


    def get_v_names(self, tableName, platforms :str= None):

        query = f"SELECT * FROM {tableName} "
        if platforms is not None:
            pla_list = platforms.split(",")
            where = f"WHERE platforms LIKE '%[{pla_list[0]}]%'"

            for i in range(1,len(pla_list)):
                where = f"{where} OR platforms LIKE '%[{pla_list[i]}]%'"


        try:
            return pd.read_sql_query(query + where, self.db_conn)
        except Exception as e:
            print(f"<Error! - SQL> SELECT: {e}")
            return


    def get_v_data(self, tableName, platforms :str= None):

        query = f"SELECT * FROM {tableName} "

        where = f"WHERE platform in ({platforms})"

        try:
            return pd.read_sql_query(query + where, self.db_conn)
        except Exception as e:
            print(f"<Error! - SQL> SELECT: {e}")
            return
