from core import (
    getSimpleList,
    getFileFromTxt,
    getFileRegion,
    prepare_names_df,
    prepare_string,
    searchLocalFuzzy,
    get_names
)

import csv

threadList = []
path_source = r"D:\Temp\JD"

# def createFolder(foldername):
#     if not os.path.exists(subfolder + '/' + foldername):
#         os.makedirs(subfolder + '/' + foldername)

if __name__ == "__main__":
    # for info about platforms ID check INFO\platformsID.txt file
    platforms = "19,58"

    df_names = get_names(platforms)

    # tratto la colonna nomi dove cercare
    df_names['name'] = prepare_names_df(df_names['name'])
    print(df_names)
    #exit()

    #sl = getSimpleList(platforms)

    # carico file da directory
    # files = getFileList(path_source)

    # carico file da txt
    files = getFileFromTxt("SNES.txt")

    prev = ""
    no = 0
    si = 0

    myfile = open("output.csv", "w", newline="", encoding="utf-8-sig")

    # --- HEADER PER ESPORTAZIONE CSV
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL, delimiter=";")
    header = (
        "NOME FILE",
        "STRINGA CERCATA",
        "ID",
        "NOME",
        "PUNTEGGIO DI RICERCA",
        "REGION",
        "DATA",
        "GENERE",
        "PUB",
        "DEV",
    )
    wr.writerow(header)
    # ---

    # scorro la lista contenente i nomi file per cercare un abbinamento utilizzando fuzzy
    for f in files:
        # FORZATURA escludo tutto quello che trovo dopo "("
        gname = f.split("(", 1)

        # estraggo la regione dal nome file
        fregion = getFileRegion(f)

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

        # cerco il file all'interno del lista
        mostaccurate = searchLocalFuzzy(df_names['name'].to_list(), gname, 89)

        if mostaccurate == None:
            out = f, gname, "", "<NOT FOUND>"
            print(out)
            wr.writerow(out)
            no = no + 1
            continue
        else:
            out = f, gname, "", mostaccurate[0], int(mostaccurate[1])
            print(out)
            si = si + 1

            # print(mostaccurate)
            # pgia = getDictFromList(psl,'name',mostaccurate[0])
            # pgir = getDictFromList(pgia,'region',region_db_dict[fregion])
            # if len(pgir) == 0: pgir = getDictFromList(pgia,'region','Other')
            # if len(pgir) == 0: pgir = getDictFromList(pgia,'region','Region Not Set')
            # if len(pgir) == 0: pgir = pgia

            # #print(mostaccurate[0])
            # ginfoID = getElementFromList(pgir,'game_title',mostaccurate[0],'id')

            # ginfo = getDictFromList(gi,'id',ginfoID)[0]

            # if len(ginfo) == 1:
            #      out = f,gname,'','<NOT FOUND>'
            #      print(out)
            #      wr.writerow(out)
            #      no = no + 1
            #      continue
            # else:
            #     try:
            #         id = ginfo['id']
            #         name = ginfo['game_title']
            #         release = ginfo['release_date']
            #         gen = ginfo['genres']
            #         pub = ginfo['publishers']
            #         dev = ginfo['developers']
            #     except:
            #         pass

            #     si = si + 1
            #     out = f,gname,str(id),name,str(mostaccurate[1]),fregion,str(release),str(gen),str(pub),str(dev)
            #     #print(out)

            # --- PER ESPORTAZIONE CSV
            wr.writerow(out)
            # ---

    myfile.close()
    print("----------------")
    print("si", si)
    print("no", no)
    print("tot", si + no)
    print("----------------")
    print("%:", (100 / (si + no)) * si)
    print("----------------")

    # for x in range(len(games)):
    #     genre = str(games[x]['genre'])
    #     genre = genre.split(' / ', 1)[0]
    #     print(genre)
    #     createFolder(genre)
    #     filename = str(games[x]['path']).replace('./','',1)
    #     print(subfolder + '/' + genre + '/' + filename)
    #     shutil.copyfile(source + '/' + filename, subfolder + '/' + genre + '/' + filename)
