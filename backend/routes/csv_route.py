from fastapi import File, UploadFile, APIRouter, HTTPException
from typing import Annotated
from functions.helper import allowed_file

router = APIRouter(
    prefix="/convert/csv",
    tags=["bson"],
)


@router.post("/upload")
async def upload(file: Annotated[UploadFile, File(description="upload a csv file")]):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not allowed")
    return {"status":"ok"}
