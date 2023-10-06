# import sqlite3
import datetime
from pathlib import Path
from dotenv import load_dotenv
import sqlean as sqlite3
import pandas as pd
import os.path
import logging

# load the needed env vars.
# order is: os env first, .env file second. (see https://pypi.org/project/python-dotenv/)
load_dotenv(override=False)
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger("db_class")

# get current working directory
BASE_DIR = os.path.join(os.getcwd(), "DB")
SCHEMA_FILE_PATH = os.path.join(BASE_DIR, "schema", "schema.sql")
DB_DATA_FILE_PATH = os.path.join(BASE_DIR, "schema", "base-data.sql")

"""
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
"""


class DATABASE:
    def __init__(self, db_name, db_path=BASE_DIR):
        logger.info(f"<Info - SQL> SQLite v.{sqlite3.sqlite_version}")
        self.db_name = db_name
        self.db_path = os.path.join(db_path, db_name)
        self.db_conn, self.db_cur = self.__connect()
        if self.test_connection():
            logger.debug("db init: db ok")
            return
        else:
            raise ValueError(f"connection failed to tb {db_name} in {db_path}")

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
            logger.debug(f"<DATABASE> connected to {self.db_path}")
            # this forces the client to load additional extensions avaible,
            # useful for multi os support
            db_conn.enable_load_extension(True)
        except Exception as e:
            logger.error(f"<Error! - SQL> Connection: {e}", e)
            return

        db_cur = db_conn.cursor()
        return db_conn, db_cur

    def close(self):
        self.db_conn.close()

    def tune(self):
        try:
            self.db_cur.execute(f"PRAGMA synchronous = NORMAL")  # Synchronous Commit
            self.db_cur.execute(f"PRAGMA cache_size = -4000")  # Max memory cache size
            self.db_cur.execute(
                f"PRAGMA temp_store = MEMORY"
            )  # Temporary files location
            self.db_cur.execute(
                f"PRAGMA mmap_size = 30000000000"
            )  # Enable memory mapping
            self.db_cur.execute(f"PRAGMA journal_mode = WAL")  # Journal Mode
        except Exception as e:
            logger.error(f"<Error! - SQL> Tune: {e}")
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
        query = (
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{tableName}'"
        )
        listOfTables = self.db_cur.execute(query).fetchall()

        if listOfTables == []:
            logger.debug(f"table_exist listOfTables: {self.db_name} - {listOfTables}")
            return False
        else:
            logger.debug("table_exist table_exist: all table ok")
            return True

    def empty_table(self, tableName):
        query = f"DELETE FROM {tableName}"

        try:
            self.db_cur.execute(query)
        except Exception as e:
            logger.error(f"empty_table: cannot empty table '{tableName}'", e)
            return

        self.db_conn.commit()

    def create_agr_table(self, platforms: str = None):
        query = f"{query} DROP TABLE IF EXISTS [t_agr_all];"
        try:
            self.db_cur.execute(query)
        except Exception as e:
            print(f"<Error! - SQL> Drop Table: {e}")
            return

        query = ""
        query = f"{query} CREATE TABLE IF NOT EXISTS [t_agr_all] AS"
        query = f"{query} select * FROM v_agr_all"
        if platforms is not None:
            where = f" where platform in ({platforms})"
        try:
            self.db_cur.execute(query + where)
        except Exception as e:
            print(f"<Error! - SQL> Create Table: {e}")
            return

        self.db_conn.commit()

    def create_selected_platforms_table(self, platforms: str = None):
        table_name = "platforms#selected"
        if platforms is not None:
            where = f"WHERE p.id in ({platforms})"

        queryscript = f"""
DROP VIEW IF EXISTS '{table_name}';
CREATE VIEW IF NOT EXISTS '{table_name}' AS
SELECT id, abbreviation FROM platforms as p {where};
"""
        try:
            self.db_cur.executescript(queryscript)
        except Exception as e:
            print(f"<Error! - SQL> Create Table: {e}")
            return

        self.db_conn.commit()

    def list_to_db(self, inputList, tableName, emptyBefore: bool = False):
        if not self.table_exist(tableName):
            logger.error(f"<Error! - SQL> Table '{tableName}' not found")
            return
        elif emptyBefore:
            self.empty_table(tableName)

        for row_dict in inputList:
            columns = ", ".join(row_dict.keys())
            placeholders = ":" + ", :".join(row_dict.keys())

            query = f"INSERT INTO {tableName} (%s) VALUES (%s)" % (
                columns,
                placeholders,
            )

            # transform list value in str
            for key, value in row_dict.items():
                if type(value) is list:
                    row_dict[key] = str(value).strip()

            try:
                self.db_cur.execute(query, row_dict)
            except Exception as e:
                logger.error(f"<Error! - SQL> Insert: {e}")
                return

        self.db_conn.commit()
        logger.info(f"<DONE - SQL> Table '{tableName}' populated")

    def get_v_names(self, tableName, platforms: str = None):
        query = f"SELECT * FROM {tableName} "
        if platforms is not None:
            pla_list = platforms.split(",")
            where = f"WHERE platforms LIKE '%[{pla_list[0]}]%'"

            for i in range(1, len(pla_list)):
                where = f"{where} OR platforms LIKE '%[{pla_list[i]}]%'"

        try:
            return pd.read_sql_query(query + where, self.db_conn)
        except Exception as e:
            logger.error(f"<Error! - SQL> get_v_names SELECT: {tableName}", e)
            return

    def get_v_data(self, tableName, platforms: str = None):
        query = f"SELECT * FROM {tableName} "

        where = f"WHERE platform in ({platforms})"

        try:
            return pd.read_sql_query(query + where, self.db_conn)
        except Exception as e:
            logger.error(
                f"<Error! - SQL> get_v_data SELECT: {tableName} in platforms", e
            )
            return

    def test_connection(self):
        try:
            self.db_cur.execute(f"SELECT COUNT(*) FROM sqlite_temp_master;")
            logger.debug(f"testing db ok")
            return True
        except Exception as error:
            logger.error("cannot connect to db", error)
            return False

    @staticmethod
    def create_empty_db(
        newdbname=f"temp-db-file-{datetime.datetime.now().timestamp()}.db",
    ):
        # uses the schema.sql to create a new empty database
        os.makedirs(os.path.join(os.getcwd(), ".tmp"), exist_ok=True)
        db_path = os.path.join(os.getcwd(), ".tmp", newdbname)
        try:
            schema = Path(SCHEMA_FILE_PATH).read_text()
            dbdata = Path(DB_DATA_FILE_PATH).read_text()

            db_conn = sqlite3.connect(db_path)
            db_conn.enable_load_extension(True)

            cur = db_conn.cursor()
            cur.executescript(schema)
            db_conn.commit()

            cur.executescript(dbdata)
            db_conn.commit()

            db_conn.close()
            print(f"created: {db_path}")
            return db_path
        except Exception as e:
            raise f"unable to create db {db_path} with error {e}"
