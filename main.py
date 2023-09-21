
import os
import sys
import shutil
from igdb.wrapper import IGDBWrapper
import json
from datetime import datetime
import joblib
import csv
from typing import List
import threading
import queue
import time
import re
#from thefuzz import process
from rapidfuzz import process, fuzz, utils

from sentence_transformers import SentenceTransformer, util
import torch


import pandas as pd
import numpy as np
import faiss
from fuzzywuzzy import fuzz
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import AutoTokenizer, AutoModel
import tensorflow as tf
import tensorflow_hub as hub

threadList = []

path_source = r'D:\Temp\JD'
CSVfolder = 'CSV/'
JSONfolder = 'JSON/'
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

class FuzzySemanticSearch:
    def __init__(self, dataset, model_name):

        self.dataset = dataset

        # Path where to save the model
        saved_model_path = "model"

        try:
            self.embed = hub.load(saved_model_path)
        except:
            self.embed = hub.load(model_name)

        # Save TF Hub model to custom folder path
        tf.saved_model.save(self.embed, saved_model_path)
        
        self.vectors = self.get_embedding()
        self.index = faiss.IndexFlatIP(self.vectors.shape[-1])



    def preprocess_text(self, text):
        stop_words = set(stopwords.words('english'))
        tokens = word_tokenize(text)
        tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stop_words]
        return ' '.join(tokens)

    def encode_text(self, text):
        embedding = self.embed([text]).numpy()
        return embedding

    def get_embedding(self):
        embeddings = []
        for text in self.dataset['text']:
            #preprocessed_text = self.preprocess_text(text)
            #embedding = self.encode_text(preprocessed_text)
            embedding = self.encode_text(text)
            embeddings.append(embedding)
        embeddings = np.concatenate(embeddings, axis=0)
        return embeddings

    def build_index(self):
        embeddings = np.array(self.vectors)
        self.index.add(embeddings)

    def search(self, query, k=1, threshold=0):
        preprocessed_query = self.preprocess_text(query)
        embedding = self.encode_text(preprocessed_query)
        distances, indices = self.index.search(embedding.reshape(1, -1), k)
        results = []
        for distance, index in zip(distances[0], indices[0]):
            text = self.dataset.iloc[index]['text']
            score = fuzz.token_sort_ratio(preprocessed_query, self.preprocess_text(text))
            if score >= threshold:
                results.append({'text': text, 'score': score, 'distance': distance})
                out = 'AI '+ results[0]['text'],results[0]['score']

            else:
                out = None
        #results = sorted(results, key=lambda x: (x['distance'], x['score']), reverse=True)[:k]


        return out

# def createFolder(foldername):
#     if not os.path.exists(subfolder + '/' + foldername):
#         os.makedirs(subfolder + '/' + foldername)

def exportListCSV(sourceList,fileName):

    # # try:
    # myfile = open(CSVfolder + fileName, 'w', newline='', encoding="utf-8-sig")
    # wr = csv.writer(myfile, quoting=csv.QUOTE_ALL,delimiter =';')
    # wr.writerow(list(sourceList[0]))
    # for element in sourceList:
    #     # controllo se l'elemento è un dizionario
    #     if type(element) is dict: wr.writerow(element.values())
    #     else: wr.writerow(element)
    #     #wr.writerow(element.values())
    # myfile.close()
    # # except:
    # #     pass

    # optional: compute the fieldnames:
    fieldnames = set()
    for d in sourceList:
        fieldnames.update(d.keys())
    fieldnames = sorted(fieldnames)    # sort the fieldnames...

    # produce the csv file
    with open(CSVfolder + fileName, "w", newline='', encoding="utf-8-sig") as fd:
        wr = csv.DictWriter(fd, fieldnames, quoting=csv.QUOTE_ALL, delimiter =';')
        wr.writeheader()
        wr.writerows(sourceList)

def exportListJSON(sourceList,fileName):
    with open(JSONfolder + fileName, "w") as myfile:
        json.dump(sourceList, myfile)

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

def initTransf():
    # Carica il modello e lo sposta sulla GPU
    device = 'cuda' if torch.cuda.is_available() else 'cpu:0'
    model = SentenceTransformer('stsb-roberta-large')
    modelPath = "model"
    model.save(modelPath)
    model = SentenceTransformer(modelPath)
    model.to(device)

    return model,device

def embTransf(model,device,sourceList,name = None):
    
    if name != None:
        pre = name
        ext = '.emb'
        filename = pre + ext

        try:
            lout = joblib.load(filename)
            #exportListCSV(lout,pre + '.csv')
            return lout
        except:
            lout = []
    else:
        lout = []

    # # Carica il modello e lo sposta sulla GPU
    # device = 'cuda' if torch.cuda.is_available() else 'cpu:0'
    # model = SentenceTransformer('stsb-roberta-large')
    # modelPath = "model"
    # model.save(modelPath)
    # model = SentenceTransformer(modelPath)
    # model.to(device)

    # Calcola l'embedding di ogni testo nella lista
    lout = model.encode(sourceList, convert_to_tensor=True, show_progress_bar=True, device=device)

    if name != None: joblib.dump(lout, filename)

    return lout

def initFuzzSem(list):
    #nltk.download('stopwords')

    #nltk.download('punkt')

    model_name = 'https://tfhub.dev/google/universal-sentence-encoder-large/5'

    dataset = pd.DataFrame({'text': list})

    fuzzy_semantic_search = FuzzySemanticSearch(dataset, model_name)

    fuzzy_semantic_search.build_index()

    return fuzzy_semantic_search



