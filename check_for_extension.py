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
for filename in os.listdir(directory):
    gpus[filename.replace(".json", "")] = ''
    full_filename = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(full_filename):
        json_files.append(full_filename)
        

for json_filename in json_files:
    f = open(json_filename)
    value = ""
    data = json.load(f)
    for first_layer in data:
        if first_layer == "extensions":
            for extension in data[first_layer]:
                for key in extension:
                    if key == "extensionName":
                        if extension[key] in searched_extensions:
                            value = value + ' ' + extension[key]
    for gpu in gpus:
        if gpu in json_filename:
            gpus[gpu] = value
                                

print(gpus)
    
gpus_info = ["GPU", "Extensions"]

with open('test.csv', 'w', encoding='UTF8', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)
    writer.writerow(gpus_info)
    
    for key, value in gpus.items():
        row = [key, value]
        writer.writerow(row)

