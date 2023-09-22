from core import (
    getSimpleList,
    prepareList,
    getFileFromTxt,
    getFileRegion,
    prepareString,
    searchLocalFuzzy,
)

threadList = []
path_source = r"D:\Temp\JD"
DBfolder = "DB/"


# def createFolder(foldername):
#     if not os.path.exists(subfolder + '/' + foldername):
#         os.makedirs(subfolder + '/' + foldername)

if __name__ == "__main__":
    # 4 = N65
    # 19 = SNES
    # 58 = S Famicom
    platform = "19,58"

    # --------------------------------------------------
    # DA ABILITARE PER SCARICARE LOCALMENTE LE VARIE TABELLE TRAMITE API, VERRANNO SALVATE COME .CSV E .SAV (LISTA IN FORMATO BINARIO)
    # la funzione "getMultiThread" richiede:
    #       name = nome della lista creata
    #       endPoint = nome tabella IGDB (https://api-docs.igdb.com/#endpoints)
    #       fields = colonne richieste
    #       where = condizione di where per la query
    # --------------------------------------------------

    # getMultiThread('game_localizations','game_localizations','fields *')
    # getMultiThread('regions','regions','fields *')

    # getMultiThread('release_dates','release_dates','fields *')
    # getMultiThread('release_dates_' + str(platform),'release_dates','fields *','where platform = (' + str(platform) + ')')

    # getMultiThread('companies','companies','fields *')
    # getMultiThread('involved_companies','involved_companies','fields *')
    # getMultiThread('platforms','platforms','fields *')

    # getMultiThread('genres','genres','fields *')
    # getMultiThread('games','games','fields *')

    # getMultiThread('games_' + str(platform),'games','fields *','where platforms = (' + str(platform) + ')')

    # getMultiThread('alternative_names','alternative_names','fields *')

    # exit()

    # --------------------------------------------------

    # preparo una lista semplificata con le informazioni minime per provare l'abbinamento
    # al suo interno utilizza gia la funzione "getMultiThread"
    # le tabelle scaricate saranno:
    #   genres
    #   companies
    #   involved_companies
    #   games_# (dove # = id piattaforma)
    #   alternative_names
    sl = getSimpleList(platform)

    # tratto la lista di testi dove cercare
    psl = prepareList(sl, "name")

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
        gname = prepareString(gname)

        id = ""
        name = ""
        release = ""
        gen = []
        pub = []
        dev = []

        ginfo = []

        where = [d["name"] for d in psl]

        # cerco il file all'interno del lista
        mostaccurate = searchLocalFuzzy(where, gname, 89)

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
