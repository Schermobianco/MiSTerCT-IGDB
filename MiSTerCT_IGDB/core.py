import os
import re
import csv
from rapidfuzz import process
from rich.console import Console
from rich.table import Table

from config_dicts import replacements_dict, regionEnum_dict, region_dict
from db_class import DATABASE
import pandas as pd


def prepare_names_df(df_column: pd.DataFrame):
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
    if regionNum is None:
        return "<NOT FOUND>"

    return regionEnum_dict[regionNum]


def get_db_names(db_path, tableName, platforms):
    with DATABASE(db_path) as db:
        return db.get_v_names(tableName, platforms)


def get_db_data(db_path, tableName, platforms):
    with DATABASE(db_path) as db:
        return db.get_v_data(tableName, platforms)


def get_data(db_path, platforms):
    df_data = get_db_data(db_path, "v_agr_all", platforms)
    df_data = df_data.set_index("id")
    return df_data


def get_official_names(db_path, platforms):
    df_names_off = get_db_names(db_path, "v_official_names_regions", platforms)
    df_names_off = df_names_off.set_index("id")
    return df_names_off


def get_alternative_names(db_path, platforms):
    df_names_alt = get_db_names(db_path, "v_alternative_names_regions", platforms)
    df_names_alt = df_names_alt.set_index("id")
    return df_names_alt


def prepare_names(df):
    df["name"] = prepare_names_df(df["name"])
    return df


def search_game_name(files, df_names_off, df_names_alt):
    found = 0
    not_found = 0
    results = []
    for f in files:
        # FORCING text exclusion after "("
        gname = f.split("(", 1)

        # reg extraction from file name
        fregion = get_file_region(f)

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

        mostaccurate = None

        if fregion == None:
            # search game name inside official name df WITHOUT REGION
            mostaccurate = fuzzy_search(df_names_off["name"], gname, 89)
        else:
            # search game name inside official name df WITH REGION
            mostaccurate = fuzzy_search(
                df_names_off.loc[df_names_off["region"] == int(fregion)]["name"],
                gname,
                89,
            )
            # search game name inside alternative name df WITH REGION
            if mostaccurate == None:
                mostaccurate = fuzzy_search(
                    df_names_alt.loc[df_names_alt["region"] == int(fregion)]["name"],
                    gname,
                    89,
                )

        # search game name inside official name df WITHOUT REGION
        if mostaccurate is None:
            mostaccurate = fuzzy_search(df_names_off["name"], gname, 89)
        # search game name inside alternative name df WITHOUT REGION
        if mostaccurate is None:
            mostaccurate = fuzzy_search(df_names_alt["name"], gname, 89)

        if mostaccurate is None or isinstance(mostaccurate, bool):
            out = f, gname, "", "<NOT FOUND>"
            print(out)
            not_found += 1
            # if isinstance(mostaccurate, bool):
            #   print(f"skip this, just a bool -> {mostaccurate}")
            continue
        else:
            # mostaccurate[0] = text found
            # mostaccurate[1] = score
            # mostaccurate[2] = game id
            out = (
                f,
                gname,
                mostaccurate[2],
                mostaccurate[0],
                int(mostaccurate[1]),
                get_region_name(fregion),
            )
            # print(f"all good, found values -> {mostaccurate} | {mostaccurate[0]} | {mostaccurate[1]}")
            # df_data.iloc[mostaccurate[2]]['name'],
            # df_data.loc[(df_data['id'] == mostaccurate[2]) & (df_data['B'] == 'c')]['name'],

            # df_data.iloc[int(mostaccurate[2])]['region_name'],
            # df_data.iloc[mostaccurate[2]]['date'],
            # df_data.iloc[mostaccurate[2]]['genres_name'],
            # df_data.iloc[mostaccurate[2]]['publishers_name'],
            # df_data.iloc[mostaccurate[2]]['developers_name']
            print(out)
            found += 1

            results.append(out)

    return results, found, not_found


def write_csv(file_path, data):
    with open(file_path, "w", newline="") as csvfile:
        header = (
            "NOME FILE",
            "STRINGA CERCATA",
            "ID",
            "NOME",
            "PUNTEGGIO DI RICERCA",
            "REGION FROM FILE",
            "REGION FROM DB",
            "DATA",
            "GENERE",
            "PUB",
            "DEV",
        )
        wr = csv.writer(
            csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
        )
        wr.writerow(header)
        wr.writerow(
            ["File Name", "Game Name", "Game ID", "Matched Name", "Score", "Region"]
        )
        for row in data:
            wr.writerow(row)


def print_results(found, not_found):
    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Results", style="dim", width=12)
    table.add_column("Count", justify="right", width=8)

    table.add_row("Found", str(found))
    table.add_row("Not Found", str(not_found))
    table.add_row("Total", str(found + not_found))

    console.print(table)

    percentage = (100 / (found + not_found)) * found
    console.print(f"\nPercentage: [bold green]{percentage:.2f}%[/bold green]")
