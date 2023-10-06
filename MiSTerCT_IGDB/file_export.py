import csv
import json

CSVfolder = "Export/"
JSONfolder = "Export/"


def export_list_to_csv(source_list, file_name):
    try:
        fieldnames = set()
        for d in source_list:
            fieldnames.update(d.keys())
        fieldnames = sorted(fieldnames)

        with open(
            CSVfolder + file_name, "w", newline="", encoding="utf-8-sig"
        ) as csv_file:
            csv_writer = csv.DictWriter(
                csv_file, fieldnames, quoting=csv.QUOTE_ALL, delimiter=";"
            )
            csv_writer.writeheader()
            csv_writer.writerows(source_list)
    except Exception as e:
        print(f"Error: {e}")


def export_list_to_json(sourceList, fileName):
    with open(JSONfolder + fileName, "w") as myfile:
        json.dump(sourceList, myfile)
