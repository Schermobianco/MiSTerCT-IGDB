
import os
import sys
import shutil

from pack.fun import *
from pack.api_igdb import *

from datetime import datetime
import joblib

from typing import List

import time
import re
#from thefuzz import process
from rapidfuzz import process, fuzz, utils

threadList = []

path_source = r'D:\Temp\JD'
DBfolder = 'DB/'

replacements_dict = {
    ' a ':' ',
    ' the ':' ',
    'the ':' ',
    '!': ' ',
    '?': ' ',
    '&': ' ',
    '@': ' ',
    '-': ' ',
    '.': '',
    ',': '',
    ';': '',
    ':': '',
    '*': '',
    #"'s ": ' ',
    "'": ' ',
    '/': ' ',
    '|': ' '
}

region_dict = {
    '(usa)': 'U',
    '(us)': 'U',
    '(u)': 'U',
    '(europe)': 'E',
    '(euro)': 'E',
    '(eu)': 'E',
    '(e)': 'E',
    '(japan)': 'J',
    '(jp)': 'J',
    '(j)': 'J',
    '[usa]': 'U',
    '[us]': 'U',
    '[u]': 'U',
    '[europe]': 'E',
    '[euro]': 'E',
    '[eu]': 'E',
    '[e]': 'E',
    '[japan]': 'J',
    '[j]': 'J',
    '[jp]': 'J',
    '{usa}': 'U',
    '{us}': 'U',
    '{u}': 'U',
    '{europe}': 'E',
    '{euro}': 'E',
    '{eu}': 'E',
    '{e}': 'E',
    '{japan}': 'J',
    '{j}': 'J',
    '{jp}': 'J'
}

regionEnum_dict = {
    '1':'europe',
    '2':'north_america',
    '3':'australia',
    '4':'new_zealand',
    '5':'japan',
    '6':'china',
    '7':'asia',
    '8':'worldwide',
    '9':'korea',
    '10':'brazil'
}

exclusion = '(pirate)','(proto)'

wrapper = IGDBWrapper("ltoj7yg0pb1t32gxtvph876ojyp12d", "qb3lm8ls99u2kux3se4z4wk3501pc8")

# def createFolder(foldername):
#     if not os.path.exists(subfolder + '/' + foldername):
#         os.makedirs(subfolder + '/' + foldername)

def prepareList(sourceList,keyname = None):
    
    for e in sourceList:
        if type(sourceList[0]) is dict:
            for key, value in replacements_dict.items():
                if e[keyname] == None: e[keyname] = ''
                if key in e[keyname]:
                    
                    # se dizionario
                    e[keyname] = e[keyname].replace(key, value)

            re.sub("[\(\[].*?[\)\]]", "", e[keyname])
            e[keyname] = re.sub('\s{2,}', ' ', e[keyname])
            e[keyname] = e[keyname].strip()
            e[keyname] = e[keyname].lower()

            # rimpiazza le lettere multiple consecutive
            #e[keyname] = re.sub(r"(.)\1+", r"\1", e[keyname])
                    
        else:
            for key, value in replacements_dict.items():
                if e == None: e = ''
                if key in e:
                    
                    # se dizionario
                    e = e.replace(key, value)

            re.sub("[\(\[].*?[\)\]]", "", e)
            e = re.sub('\s{2,}', ' ', e)
            e = e.strip()
            e = e.lower()

            # rimpiazza le lettere multiple consecutive
            #e = re.sub(r"(.)\1+", r"\1", e)

    return sourceList

def prepareString(source):
    source = source.lower()
    for key, value in replacements_dict.items():
        if key in source:
            source = source.replace(key, value)
            
    source = re.sub('\s{2,}', ' ', source)
    source = source.strip()
    
    return source

def searchLocalFuzzy(sourceList, search: str, cutoff) -> str:

        if len(sourceList) == 0:
            return False

        out = process.extractOne(search, sourceList, score_cutoff=cutoff)

        return out


def getElementFromList(list,tosearch,value,toget):
    return [d[toget] for d in list if d[tosearch] == value][0]

def getDictFromList(list,tosearch,value):
    return [d for d in list if d[tosearch] == value]

def getFileList(dir_path):
    # directory/folder path
    

    # list to store files
    res = []

    # Iterate directory
    for file_path in os.listdir(dir_path):
        # check if current file_path is a file
        if os.path.isfile(os.path.join(dir_path, file_path)):
            # add filename to list
            res.append(file_path)
    return res

