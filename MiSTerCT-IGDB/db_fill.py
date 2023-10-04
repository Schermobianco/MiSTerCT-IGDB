import logging
import os.path
from igdb_api_class import IGDBAPI
from db_class import DATABASE
from dotenv import load_dotenv
from pathlib import Path
import shutil

# load the needed env vars.
# order is: os env first, .env file second. (see https://pypi.org/project/python-dotenv/)
load_dotenv(override=False)

DATABASE_FILE_NAME = "IGDB_megafull_test.db"
LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger("db_fill")

# get current working directory
path = os.path.join(os.getcwd(), "DB")

BASE_DIR = path

def file_exist(path):
    check_file = os.path.isfile(path)
    return check_file

def copy_file(source, destination):
    ## use this lib for better cross-os compatibility
    shutil.copy2(source, destination)

def fill_db(platform_filter = "All"):
    os.makedirs(os.path.join(os.getcwd(), '.tmp'), exist_ok=True)
    db_path = os.path.join(BASE_DIR, DATABASE_FILE_NAME)
    db_path_empty = 0 # init 0, needed later to control the logs
    if not file_exist(db_path):
        logger.info(f'db not found, creating new empty db....')
        db_path_empty = DATABASE.create_empty_db()
        logger.info(f'start new db in {db_path} (from empty {db_path_empty})');
        if file_exist(db_path_empty):
            copy_file(db_path_empty, db_path)
            logger.info(f'copied emty into {db_path}.');
        else:
            logger.error(f"<Error! - FILL DB> Empty DB is missing: {db_path_empty}")
            return
    #  request from IGDB the tables
    platforms = IGDBAPI("platforms","platforms","fields *").retrieve_data()
    genres = IGDBAPI("genres", "genres", "fields *").retrieve_data()
    companies = IGDBAPI("companies", "companies", "fields *").retrieve_data()
    involved_companies = IGDBAPI("involved_companies", "involved_companies", "fields *").retrieve_data()
    regions = IGDBAPI('regions','regions','fields *').retrieve_data()
    release_dates = IGDBAPI('release_dates','release_dates','fields *').retrieve_data()
    alternative_names = IGDBAPI('alternative_names','alternative_names','fields *').retrieve_data()
    franchises = IGDBAPI('franchises','franchises','fields *').retrieve_data()
    game_modes = IGDBAPI('game_modes','game_modes','fields *').retrieve_data()
    player_perspectives = IGDBAPI('player_perspectives','player_perspectives','fields *').retrieve_data()
    collections = IGDBAPI('collections','collections','fields *').retrieve_data()
    age_ratings = IGDBAPI('age_ratings','age_ratings','fields *').retrieve_data()
    game_localizations = IGDBAPI('game_localizations','game_localizations','fields *').retrieve_data()

    #  request from IGDB the tables (platforms filtered)
    if platform_filter == 'All':
        games = IGDBAPI('games','games','fields *').retrieve_data()
        game_engines = IGDBAPI('game_engines','game_engines','fields *').retrieve_data()

    else:
        games = IGDBAPI(
            f"games_{platform_filter}",
            "games",
            "fields *",
            f"where platforms = ({platform_filter})",
        ).retrieve_data()
        game_engines = IGDBAPI(
            f"game_engines_{platform_filter}",
            "game_engines",
            "fields *",
            f"where platforms = ({platform_filter})",
        ).retrieve_data()

    with DATABASE(db_path, '') as db:
        # tune db
        db.tune()

        # populte the tables into DB
        empty_table = True
        db.list_to_db(platforms, "platforms",empty_table)
        db.list_to_db(genres, "genres",empty_table)
        db.list_to_db(companies, "companies",empty_table)
        db.list_to_db(involved_companies, "involved_companies",empty_table)
        db.list_to_db(regions, "regions",empty_table)
        db.list_to_db(release_dates, "release_dates",empty_table)
        db.list_to_db(games, "games",empty_table)
        db.list_to_db(alternative_names, "alternative_names",empty_table)
        db.list_to_db(franchises, "franchises",empty_table)
        db.list_to_db(game_engines, "game_engines",empty_table)
        db.list_to_db(game_modes, "game_modes",empty_table)
        db.list_to_db(player_perspectives, "player_perspectives",empty_table)
        db.list_to_db(collections, "collections",empty_table)
        db.list_to_db(age_ratings, "age_ratings",empty_table)
        db.list_to_db(game_localizations, "game_localizations",empty_table)

        # create agr table, needed?
        # db.create_agr_table(platform_filter)

        # optimize db
        db.optimize()

    logger.info(f'db populated: {db_path}');
    if db_path_empty != 0:
        logger.info(f'can safely remove {db_path_empty}');
    logger.info(f'bye.');

if __name__ == "__main__":
    platforms = "4,7,18,19,22,29,30,32,33,35,57,58,59,60,61,62,64,66,67,68,70,78,79,80,84,86,88,99,119,120,136,150,160"
    fill_db(platforms)
