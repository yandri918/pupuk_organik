import sys
import os

# Add root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.solid_fertilizer import calculate_solid_fertilizer, ORGANIC_DATABASE, SOLID_PRESET_RECIPES
from app.models.schemas import SolidCalculationRequest, MaterialInput, LiquidDoseRequest, LiquidSNIRequest, EconomicsRequest
from app.services.liquid_fertilizer import calculate_liquid_dosage, check_liquid_sni, POC_RECIPES_DATABASE
from app.services.optimizer import optimize_solid_formulation
from app.services.economics import calculate_economics

print("1. Testing Solid Fertilizer Calculation...")
req = SolidCalculationRequest(
    materials=[
        MaterialInput(name="Kotoran Sapi", weight_kg=500),
        MaterialInput(name="Sekam Padi Mentah", weight_kg=200),
        MaterialInput(name="Dedak Padi Halus (Katul)", weight_kg=30)
    ],
    fermentation_days=5
)
res = calculate_solid_fertilizer(req)
print(f"   Total Weight: {res.total_weight_kg} kg")
print(f"   NPK: {res.npk_label}")
print(f"   Initial C/N: {res.initial_c_n_ratio}, Current C/N: {res.estimated_current_c_n_ratio}")
print(f"   Phase: {res.fermentation_phase} ({res.temperature_range})")
assert res.total_weight_kg == 730.0

print("2. Testing AI Optimizer...")
from app.models.schemas import SolidOptimizationRequest
opt_req = SolidOptimizationRequest(
    target_total_weight_kg=1000,
    target_c_n_ratio=28.0,
    available_materials=["Kotoran Sapi", "Sekam Padi Mentah", "Dedak Padi Halus (Katul)"],
    priority="balanced"
)
opt_res = optimize_solid_formulation(opt_req)
print(f"   Target C/N: {opt_res.target_c_n_ratio}, Achieved: {opt_res.estimated_achieved_c_n}")
for m in opt_res.materials:
    print(f"   - {m.name}: {m.recommended_kg} kg ({m.percentage}%)")

print("3. Testing Liquid Fertilizer Dosage...")
dose_req = LiquidDoseRequest(
    poc_type="POC ROTAN Premium",
    crop_category="Padi",
    application_method="Semprot Daun (Spraying)",
    volume_liters=14.0
)
dose_res = calculate_liquid_dosage(dose_req)
print(f"   Recommended POC: {dose_res.recommended_poc_cc} cc for {dose_res.water_volume_liters} L")
print(f"   Frequency: {dose_res.application_frequency}")

print("4. Testing Liquid SNI Check...")
sni_req = LiquidSNIRequest(
    c_organic_pct=12.5,
    total_npk_pct=3.5,
    ph=6.8,
    pathogen_salmonella="Negatif"
)
sni_res = check_liquid_sni(sni_req)
print(f"   SNI Status: {sni_res.overall_status}")

print("5. Testing Economics & HPP...")
eco_req = EconomicsRequest(
    fertilizer_type="Padat (kg)",
    batch_volume=1000,
    raw_material_cost=250000,
    bioactivator_cost=80000,
    labor_cost=300000,
    energy_packaging_cost=150000,
    capex_equipment=10000000,
    depreciation_months=36,
    target_selling_price=2500
)
eco_res = calculate_economics(eco_req)
print(f"   HPP Unit: Rp {eco_res.unit_cost_hpp:,.0f} / kg")
print(f"   Net Profit: Rp {eco_res.net_profit:,.0f} (Margin: {eco_res.profit_margin_pct}%)")
print(f"   BEP: {eco_res.break_even_units} kg")

print("\nALL BACKEND SERVICES TESTED AND PASSED SUCCESSFULLY!")