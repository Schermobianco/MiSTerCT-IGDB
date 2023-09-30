from core import (
    get_files_from_txt,
    get_file_region,
    get_region_name,
    prepare_names_df,
    prepare_string,
    fuzzy_search,
    get_db_names,
    get_db_data
)

import csv # -- TO REMOVE

threadList = []
path_source = r"Sample Sources\\"

if __name__ == "__main__":
    # for info about platforms ID check INFO\platformsID.txt file
    platforms = "19,58"

    df_data = get_db_data('v_agr_all',platforms)
    df_data = df_data.set_index('id')


    df_names_off = get_db_names('v_official_names_regions',platforms)
    df_names_off = df_names_off.set_index('id')

    df_names_alt = get_db_names('v_alternative_names_regions',platforms)
    df_names_alt = df_names_alt.set_index('id')

    # tratto la colonna nomi dove cercare
    df_names_off['name'] = prepare_names_df(df_names_off['name'])
    df_names_alt['name'] = prepare_names_df(df_names_alt['name'])

    # fronm directory
    # files = get_files_from_dir(path_source)

    # from txt file
    files = get_files_from_txt(f"{path_source}SNES.txt")

    prev = ""
    not_found = 0
    found = 0

    myfile = open("output.csv", "w", newline="", encoding="utf-8-sig")

    # --- HEADER CSV -- TO REMOVE
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=";")
    header = (
        "NOME FILE",
        "STRINGA CERCATA",
        "ID",
        "NOME",
        "PUNTEGGIO DI RICERCA",
        "REGION FROM FILE",
        "REGION FROM DB",
        "DATA",
        "GENERE",
        "PUB",
        "DEV",
    )
    wr.writerow(header)
    # ---

    # loop in files names list using with fuzzy search to match the game
    for f in files:
        # FORCING text exclusion after "("
        gname = f.split("(", 1)

        # reg extraction from file name
        fregion = get_file_region(f)

        gname = gname[0]

        # tratto la stringa da cercare
        gname = prepare_string(gname)

        id = ""
        name = ""
        release = ""
        gen = []
        pub = []
        dev = []

        ginfo = []

        mostaccurate = None

        if fregion == None: 
            # search game name inside official name df WITHOUT REGION
            mostaccurate = fuzzy_search(df_names_off['name'], gname, 89)
        else: 
            # search game name inside official name df WITH REGION
            mostaccurate = fuzzy_search(df_names_off.loc[df_names_off['region'] == int(fregion)]['name'], gname, 89)
            # search game name inside alternative name df WITH REGION
            if mostaccurate == None: mostaccurate = fuzzy_search(df_names_alt.loc[df_names_alt['region'] == int(fregion)]['name'], gname, 89)

        # search game name inside official name df WITHOUT REGION
        if mostaccurate == None: mostaccurate = fuzzy_search(df_names_off['name'], gname, 89)
        # search game name inside alternative name df WITHOUT REGION
        if mostaccurate == None: mostaccurate = fuzzy_search(df_names_alt['name'], gname, 89)
        
        if mostaccurate == None:
            out = f, gname, "", "<NOT FOUND>"
            print(out)
            wr.writerow(out)
            not_found += 1
            continue
        else:
            # mostaccurate[0] = text found
            # mostaccurate[1] = score
            # mostaccurate[2] = game id 
            #out = f, gname, mostaccurate[2], mostaccurate[0], int(mostaccurate[1]), get_region_name(fregion), 
            out = f, gname, mostaccurate[2], mostaccurate[0], int(mostaccurate[1]), get_region_name(fregion)
            #df_data.iloc[mostaccurate[2]]['name'], 
            #df_data.loc[(df_data['id'] == mostaccurate[2]) & (df_data['B'] == 'c')]['name'], 
             
            
            # df_data.iloc[int(mostaccurate[2])]['region_name'], 
            # df_data.iloc[mostaccurate[2]]['date'], 
            # df_data.iloc[mostaccurate[2]]['genres_name'], 
            # df_data.iloc[mostaccurate[2]]['publishers_name'], 
            # df_data.iloc[mostaccurate[2]]['developers_name']
            print(out)
            found += 1


            # --- EXPORT CSV -- TO REMOVE
            wr.writerow(out)
            # ---

    myfile.close()
    print("----------------")
    print("FOUND", found)
    print("NOT FOUND", not_found)
    print("TOT", found + not_found)
    print("----------------")
    print("%:", (100 / (found + not_found)) * found)
    print("----------------")

    # for x in range(len(games)):
    #     genre = str(games[x]['genre'])
    #     genre = genre.split(' / ', 1)[0]
    #     print(genre)
    #     createFolder(genre)
    #     filename = str(games[x]['path']).replace('./','',1)
    #     print(subfolder + '/' + genre + '/' + filename)
    #     shutil.copyfile(source + '/' + filename, subfolder + '/' + genre + '/' + filename)
