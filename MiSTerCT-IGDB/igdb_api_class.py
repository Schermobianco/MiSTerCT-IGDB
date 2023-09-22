from igdb.wrapper import IGDBWrapper
from twitch_token import get_access_token
import joblib
import threading
import queue
import time
import json
import os

from file_export import export_list_to_csv

THREAD_COUNT = 4  # numero massimo di thread per interrgogare IGDB max 4 al secondo
MIN_TIME = 1  # ritardo in secondi tra le richieste ai thread (in secondi)


def createIGDBWrapper():
    access_token = get_access_token()
    client_id = os.environ.get("TWITCH_CLIENT_ID")
    wrapper = IGDBWrapper(client_id, access_token)
    return wrapper


class IGDBAPI:
    def __init__(self, name, endPoint, fields, where=""):
        self.name = name
        self.endPoint = endPoint
        self.fields = fields
        self.where = where
        self.wrapper = createIGDBWrapper()
        self.threadList = []
        self.filename = f"{name}.sav"
        self.counted = 0

    def load_data(self):
        try:
            self.threadList = joblib.load(self.filename)
            return self.threadList
        except Exception:
            self.threadList = []
            return self.threadList

    def count_records(self):
        byte_array = self.wrapper.api_request(f"{self.endPoint}/count", f"{self.where};")
        json_string = byte_array.decode()
        json_list = json.loads(json_string)
        self.counted = json_list["count"]
        return self.counted

    def main_query(self, offset):
        lout = []

        attempts = 0
        maxAttempts = 5

        if len(self.where) > 0:
            where = self.where + "; "
        else:
            where = ""

        while attempts < maxAttempts:
            try:
                byte_array = self.wrapper.api_request(
                    self.endPoint,
                    self.fields + "; " + where + " offset " + str(offset) + "; limit 500;",
                )
                j = byte_array.decode()
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
                    + self.endPoint,
                    "#",
                    exc,
                )
                time.sleep(1 / THREAD_COUNT)

        if attempts == maxAttempts:
            print("<FAILED! " + str(attempts) + " > EndPoint: " + self.endPoint)
            os._exit(1)

        perc = round((100 / self.counted) * offset, 2)
        print(
            "                                                                                                       ",
            end="\r",
        )
        print(self.name + " - processed: " + str(perc) + "%", end="\r")

        self.threadList.extend(lout)

    def worker(self, q):
        while True:
            offset = q.get()
            if offset is None:
                break

            start_req = time.time()
            self.main_query(offset)

            if (time.time() - start_req) < MIN_TIME:
                time.sleep(MIN_TIME - (time.time() - start_req))

            q.task_done()

    def retrieve_data(self):
        self.load_data()

        q = queue.Queue()

        threads = []
        for x in range(0, THREAD_COUNT):
            t = threading.Thread(target=self.worker, args=(q,))
            threads.append(t)
            t.start()

        self.count_records()
        print(self.name + " - records: " + str(self.counted))
        for i in range(0, int(self.counted / 500) + 1):
            offset = i * 500
            q.put(offset)

        q.join()

        for _ in threads:
            q.put(None)

        for t in threads:
            t.join()

        joblib.dump(self.threadList, self.filename)

        try:
            export_list_to_csv(self.threadList, f"{self.name}.csv")
        except Exception:
            pass

        return self.threadList
