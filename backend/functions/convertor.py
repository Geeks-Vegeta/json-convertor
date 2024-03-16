from .helper import convert_to_array_or_dict
from fastapi import UploadFile
import pandas as pd
import json
from io import BytesIO
import traceback

def convert_to_bytes(df):
    data=[row.to_dict() for _, row in df.iterrows()]
    dump_Data=json.dumps(data)
    output = BytesIO(dump_Data.encode('utf-8'))
    output.seek(0)
    return output



async def convert_excel_to_bson(file_content: bytes):
    try:
        df = pd.read_excel(BytesIO(file_content))
        df = df.applymap(convert_to_array_or_dict)
        output = convert_to_bytes(df)
        return output
    except Exception as e:
        traceback.print_exc()



async def convert_csv_to_bson(file_content: bytes):
    df = pd.read_csv(BytesIO(file_content))
    output = convert_to_bytes(df)
    return output