def getFileFromTxt(fileName):

    # Using readlines()
    myfile = open(fileName, 'r')
    Lines = myfile.readlines()
    
    count = 0
    out = []
    # Strips the newline character
    for line in Lines:
        count += 1
        out.append(line.strip())

    return out

def getFileRegion(fileName: str):
    fileName = fileName.lower()
    for key, value in region_dict.items():
        if key in fileName:
            return value
    
    return None

def getSimpleList(platformID):
    pre = 'simple_' + str(platformID)
    ext = '.sav'
    filename = pre + ext

    try:
        sl = joblib.load(filename)
        exportListCSV(sl,pre + '.csv')
        return sl
    except:
        sl = []

    lout = []

    gn = getMultiThread('genres','genres','fields *')
    c = getMultiThread('companies','companies','fields *')
    ic = getMultiThread('involved_companies','involved_companies','fields *')
    g = getMultiThread('games_' + str(platformID),'games','fields *','where platforms = (' + str(platformID) + ')')
    an = getMultiThread('alternative_names','alternative_names','fields *')

    for e in g:
        print(e['name'])
        id = e['id']
        name = e['name']
        release = ''
        
        gen = []
        try:
            for i in e['genres']:
                gname = getElementFromList(gn,'id',i,'name')
                gen.append(gname)
        except:
            pass

        dev = []
        pub = []
        try:
            release = datetime.utcfromtimestamp(e['first_release_date']).strftime('%Y-%m-%d')
            for i in e['involved_companies']:
                cid = getElementFromList(ic,'id',i,'company')
                cname = getElementFromList(c,'id',cid,'name')
                fdev = getElementFromList(ic,'id',i,'developer')
                fpub = getElementFromList(ic,'id',i,'publisher')

                if fdev:
                    dev.append(cname)
                if fpub:
                    pub.append(cname)
        except:
            pass

        lout.append({'id':id,'name':name,'rel':release,'gen':gen,'pub':pub,'dev':dev})

        altName = []
        try:
            for i in e['alternative_names']:
                gname = getElementFromList(an,'id',i,'name')
                lout.append({'id':id,'name':gname,'rel':release,'gen':gen,'pub':pub,'dev':dev})
        except:
            pass
            

    # ordino la luista per id
    lout = sorted(lout, key=lambda d: d['id']) 

    joblib.dump(lout, filename)

    try: exportListCSV(lout,pre + '.csv')
    except: pass

    return lout



if __name__ == "__main__":

    # 4 = N65
    # 19 = SNES
    # 58 = S Famicom
    platform = '19,58'

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
    psl = prepareList(sl,'name')
    
    # carico file da directory
    #files = getFileList(path_source)
   
    # carico file da txt
    files = getFileFromTxt('SNES.txt')

    prev = ''
    no = 0
    si = 0

    myfile = open('output.csv', 'w', newline='', encoding="utf-8-sig")

    # --- HEADER PER ESPORTAZIONE CSV
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL,delimiter =';')
    header = 'NOME FILE','STRINGA CERCATA','ID','NOME','PUNTEGGIO DI RICERCA','REGION','DATA','GENERE','PUB','DEV'
    wr.writerow(header)
    # ---


    # scorro la lista contenente i nomi file per cercare un abbinamento utilizzando fuzzy
    for f in files:
        
        # FORZATURA escludo tutto quello che trovo dopo "("
        gname = f.split('(',1)

        # estraggo la regione dal nome file
        fregion = getFileRegion(f)

        gname = gname[0]

        # tratto la stringa da cercare
        gname = prepareString(gname)

        id = ''
        name = ''
        release = ''
        gen = []
        pub = []
        dev = []
        
        ginfo = []

        where = [d['name'] for d in psl]

        # cerco il file all'interno del lista
        mostaccurate = searchLocalFuzzy(where,gname,89)

        if mostaccurate == None:

            out = f,gname,'','<NOT FOUND>'
            print(out)
            wr.writerow(out)
            no = no + 1
            continue
        else:
            out = f,gname,'',mostaccurate[0],int(mostaccurate[1])
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
    print('----------------')
    print('si',si)
    print('no',no)
    print('tot',si+no)
    print('----------------')
    print('%:',(100/(si+no))*si)
    print('----------------')

        


    

    

    
    
    # for x in range(len(games)):
    #     genre = str(games[x]['genre'])
    #     genre = genre.split(' / ', 1)[0]
    #     print(genre)
    #     createFolder(genre)
    #     filename = str(games[x]['path']).replace('./','',1)
    #     print(subfolder + '/' + genre + '/' + filename)
    #     shutil.copyfile(source + '/' + filename, subfolder + '/' + genre + '/' + filename)

        