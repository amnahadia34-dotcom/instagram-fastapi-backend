# ================================
# main.py — FastAPI Entry Point
# ================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import Router Modules
from routers.webhook import router as webhook_router
from routers.dataset import router as dataset_router
from routers.leads import router as leads_router
from routers.settings import router as settings_router

# ------------------------------
# APP INITIALIZATION
# ------------------------------
app = FastAPI(
    title="Instagram Automation Backend",
    description="Custom backend for IG → AI → Auto Reply → Lead Save",
    version="1.0.0"
)

# ------------------------------
# CORS SETTINGS
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Aap chaho to specific domains add kar sakte ho
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# ROUTERS REGISTRATION
# ------------------------------
app.include_router(webhook_router, prefix="/webhook", tags=["Webhook"])
app.include_router(dataset_router, prefix="/dataset", tags=["Dataset"])
app.include_router(leads_router, prefix="/leads", tags=["Leads"])
app.include_router(settings_router, prefix="/settings", tags=["Settings"])

# ------------------------------
# ROOT ENDPOINT
# ------------------------------
@app.get("/")
def root():
    return {
        "status": "running",
        "message": "Instagram Automation Backend is live.",
        "routes": [
            "/webhook",
            "/dataset",
            "/leads",
            "/settings"
        ]
    }
