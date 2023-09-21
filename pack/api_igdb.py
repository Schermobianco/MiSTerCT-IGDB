from igdb.wrapper import IGDBWrapper
import json
import joblib
import threading
import queue
import time
import os

from pack.fun import *

wrapper = IGDBWrapper("ltoj7yg0pb1t32gxtvph876ojyp12d", "qb3lm8ls99u2kux3se4z4wk3501pc8")


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