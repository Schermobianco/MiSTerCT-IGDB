import csv
import json

CSVfolder = 'CSV/'
JSONfolder = 'JSON/'

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