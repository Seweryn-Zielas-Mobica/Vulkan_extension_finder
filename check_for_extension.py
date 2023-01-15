import os
import json
import csv

directory = 'GPUs_JSONS'
 

searched_extensions = ("VK_EXT_full_screen_exclusive", "VK_EXT_calibrated_timestamps",
                       "VK_KHR_fragment_shader_barycentric", "VK_KHR_shader_quad_scope")

json_files = []
gpus = {}
 
# iterate over files in
# that directory
def main():
    search_for_json_files(directory, json_files)
            
    for json_filename in json_files:
        search_json_for_extensions(json_filename, gpus)


    print(gpus)
        
    write_to_csv("test.csv", gpus)

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