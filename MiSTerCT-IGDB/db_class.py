import sqlite3
import pandas as pd
import os.path

# get current working directory
path = os.getcwd()

path = f"{path}\DB"
BASE_DIR = path

class DATABASE():
    def __init__(self, db_name, db_path = BASE_DIR):
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
        except Exception as e:
            print(f"<Error! - SQL> Connection: {e}")
            return

        db_cur = db_conn.cursor()
        return db_conn, db_cur
    
    def close(self):
        self.db_conn.close()

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

            # trasform list value in str 
            for key, value in row_dict.items():
                if type(value) is list: 
                    row_dict[key] = str(value).replace(", ","][")

            try:
                self.db_cur.execute(query, row_dict)
            except Exception as e:
                print(f"<Error! - SQL> Insert: {e}")
                return

        self.db_conn.commit()
        print(f"<DONE - SQL> Table '{tableName}' populated")

    def get_v_complete_names(self, platforms :str= None):

        query = f"SELECT * FROM v_complete_names "
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