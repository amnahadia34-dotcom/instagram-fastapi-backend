from fastapi import APIRouter
from services.lead_service import get_leads

router = APIRouter()

@router.get("/")
def list_leads():
    """
    List all leads from the internal database.
    """
    return get_leads()
