from igdb.wrapper import IGDBWrapper
from twitch_token import get_access_token
import json
import joblib
import threading
import queue
import time
import os

from file_export import export_list_to_csv

THREAD_COUNT = 4  # numero massimo di thread per interrgogare IGDB max 4 al secondo
MIN_TIME = 1  # ritardo in secondi tra le richieste ai thread (in secondi)


def createIGDBWrapper():
    access_token = get_access_token()
    client_id = os.environ.get("TWITCH_CLIENT_ID")
    wrapper = IGDBWrapper(client_id, access_token)
    return wrapper


def getMultiThread(name, endPoint, fields, where=""):
    wrapper = createIGDBWrapper()

    global threadList

    pre = name
    ext = ".sav"
    filename = pre + ext

    try:
        lout = joblib.load(filename)
        # exportListCSV(lout,pre + '.csv')
        return lout
    except Exception as exc:
        lout = []

    threadList = lout.copy()

    print(name + " - import time> --- start")
    start_time = time.time()

    q = queue.Queue()

    def count_records(endpoint, where_clause):
        byte_array = wrapper.api_request(f"{endpoint}/count", f"{where_clause};")
        json_string = byte_array.decode()
        json_list = json.loads(json_string)
        return json_list["count"]

    def mainQuery(endPoint, fields, where, offset):
        global threadList

        lout = []

        attempts = 0
        maxAttempts = 5

        if len(where) > 0:
            where = where + "; "

        while attempts < maxAttempts:
            try:
                byte_array = wrapper.api_request(
                    endPoint,
                    # fields + ';' + where +'; offset ' + str(offset) + '; limit 500;'
                    fields + "; " + where + " offset " + str(offset) + "; limit 500;",
                )
                # converto da bytes a stringa JSON
                j = byte_array.decode()

                # converto da stringa a lista
                lout = json.loads(j)

                break

            except Exception as exc:
                attempts += 1
                print(
                    "<Error! - attempt: "
                    + str(attempts)
                    + "/"
                    + str(maxAttempts)
                    + " > EndPoint: "
                    + endPoint,
                    "#",
                    exc,
                )
                time.sleep(1 / THREAD_COUNT)

        if attempts == maxAttempts:
            print("<FAILED! " + str(attempts) + " > EndPoint: " + endPoint)
            os._exit(1)

        perc = round((100 / counted) * offset, 2)
        print(
            "                                                                                                       ",
            end="\r",
        )
        print(name + " - processed: " + str(perc) + "%", end="\r")

        threadList.extend(lout)

    threads = []

    def worker():
        while True:
            endPoint, fields, where, offset = q.get()
            if endPoint is None:
                break

            start_req = time.time()
            mainQuery(endPoint, fields, where, offset)

            # calcolo il ritardo tra le richieste
            if (time.time() - start_req) < MIN_TIME:
                time.sleep(MIN_TIME - (time.time() - start_req))

            q.task_done()

    for x in range(0, THREAD_COUNT):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
        # print('Started: %s' % t)

    counted = count_records(endPoint, where)
    print(name + " - records: " + str(counted))
    for i in range(0, int(counted / 500) + 1):
        offset = i * 500
        q.put((endPoint, fields, where, offset))

    # block until all tasks are done
    q.join()

    # stop workers
    for _ in threads:
        q.put((None, None, None, None))

    for t in threads:
        t.join()

    print(name + " - import time> --- %s seconds" % (time.time() - start_time))

    lout = threadList[:]

    joblib.dump(lout, filename)

    try:
        export_list_to_csv(lout, pre + ".csv")
    except Exception:
        pass

    return lout
