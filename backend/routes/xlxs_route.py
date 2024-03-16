from fastapi import File, UploadFile, APIRouter, HTTPException, BackgroundTasks
from typing import Annotated
from functions.helper import allowed_file
from fastapi.responses import StreamingResponse
import traceback
from functions.convertor import convert_excel_to_bson
router = APIRouter(
    prefix="/convert/xlsx",
    tags=["bson"],
)

# # Global dictionary to store processed data
processed_data_storage = {} 
processed_data_key = 'dataframe'
fileName =""



async def process_file(file_content: bytes):
    try:
        json_bytes = await convert_excel_to_bson(file_content)
        processed_data_storage[processed_data_key] = json_bytes
    except Exception as e:
         traceback.print_exc()
   

@router.post("/upload")
async def upload(file: Annotated[UploadFile, File(description="upload a xlxs file")]):
    if not allowed_file(file.filename,["xlsx","xls"]):
        raise HTTPException(status_code=400, detail="File type not allowed")
    try:
      fileName = f"{file.filename.split(".")[0]}.json"
      headers = {
        "Content-Disposition": f"attachment; filename={fileName}"
    }
      content = await file.read()
      json_bytes = await convert_excel_to_bson(content)
      return StreamingResponse(json_bytes, media_type="application/octet-stream",headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")


@router.post("/upload-background")
async def upload(file: Annotated[UploadFile, File(description="upload a xlxs file")], background_tasks: BackgroundTasks):
    if not allowed_file(file.filename,["xlsx","xls"]):
        raise HTTPException(status_code=400, detail="File type not allowed")
    try:
        file_content = await file.read()
        global fileName
        fileName = f"{file.filename.split(".")[0]}.json"

        background_tasks.add_task(process_file, file_content)
        return {"message": "File is being processed in the background. It will be available shortly."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")


@router.get("/processed-data")
async def get_processed_data():
    try:
        processed_data = processed_data_storage.get(processed_data_key)
        if processed_data:
            headers = {
            "Content-Disposition": f"attachment; filename={fileName}"
            }
            return StreamingResponse(processed_data,media_type="application/octet-stream", headers=headers)
        else:
            return {"status":"pending"}
    except Exception as e:
        return {"error": "Processed data not found"}

   