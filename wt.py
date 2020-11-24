import os
import json
import jsonschema
from jsonschema import validate

T = {str: 'string',
     int: 'integer',
     object: 'object',
     type(None): 'null',
     list: 'array'
     }

folder_data = 'task_folder/event/'
folder_schema = 'task_folder/schema/'
filelist = os.listdir(folder_data)
filelist_schema = os.listdir(folder_schema)
number = 0
with open('log.txt', mode='w', encoding='utf-8') as log:
    for file in filelist:
        number += 1
        log.writelines(f"\n{number}\nFile: {file}\n")
        with open(folder_data + file, mode='r', encoding='utf-8') as j:  # open json

            try:
                j = json.loads(j.read())  # having a py dict for json
            except ValueError:
                log.writelines('JSON file is not Valid\n')
                continue

            if not j:
                log.writelines('JSON file is empty\n')
                continue

            schema_name = j['event'] + '.schema'

            if schema_name not in filelist_schema:
                log.writelines(f"SCHEMA file not found: {schema_name}\n")
                continue
            else:
                log.writelines(f"Schema: {schema_name}\n")

            with open(folder_schema + schema_name, mode='r', encoding='utf-8') as s:  # open schema
                s = json.loads(s.read())  # having a py dict for schema

                data = j['data']
                if not data:
                    log.writelines(f"No Data in JSON file\n")
                    continue

                required_attributes = s['required']  # required attributes from .schema
                for required_attribute in required_attributes:
                    if required_attribute not in data:
                        log.writelines(f"JSON is missing required attribute: {required_attribute}\n")

                #  checking properties types of existing attributes

                described_properties = s['properties']
                for key, value in data.items():
                    if key not in described_properties:
                        log.writelines(f"Attribute not described: {key}\n")
                        continue
                    else:
                        if T[type(value)] not in described_properties[key]['type']:
                            log.writelines(f"Value type doesn't match {key, value}: {T[type(value)]} and {described_properties[key]['type']}\n")


print(f'FINISHED. {number} files processed')