import os
import re
import joblib
from datetime import datetime
from rapidfuzz import process

from file_export import export_list_to_csv
from api_igdb import getMultiThread # legacy
from igdb_api_class import IGDBAPI
from config_dicts import replacements_dict, region_dict
from db_class import DATABASE


def prepareList(sourceList, keyname=None):
    for e in sourceList:
        if type(sourceList[0]) is dict:
            for key, value in replacements_dict.items():
                if e[keyname] is None:
                    e[keyname] = ""
                if key in e[keyname]:
                    # se dizionario
                    e[keyname] = e[keyname].replace(key, value)

            re.sub("[\(\[].*?[\)\]]", "", e[keyname])
            e[keyname] = re.sub("\s{2,}", " ", e[keyname])
            e[keyname] = e[keyname].strip()
            e[keyname] = e[keyname].lower()

            # rimpiazza le lettere multiple consecutive
            # e[keyname] = re.sub(r"(.)\1+", r"\1", e[keyname])

        else:
            for key, value in replacements_dict.items():
                if e is None:
                    e = ""
                if key in e:
                    # se dizionario
                    e = e.replace(key, value)

            re.sub("[\(\[].*?[\)\]]", "", e)
            e = re.sub("\s{2,}", " ", e)
            e = e.strip()
            e = e.lower()

            # rimpiazza le lettere multiple consecutive
            # e = re.sub(r"(.)\1+", r"\1", e)

    return sourceList


def prepareString(source):
    source = source.lower()
    for key, value in replacements_dict.items():
        if key in source:
            source = source.replace(key, value)

    source = re.sub("\s{2,}", " ", source)
    source = source.strip()

    return source


def searchLocalFuzzy(sourceList, search: str, cutoff) -> str:
    if len(sourceList) == 0:
        return False

    out = process.extractOne(search, sourceList, score_cutoff=cutoff)

    return out


def getElementFromList(list, tosearch, value, toget):
    return [d[toget] for d in list if d[tosearch] == value][0]


def getDictFromList(list, tosearch, value):
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
    myfile = open(fileName, "r")
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
    prefix = "simple_" + str(platformID)
    ext = ".sav"
    filename = prefix + ext

    try:
        sl = joblib.load(filename)
        export_list_to_csv(sl, prefix + ".csv")
        return sl
    except Exception:
        sl = []

    lout = []

    genres = IGDBAPI("genres", "genres", "fields *").retrieve_data()
    companies = IGDBAPI("companies", "companies", "fields *").retrieve_data()
    involved_companies = IGDBAPI(
        "involved_companies", "involved_companies", "fields *"
    ).retrieve_data()
    games = IGDBAPI(
        "games_" + str(platformID),
        "games",
        "fields *",
        "where platforms = (" + str(platformID) + ")",
    ).retrieve_data()
    alternative_names = IGDBAPI(
        "alternative_names", "alternative_names", "fields *"
    ).retrieve_data()

    for element in games:
        print(element["name"])
        id = element["id"]
        name = element["name"]
        release = ""

        gen = []
        try:
            for i in element["genres"]:
                gname = getElementFromList(genres, "id", i, "name")
                gen.append(gname)
        except Exception:
            pass

        dev = []
        pub = []
        try:
            release = datetime.utcfromtimestamp(element["first_release_date"]).strftime(
                "%Y-%m-%d"
            )
            for i in element["involved_companies"]:
                cid = getElementFromList(involved_companies, "id", i, "company")
                cname = getElementFromList(companies, "id", cid, "name")
                fdev = getElementFromList(involved_companies, "id", i, "developer")
                fpub = getElementFromList(involved_companies, "id", i, "publisher")

                if fdev:
                    dev.append(cname)
                if fpub:
                    pub.append(cname)
        except Exception:
            pass

        lout.append(
            {"id": id, "name": name, "rel": release, "gen": gen, "pub": pub, "dev": dev}
        )

        altName = []
        try:
            for i in element["alternative_names"]:
                gname = getElementFromList(alternative_names, "id", i, "name")
                lout.append(
                    {
                        "id": id,
                        "name": gname,
                        "rel": release,
                        "gen": gen,
                        "pub": pub,
                        "dev": dev,
                    }
                )
        except Exception:
            pass

    # ordino la luista per id
    lout = sorted(lout, key=lambda d: d["id"])

    joblib.dump(lout, filename)

    try:
        export_list_to_csv(lout, prefix + ".csv")
    except Exception:
        pass

    return lout

def get_names(platforms):
    with DATABASE("IGDB.db") as db:
        return db.get_v_complete_names(platforms)
        