import os
import json
import csv
import argparse

parser = argparse.ArgumentParser(description='A test program.')

parser.add_argument("-d","--json_directory", help="Directory containing json files.", required=True)
parser.add_argument("-f", "--extensions_file", help ="Filed containing searched extensions, each extensions in separate row",
                    required=True)

args = parser.parse_args()

json_directory = args.json_directory
extensions_filename = args.extensions_file

searched_extensions = []
json_files = []
gpus = {}

def main():
    read_extensions_file(extensions_filename)
    
    print()
    print("Provided extensions:")
    for extensions in searched_extensions:
        print(extensions)
    print()
    
    search_for_json_files(json_directory, json_files)
    
    print("Searched files:")
    for file in json_files:
        print(file)
    print()
            
    for json_filename in json_files:
        search_json_for_extensions(json_filename, gpus)
        
    write_to_csv("GPUs_extensions_list.csv", gpus)

def read_extensions_file(filename):
    with open(filename, 'r', encoding='UTF8',) as f:
        for line in f:
            searched_extensions.append(line.rstrip())

def search_for_json_files(directory, json_files):
    for filename in os.listdir(directory):
        gpus[filename.replace(".json", "")] = ''
        full_filename = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(full_filename):
            json_files.append(full_filename)

def search_json_for_extensions(json_filename, gpus):
    f = open(json_filename)
    value = ""
    data = json.load(f)
    if "capabilities" not in data:
        for first_layer in data:
            if first_layer == "extensions":
                for extension in data[first_layer]:
                    for key in extension:
                        if key == "extensionName":
                            if extension[key] in searched_extensions:
                                value = value + ' ' + extension[key]
    else:
        for first_layer in data:
            if first_layer == "capabilities":
                for second_layer in data[first_layer]:
                    if second_layer == "device":
                        for third_layer in data[first_layer][second_layer]:
                            if third_layer == "extensions":
                                for extension in data[first_layer][second_layer][third_layer]:
                                    if extension in searched_extensions:
                                        value = value + ' ' + extension
    for gpu in gpus:
        if gpu in json_filename:
            gpus[gpu] = value
                                   
def write_to_csv(filename, gpus):
    gpus_info = ["GPU", "Extensions"]

    with open(filename, 'w', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(gpus_info)

        for key, value in gpus.items():
            row = [key, value]
            writer.writerow(row)
    
if __name__ == "__main__":
    main()