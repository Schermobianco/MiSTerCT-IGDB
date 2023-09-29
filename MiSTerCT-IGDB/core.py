import os
import re
import joblib
from datetime import datetime
from rapidfuzz import process

from file_export import export_list_to_csv
from igdb_api_class import IGDBAPI
from config_dicts import replacements_dict, regionEnum_dict, region_dict
from db_class import DATABASE
import pandas as pd

def prepare_names_df(df_column :pd.DataFrame):
    for key, value in replacements_dict.items():
        df_column = df_column.str.replace(key, value)

    df_column.str.replace("[\(\[].*?[\)\]]", "", regex=True)
    df_column.str.replace("\s{2,}", " ", regex=True)
    df_column = df_column.str.strip()
    df_column = df_column.str.lower()

    # rimpiazza le lettere multiple consecutive
    # e[keyname] = re.sub(r"(.)\1+", r"\1", e[keyname])

    return df_column


def prepare_string(source):
    source = source.lower()
    for key, value in replacements_dict.items():
        if key in source:
            source = source.replace(key, value)

    source = re.sub("\s{2,}", " ", source)
    source = source.strip()

    return source


def fuzzy_search(sourceList, search: str, cutoff) -> str:
    if len(sourceList) == 0:
        return False

    out = process.extractOne(search, sourceList, score_cutoff=cutoff)

    return out


def get_listdict_element(list, tosearch, value, toget):
    return [d[toget] for d in list if d[tosearch] == value][0]


def get_listdict(list, tosearch, value):
    return [d for d in list if d[tosearch] == value]


def get_files_from_dir(dir_path):
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


def get_files_from_txt(fileName):
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


def get_file_region(fileName: str):
    fileName = fileName.lower()
    for key, value in region_dict.items():
        if key in fileName:
            return value

    return None

def get_region_name(regionNum: str):
    if regionNum is None: return '<NOT FOUND>'

    return regionEnum_dict[regionNum]


def get_db_names(tableName,platforms):
    with DATABASE("IGDB.db") as db:
        return db.get_v_names(tableName,platforms)
    
def get_db_data(tableName,platforms):
    with DATABASE("IGDB.db") as db:
        return db.get_v_data(tableName,platforms)
        