from dotenv import load_dotenv
from igdb.wrapper import IGDBWrapper
from twitch_token import get_access_token
from file_export import export_list_to_csv
import joblib
import json
import logging
import os
import queue
import threading
import time

load_dotenv(override=False)
LOGLEVEL = os.environ.get("LOGLEVEL", "DEBUG").upper()
logging.basicConfig(level=LOGLEVEL)

logger = logging.getLogger("igdb_api_class")


THREAD_COUNT = 4  # numero massimo di thread per interrgogare IGDB max 4 al secondo
MIN_TIME = 1  # ritardo in secondi tra le richieste ai thread (in secondi)


def createIGDBWrapper():
    access_token = get_access_token()
    client_id = os.environ.get("TWITCH_CLIENT_ID")
    wrapper = IGDBWrapper(client_id, access_token)
    return wrapper


class IGDBAPI:
    def __init__(
        self,
        name,
        endPoint,
        fields,
        where="",
        saveBin: bool = True,
        saveCSV: bool = False,
    ):
        self.name = name
        self.endPoint = endPoint
        self.fields = fields
        self.where = where
        self.wrapper = 0  ## init later
        self.threadList = []
        self.filename = os.path.join(".tmp", "sav", f"{name}.sav")
        self.counted = 0
        self.saveBin = saveBin
        self.saveCSV = saveCSV

    def load_data(self):
        if self.saveBin:
            try:
                os.makedirs(os.path.join(".tmp", "sav"), exist_ok=True)
                self.threadList = joblib.load(self.filename)
                logger.info(f"<load_data! reusing {self.filename}")
                return self.threadList
            except Exception:
                self.wrapper = createIGDBWrapper()
                self.threadList = []
                return self.threadList
        else:
            self.wrapper = createIGDBWrapper()
            self.threadList = []
            return self.threadList

    def count_records(self):
        byte_array = self.wrapper.api_request(
            f"{self.endPoint}/count", f"{self.where};"
        )
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
                    self.fields
                    + "; "
                    + where
                    + " offset "
                    + str(offset)
                    + "; limit 500;",
                )
                j = byte_array.decode()
                lout = json.loads(j)
                break

            except Exception as exc:
                attempts += 1
                print(
                    "<ERROR! - IGDB attempt: "
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
            print("<FAILED! - IGDB " + str(attempts) + " > EndPoint: " + self.endPoint)
            os._exit(1)

        perc = round((100 / self.counted) * offset, 2)
        print(
            "                                                                                                                                                               ",
            end="\r",
        )
        print(
            "<WORKING - IGDB> " + self.name + " - processed: " + str(perc) + "%",
            end="\r",
        )

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

        # if not empty i return it (is form .sav file)
        if self.threadList != []:
            return self.threadList

        q = queue.Queue()

        threads = []
        for x in range(0, THREAD_COUNT):
            t = threading.Thread(target=self.worker, args=(q,))
            threads.append(t)
            t.start()

        self.count_records()
        print("")
        print(f'<STARTED - IGDB> {self.name} - records: " {str(self.counted)}')
        for i in range(0, int(self.counted / 500) + 1):
            offset = i * 500
            q.put(offset)

        q.join()
        print(
            "                                                                                                                                                               ",
            end="\r",
        )
        print("<DONE - IGDB> Finished")

        for _ in threads:
            q.put(None)

        for t in threads:
            t.join()

        if self.saveBin:
            joblib.dump(self.threadList, self.filename)

        if self.saveCSV:
            try:
                export_list_to_csv(self.threadList, f"{self.name}.csv")
            except Exception:
                pass

        return self.threadList
