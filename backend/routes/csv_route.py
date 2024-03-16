from fastapi import File, UploadFile, APIRouter, HTTPException
from typing import Annotated
from functions.helper import allowed_file
from functions.convertor import convert_csv_to_bson
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/convert/csv",
    tags=["bson"],
)

@router.post("/upload")
async def upload(file: Annotated[UploadFile, File(description="upload a csv file")]):
   if not allowed_file(file.filename,"csv"):
        raise HTTPException(status_code=400, detail="File type not allowed")
   try:
      fileName = f"{file.filename.split(".")[0]}.json"
      headers = {
        "Content-Disposition": f"attachment; filename={fileName}"
    }
      json_bytes = await convert_csv_to_bson(file)
      return StreamingResponse(json_bytes, media_type="application/octet-stream",headers=headers)
   except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error processing file: {e}")
    

