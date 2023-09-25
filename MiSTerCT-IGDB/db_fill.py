from igdb_api_class import IGDBAPI
from db_class import DATABASE

def fill_db(platform_filter = 'All'):

    platforms = IGDBAPI("platforms","platforms","fields *").retrieve_data()
    genres = IGDBAPI("genres", "genres", "fields *").retrieve_data()
    companies = IGDBAPI("companies", "companies", "fields *").retrieve_data()
    involved_companies = IGDBAPI(
        "involved_companies", "involved_companies", "fields *"
    ).retrieve_data()
    regions = IGDBAPI('regions','regions','fields *').retrieve_data()
    release_dates = IGDBAPI('release_dates','release_dates','fields *').retrieve_data()
    alternative_names = IGDBAPI('alternative_names','alternative_names','fields *').retrieve_data()

    if platform_filter == 'All':
        games = IGDBAPI('games','games','fields *').retrieve_data()
        
    else:
        games = IGDBAPI(
            f"games_{platform_filter}",
            "games",
            "fields *",
            f"where platforms = ({platform_filter})",
        ).retrieve_data()

    with DATABASE("IGDB.db") as db:
        db.list_to_db(platforms, "platforms",True)
        db.list_to_db(genres, "genres",True)
        db.list_to_db(companies, "companies",True)
        db.list_to_db(involved_companies, "involved_companies",True)
        db.list_to_db(regions, "regions",True)
        db.list_to_db(release_dates, "release_dates",True)
        db.list_to_db(games, "games",True)
        db.list_to_db(alternative_names, "alternative_names",True)

if __name__ == "__main__":
    platforms = "5,4,18,19,22,29,30,32,33,35,57,58,59,60,61,62,63,64,66,55,56,58,78,79,80,84,86,88,99,119,120,136,150,160"
    fill_db(platforms)