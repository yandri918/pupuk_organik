import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Dict, Any, List

from app.core.config import settings
from app.models.schemas import (
    SolidCalculationRequest, SolidCalculationResponse,
    SolidOptimizationRequest, SolidOptimizationResponse,
    LiquidDoseRequest, LiquidDoseResponse,
    LiquidSNIRequest, LiquidSNIResponse,
    POCBatchBrewRequest, POCBatchBrewResponse,
    POCFieldScheduleRequest, POCFieldScheduleResponse,
    POCTroubleshootItem, POCTankMixItem,
    EconomicsRequest, EconomicsResponse
)
from app.services.solid_fertilizer import (
    ORGANIC_DATABASE, SOLID_PRESET_RECIPES, calculate_solid_fertilizer
)
from app.services.liquid_fertilizer import (
    POC_RECIPES_DATABASE, MOL_COLLECTION, calculate_liquid_dosage, check_liquid_sni,
    calculate_poc_batch_brew, calculate_field_schedule,
    get_troubleshoot_database, get_tank_mix_guide
)
from app.services.optimizer import optimize_solid_formulation
from app.services.economics import calculate_economics

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
async def serve_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": f"Welcome to {settings.PROJECT_NAME}. UI index.html will be served here."}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "features": ["pupuk_padat", "pupuk_cair", "ai_optimizer", "economics"]
    }

# --- SOLID FERTILIZER ENDPOINTS ---

@app.get("/api/solid/materials")
async def get_solid_materials():
    return {
        "materials": [
            {
                "name": name,
                "category": data["category"],
                "carbon_pct": data["carbon"],
                "n_pct": data["n"],
                "p_pct": data["p"],
                "k_pct": data["k"],
                "c_n_ratio": data["c_n"],
                "character": data["character"]
            }
            for name, data in ORGANIC_DATABASE.items()
        ]
    }

@app.post("/api/solid/calculate", response_model=SolidCalculationResponse)
async def calculate_solid(req: SolidCalculationRequest):
    try:
        return calculate_solid_fertilizer(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/solid/optimize", response_model=SolidOptimizationResponse)
async def optimize_solid(req: SolidOptimizationRequest):
    try:
        return optimize_solid_formulation(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/solid/recipes")
async def get_solid_recipes():
    return {"recipes": SOLID_PRESET_RECIPES}

# --- LIQUID FERTILIZER (POC) ENDPOINTS ---

@app.get("/api/liquid/recipes")
async def get_liquid_recipes():
    return {
        "poc_recipes": POC_RECIPES_DATABASE,
        "mol_collection": MOL_COLLECTION
    }

@app.post("/api/liquid/calculate-dose", response_model=LiquidDoseResponse)
async def calculate_liquid_dose(req: LiquidDoseRequest):
    try:
        return calculate_liquid_dosage(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/liquid/sni-check", response_model=LiquidSNIResponse)
async def check_liquid_sni_endpoint(req: LiquidSNIRequest):
    try:
        return check_liquid_sni(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/liquid/batch-brew", response_model=POCBatchBrewResponse)
async def calculate_batch_brew_endpoint(req: POCBatchBrewRequest):
    try:
        return calculate_poc_batch_brew(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/liquid/field-schedule", response_model=POCFieldScheduleResponse)
async def calculate_field_schedule_endpoint(req: POCFieldScheduleRequest):
    try:
        return calculate_field_schedule(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/liquid/troubleshooting", response_model=List[POCTroubleshootItem])
async def get_troubleshooting_endpoint():
    return get_troubleshoot_database()

@app.get("/api/liquid/tank-mix-guide", response_model=List[POCTankMixItem])
async def get_tank_mix_endpoint():
    return get_tank_mix_guide()

# --- BUSINESS ECONOMICS ENDPOINTS ---

@app.post("/api/economics/calculate", response_model=EconomicsResponse)
async def calculate_economics_endpoint(req: EconomicsRequest):
    try:
        return calculate_economics(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