def bestTrasf(emb1,emb2,list2,cutout):

    sim_scores = util.pytorch_cos_sim(emb1, emb2)[0]

    # Trova il testo più simile nella lista 2
    top_idx = torch.argmax(sim_scores)

    sim_score = sim_scores[top_idx]

    score = round(sim_score.item()*100,2)

    if score >= cutout:
        lout = list2[top_idx],'AI ' + str(int(score))
    else:
        lout = None

    return lout


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

def getMultiThread(name,endPoint,fields,where = ''):

    global threadList

    pre = name
    ext = '.sav'
    filename = pre + ext

    try:
        lout = joblib.load(filename)
        #exportListCSV(lout,pre + '.csv')
        return lout
    except:
        lout = []

    threadList = lout.copy()

    print(name + ' - import time> --- start')
    start_time = time.time()

    q = queue.Queue()

    def count(endPoint,where):
        byte_array = wrapper.api_request(endPoint + '/count',where + ';')
        
        # converto da bytes a stringa JSON
        j = byte_array.decode()

        # converto da stringa a lista
        l = json.loads(j)

        return l['count']


    def mainQuery(endPoint,fields,where,offset):
        global threadList

        lout = []
        
        attempts = 0
        maxAttempts = 5

        if len(where) > 0: where = where + '; '

        while attempts < maxAttempts:
            try:
                byte_array = wrapper.api_request(
                        endPoint,
                        #fields + ';' + where +'; offset ' + str(offset) + '; limit 500;'
                        fields + '; ' + where +' offset ' + str(offset) + '; limit 500;'
                    )
                # converto da bytes a stringa JSON
                j = byte_array.decode()

                # converto da stringa a lista
                lout = json.loads(j)

                break

            except Exception as exc:
                attempts += 1
                print('<Error! - attempt: ' + str(attempts) + '/' + str(maxAttempts) + ' > EndPoint: ' + endPoint  , '#',exc)
                time.sleep(1/thread_count)

        if attempts == maxAttempts: 
            print('<FAILED! ' + str(attempts) + ' > EndPoint: ' + endPoint )
            os._exit(1)
            
        perc = round((100 / counted) * offset,2)
        print('                                                                                                       ', end="\r")
        print( name + ' - processed: ' + str(perc) + '%', end="\r")

        threadList.extend(lout)

    threads = []

    
    thread_count = 4 # numero massimo di thread per interrgogare IGDB max 4 al secondo
    min_time = 1 # ritardo in secondi tra le richieste ai thread (in secondi)

    def worker():
        while True:

            endPoint,fields,where,offset = q.get()
            if endPoint is None:
                break

            start_req = time.time()
            mainQuery(endPoint,fields,where,offset)

            # calcolo il ritardo tra le richieste
            if (time.time() - start_req) < min_time: 
                time.sleep(min_time - (time.time() - start_req))

            q.task_done()

    for x in range(0, thread_count):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
        # print('Started: %s' % t)

    
    counted = count(endPoint,where)
    print(name + ' - records: ' + str(counted))
    for i in range(0,int(counted/500) + 1):
        offset = i * 500
        q.put((endPoint,fields,where,offset))
        
    # block until all tasks are done
    q.join()

    # stop workers
    for _ in threads:
        q.put((None,None,None,None))

    for t in threads:
        t.join()

    print(name + ' - import time> --- %s seconds' % (time.time() - start_time))

    lout = threadList[:]

    joblib.dump(lout, filename)

    try: exportListCSV(lout,pre + '.csv')
    except: pass

    return lout

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


    sl = getSimpleList(platform)


    # exit()


    psl = prepareList(sl,'name')
    
    #files = getFileList(path_source)
   
    files = getFileFromTxt('SNES.txt')

    prev = ''
    no = 0
    si = 0

    myfile = open('output.csv', 'w', newline='', encoding="utf-8-sig")

    # --- PER ESPORTAZIONE CSV
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL,delimiter =';')
    header = 'NOME FILE','STRINGA CERCATA','ID','NOME','PUNTEGGIO DI RICERCA','REGION','DATA','GENERE','PUB','DEV'
    wr.writerow(header)
    # ---
    # model, device = initTransf()
    # embDB = embTransf(model, device, [d['name'] for d in psl],'simple' + str(platform))

    fs = initFuzzSem([d['name'] for d in psl])

    for f in files:
        
        gname = f.split('(',1)

        fregion = getFileRegion(f)
        gname = gname[0]
        gname = prepareList(gname)

        id = ''
        name = ''
        release = ''
        gen = []
        pub = []
        dev = []
        
        ginfo = []

        where = [d['name'] for d in psl]

        mostaccurate = searchLocalFuzzy(where,gname,89)


        
        if mostaccurate == None:

        #     embF = embTransf(model, device, [gname])
        #     mostaccurate = bestTrasf(embF ,embDB, [d['name'] for d in sl], 60)
            mostaccurate = fs.search(gname,1,60)

        if mostaccurate == None:

            out = f,gname,'','<NOT FOUND>'
            print(out)
            wr.writerow(out)
            no = no + 1
            continue
        else:
            out = f,gname,'',mostaccurate[0],int(mostaccurate[1])
            #out = f,gname,'',mostaccurate
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
        #break

        


    

    

    
    
    # for x in range(len(games)):
    #     genre = str(games[x]['genre'])
    #     genre = genre.split(' / ', 1)[0]
    #     print(genre)
    #     createFolder(genre)
    #     filename = str(games[x]['path']).replace('./','',1)
    #     print(subfolder + '/' + genre + '/' + filename)
    #     shutil.copyfile(source + '/' + filename, subfolder + '/' + genre + '/' + filename)

        