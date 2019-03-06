import csv
import json
import os

class ipReader:
    url_list = []
    category_title = {}
    category_path = {}

    def initiate(self):
        self.url_list = []
        self.category_path = {}
        self.category_title = {}

    def readFile(self, filename):
        with open(filename, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                self.url_list.append(row[3])
                row[0] = row[0].replace("*", ",")
                self.category_title[row[0]] = row[1]
                self.category_path[row[0]] = row[2]

def write_into_json(file_path, dict_of_items):
    # Check if file-path available
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = os.path.join(file_path ,'data.json')
    with open(file_name, 'a') as outfile:
        if outfile.tell() == 0:
            outfile.write('[')
            json.dump(dict_of_items, outfile)
            outfile.write(']')

        else:
            outfile.seek(0, os.SEEK_END)
            outfile.seek(outfile.tell() - 1, os.SEEK_SET)
            outfile.truncate()
            outfile.write(',')
            json.dump(dict_of_items, outfile)
            outfile.write(']')
