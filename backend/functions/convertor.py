from helper import convert_to_array_or_dict
import pandas as pd
import json

def convert_excel_to_bson(file, filename):
    df = pd.read_excel(file)
    df = df.applymap(convert_to_array_or_dict)
    data=[row.to_dict() for _, row in df.iterrows()]
    dump_Data=json.dumps(data)

    with open(f"{filename}.json","w") as f:
        f.write(dump_Data)

def convert_csv_to_bson(file, filename):
    df = pd.read_csv(file)
    df = df.applymap(convert_to_array_or_dict)
    data=[row.to_dict() for _, row in df.iterrows()]
    dump_Data=json.dumps(data)

    with open(f"{filename}.json","w") as f:
        f.write(dump_Data)