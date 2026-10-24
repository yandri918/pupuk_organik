from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

# --- SOLID FERTILIZER SCHEMAS ---

class MaterialInput(BaseModel):
    name: str
    weight_kg: float = Field(..., gt=0, description="Berat bahan baku basah (as-is) dalam kilogram")

class SolidCalculationRequest(BaseModel):
    materials: List[MaterialInput]
    fermentation_days: Optional[int] = Field(default=0, ge=0, le=90)
    moisture_added_liters: Optional[float] = Field(default=0.0, ge=0)

class MaterialDetail(BaseModel):
    name: str
    weight_wet_kg: float
    moisture_pct: float
    weight_dry_kg: float
    carbon_pct_dw: float
    nitrogen_pct_dw: float
    phosphorus_pct_dw: float
    potassium_pct_dw: float
    carbon_kg: float
    nitrogen_kg: float
    phosphorus_kg: float
    potassium_kg: float
    c_n_ratio: float
    function_desc: str

class SNICheckResult(BaseModel):
    parameter: str
    measured_value: float
    standard_range: str
    unit: str
    status: str  # 'Lolos SNI' | 'Perlu Penyesuaian' | 'Kurang' | 'Melebihi Batas SNI'
    note: str

class SolidCalculationResponse(BaseModel):
    total_wet_weight_kg: float
    total_dry_weight_kg: float
    initial_moisture_pct: float
    total_carbon_kg: float
    total_nitrogen_kg: float
    total_p2o5_kg: float
    total_k2o_kg: float
    dry_basis_c_pct: float
    dry_basis_n_pct: float
    dry_basis_p2o5_pct: float
    dry_basis_k2o_pct: float
    initial_c_n_ratio: float
    estimated_current_c_n_ratio: float
    fermentation_phase: str
    temperature_range: str
    npk_label: str
    suitability: str
    recommendations: List[str]
    sni_evaluation: List[SNICheckResult]
    materials_breakdown: List[MaterialDetail]
    scientific_disclaimer: str

class SolidOptimizationRequest(BaseModel):
    target_total_weight_kg: float = Field(100.0, gt=10)
    target_c_n_ratio: float = Field(28.0, ge=15, le=40)
    available_materials: List[str]
    priority: str = Field("balanced", description="balanced, high_n, high_p, high_k")

class OptimizedMaterial(BaseModel):
    name: str
    recommended_wet_kg: float
    percentage: float
    role: str

class SolidOptimizationResponse(BaseModel):
    target_total_weight_kg: float
    target_c_n_ratio: float
    estimated_achieved_c_n: float
    estimated_npk: str
    feasibility_status: str
    materials: List[OptimizedMaterial]
    notes: List[str]

# --- LIQUID FERTILIZER (POC) SCHEMAS ---

class LiquidDoseRequest(BaseModel):
    poc_type: str
    crop_category: str  # Padi, Sayuran Daun, Buah/Palawija, Tanaman Keras/Sawit
    application_method: str  # Semprot Daun (Spraying) / Kocor Akar (Drenching)
    volume_liters: float = Field(14.0, gt=0, description="Volume tangki semprot atau ember kocor (Liter)")
    target_plant_age_days: Optional[int] = Field(default=30, ge=0)

class LiquidDoseResponse(BaseModel):
    poc_type: str
    crop_category: str
    application_method: str
    water_volume_liters: float
    recommended_poc_cc: float
    dilution_ratio: str
    application_frequency: str
    optimal_time: str
    special_tips: List[str]

class LiquidSNIRequest(BaseModel):
    c_organic_pct: float = Field(..., ge=0)
    total_npk_pct: float = Field(..., ge=0)
    ph: float = Field(..., ge=0, le=14)
    pathogen_ecoli_cfu: float = Field(0.0, ge=0, description="Cemaran E. coli dalam CFU/ml atau MPN/ml")
    pathogen_salmonella: str = Field("Negatif")

class LiquidSNIResponse(BaseModel):
    overall_status: str  # Memenuhi Standar Mutu POC (Permentan 261/2019) / Gagal Standar Mutu
    is_passed: bool
    details: List[SNICheckResult]
    improvement_advice: List[str]

# --- BUSINESS & ECONOMICS SCHEMAS ---

class EconomicsRequest(BaseModel):
    fertilizer_type: str  # Padat (kg) / Cair (Liter)
    batch_volume: float = Field(..., gt=0)
    raw_material_cost: float = Field(0.0, ge=0)
    bioactivator_cost: float = Field(0.0, ge=0)
    labor_cost: float = Field(0.0, ge=0)
    energy_packaging_cost: float = Field(0.0, ge=0)
    fixed_overhead_cost: float = Field(0.0, ge=0, description="Biaya overhead tetap per siklus batch (sewa tempat, utilitas tetap)")
    capex_equipment: float = Field(0.0, ge=0)
    depreciation_months: int = Field(36, ge=1)
    batches_per_month: float = Field(2.0, gt=0, description="Frekuensi siklus batch per bulan (misal 2 siklus untuk kompos 14 hari)")
    target_selling_price: float = Field(..., gt=0)

class EconomicsResponse(BaseModel):
    fertilizer_type: str
    batch_volume: float
    variable_opex: float
    fixed_batch_cost: float
    batch_depreciation: float
    total_production_cost: float
    unit_cost_hpp: float
    target_selling_price: float
    total_revenue: float
    gross_profit: float
    net_profit: float
    profit_margin_pct: float
    roi_pct: float
    break_even_units: float
    feasibility_status: str
    insights: List[str]
