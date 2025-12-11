from fastapi import APIRouter
from pydantic import BaseModel
from services.dataset_service import process_dataset

router = APIRouter()

class DatasetUpload(BaseModel):
    filename: str
    filedata: str  # base64 encoded file

@router.post("/upload")
def upload_dataset(data: DatasetUpload):
    """
    Upload and process dataset file (PDF or DOCX).
    """
    result = process_dataset(data.filename, data.filedata)
    return result
