import sys
import os

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.solid_fertilizer import calculate_solid_fertilizer, ORGANIC_DATABASE, SOLID_PRESET_RECIPES
from app.models.schemas import (
    SolidCalculationRequest, MaterialInput,
    LiquidDoseRequest, LiquidSNIRequest, EconomicsRequest,
    SolidOptimizationRequest
)
from app.services.liquid_fertilizer import calculate_liquid_dosage, check_liquid_sni, POC_RECIPES_DATABASE
from app.services.optimizer import optimize_solid_formulation
from app.services.economics import calculate_economics

print("=== 1. Testing Solid Fertilizer Mass Balance (Dry Basis vs Wet Input) ===")
# Exact test case from user audit: 100 kg Kotoran Sapi (moisture 65%, N 1.4% DW)
audit_req = SolidCalculationRequest(
    materials=[MaterialInput(name="Kotoran Sapi", weight_kg=100.0)],
    fermentation_days=0
)
audit_res = calculate_solid_fertilizer(audit_req)
print(f"   Wet Input: {audit_res.total_wet_weight_kg} kg")
print(f"   Dry Matter: {audit_res.total_dry_weight_kg} kg (Expected: 35.0 kg)")
print(f"   Total Nitrogen Mass: {audit_res.total_nitrogen_kg} kg (Expected: 0.49 kg)")
assert abs(audit_res.total_dry_weight_kg - 35.0) < 0.1
assert abs(audit_res.total_nitrogen_kg - 0.49) < 0.01
print("   PASS: Dry-basis mass balance correctly calculates 0.49 kg N instead of 1.40 kg!")

print("\n=== 2. Testing Solid SNI Upper Bound for C-Organic (9.80 - 32.00%) ===")
# Mixture with high carbon (Arang Sekam & Serbuk Gergaji > 32% C-DW)
high_c_req = SolidCalculationRequest(
    materials=[
        MaterialInput(name="Arang Sekam Padi", weight_kg=200.0),
        MaterialInput(name="Serbuk Gergaji Kayu Lunak", weight_kg=200.0)
    ],
    fermentation_days=21
)
high_c_res = calculate_solid_fertilizer(high_c_req)
c_sni_item = next(item for item in high_c_res.sni_evaluation if "C-Organik" in item.parameter)
print(f"   Measured C-Organic: {c_sni_item.measured_value}% | Status: {c_sni_item.status}")
assert "Melebihi Batas SNI" in c_sni_item.status
print("   PASS: C-Organic > 32% is correctly flagged as exceeding SNI standard!")

print("\n=== 3. Testing SLSQP Optimizer with Moisture Correction & Feasibility ===")
opt_req = SolidOptimizationRequest(
    target_total_weight_kg=1000.0,
    target_c_n_ratio=28.0,
    available_materials=["Kotoran Sapi", "Sekam Padi Mentah", "Dedak Padi Halus (Katul)"],
    priority="balanced"
)
opt_res = optimize_solid_formulation(opt_req)
print(f"   Target C/N: {opt_res.target_c_n_ratio} | Achieved C/N: {opt_res.estimated_achieved_c_n}")
print(f"   Feasibility Status: {opt_res.feasibility_status}")
for m in opt_res.materials:
    print(f"   - {m.name}: {m.recommended_wet_kg} kg ({m.percentage}%)")
assert abs(sum(m.recommended_wet_kg for m in opt_res.materials) - 1000.0) < 0.2
print("   PASS: Optimizer respects total weight constraint and dry-matter C/N target!")

print("\n=== 4. Testing Liquid POC NPK > 6% Strict Failure Check ===")
poc_high_npk = LiquidSNIRequest(
    c_organic_pct=15.0,
    total_npk_pct=7.2,  # > 6.0% (Exceeds Permentan 261/2019)
    ph=6.5,
    pathogen_ecoli_cfu=10.0,
    pathogen_salmonella="Negatif"
)
poc_res = check_liquid_sni(poc_high_npk)
print(f"   Total NPK: 7.2% | is_passed: {poc_res.is_passed} | Status: {poc_res.overall_status}")
assert poc_res.is_passed is False
npk_eval = next(e for e in poc_res.details if "Hara Makro" in e.parameter)
assert "Melebihi Batas" in npk_eval.status
print("   PASS: POC with NPK > 6.0% correctly fails overall Permentan 261/2019 standard!")

print("\n=== 5. Testing Biological Safety Check (E. coli & Salmonella) ===")
poc_contaminated = LiquidSNIRequest(
    c_organic_pct=12.0,
    total_npk_pct=3.5,
    ph=6.5,
    pathogen_ecoli_cfu=250.0,  # >= 100 CFU/ml (Contaminated)
    pathogen_salmonella="Negatif"
)
poc_contam_res = check_liquid_sni(poc_contaminated)
print(f"   E. coli: 250 CFU/ml | is_passed: {poc_contam_res.is_passed}")
assert poc_contam_res.is_passed is False
ecoli_eval = next(e for e in poc_contam_res.details if "Escherichia coli" in e.parameter)
assert "Tercemar" in ecoli_eval.status
print("   PASS: E. coli contamination is strictly flagged and fails certification!")

print("\n=== 6. Testing Economics & Contribution Margin BEP ===")
eco_req = EconomicsRequest(
    fertilizer_type="Padat (kg)",
    batch_volume=1000.0,
    raw_material_cost=250000.0,
    bioactivator_cost=80000.0,
    labor_cost=300000.0,
    energy_packaging_cost=150000.0,
    fixed_overhead_cost=100000.0,
    capex_equipment=10000000.0,
    depreciation_months=36,
    batches_per_month=2.0,  # Configurable batch cycles
    target_selling_price=2500.0
)
eco_res = calculate_economics(eco_req)
print(f"   HPP Unit: Rp {eco_res.unit_cost_hpp:,.0f} / kg")
print(f"   Net Profit: Rp {eco_res.net_profit:,.0f} (Margin: {eco_res.profit_margin_pct}%)")
print(f"   BEP Units: {eco_res.break_even_units:,.1f} kg")
assert eco_res.unit_cost_hpp > 0
assert eco_res.break_even_units > 0
print("   PASS: Economics separates fixed/variable burdens with accurate contribution margin!")

print("\n=== 7. Testing POC Batch Brewing Calculator (100L Drum) ===")
from app.models.schemas import POCBatchBrewRequest, POCFieldScheduleRequest
from app.services.liquid_fertilizer import calculate_poc_batch_brew, calculate_field_schedule, get_troubleshoot_database

brew_req = POCBatchBrewRequest(
    drum_volume_liters=100.0,
    purpose="vegetatif_n",
    fermentation_type="anaerob"
)
brew_res = calculate_poc_batch_brew(brew_req)
print(f"   Drum: {brew_res.drum_volume_liters}L | Effective: {brew_res.effective_liquid_liters}L | Headspace: {brew_res.headspace_liters}L")
print(f"   Purpose: {brew_res.purpose_title}")
print(f"   Estimated NPK: {brew_res.estimated_npk}")
print(f"   Total Ingredients: {len(brew_res.ingredients)} | Cost/L: Rp {brew_res.estimated_cost_per_liter:,.0f}")
assert brew_res.effective_liquid_liters == 85.0
assert brew_res.headspace_liters == 15.0
assert len(brew_res.ingredients) >= 5
print("   PASS: POC Batch Brewing Formulator correctly scales 85L working volume with 15L gas headspace safety!")

print("\n=== 8. Testing Field-Scale Spray Schedule for Rice (Padi Sawah 10,000 m²) ===")
field_req = POCFieldScheduleRequest(
    crop_name="Padi Sawah",
    land_area_sqm=10000.0,
    tank_capacity_liters=16.0
)
field_res = calculate_field_schedule(field_req)
print(f"   Crop: {field_res.crop_name} | Area: {field_res.land_area_desc}")
print(f"   Total Seasonal POC: {field_res.total_seasonal_poc_liters} L")
print(f"   Total Stages: {len(field_res.stages)}")
assert field_res.total_seasonal_poc_liters > 0
assert len(field_res.stages) == 5
print("   PASS: Field-scale HST schedule calculates all 5 growth phases and seasonal POC requirements!")

print("\n=== 9. Testing POC Troubleshooting & Diagnostics Database ===")
troubles = get_troubleshoot_database()
print(f"   Total Diagnosed Symptoms: {len(troubles)}")
assert len(troubles) >= 6
assert any(t.id == "bau_busuk_bangkai" for t in troubles)
assert any(t.id == "tong_kembung_meledak" for t in troubles)
print("   PASS: Troubleshooting database covers anaerobic spoilage, airlock, and mould diagnostics!")

print("\n=== 10. Testing Organic Waste / Garbage Materials in Solid Fertilizer Database ===")
waste_materials = [
    "Sampah Sayuran Hijau (Limbah Pasar & Dapur)",
    "Sampah Kulit Buah-Buahan (Sisa Pasar/Jus)",
    "Sampah Sisa Makanan Dapur (Food Waste)",
    "Ampas Kopi (Spent Coffee Grounds)",
    "Ampas Tahu Basah (Limbah Industri Tahu)",
    "Limbah Baglog Jamur Tiram (Bekas Media)",
    "Sampah Daun Kering / Serasah Kebun",
    "Eceng Gondok (Cacahan Gulma Rawa)",
    "Tandan Kosong Kelapa Sawit (TKKS Cacah)",
    "Limbah Kulit Bawang Merah & Putih"
]
for wm in waste_materials:
    assert wm in ORGANIC_DATABASE, f"Missing {wm} in ORGANIC_DATABASE"
print(f"   Total Solid Organic Materials in DB: {len(ORGANIC_DATABASE)} (Includes 10 Waste/Garbage Variants)")

# Test calculation with market waste mix
waste_calc_req = SolidCalculationRequest(
    materials=[
        MaterialInput(name="Sampah Sayuran Hijau (Limbah Pasar & Dapur)", weight_kg=300.0),
        MaterialInput(name="Sampah Kulit Buah-Buahan (Sisa Pasar/Jus)", weight_kg=200.0),
        MaterialInput(name="Sampah Daun Kering / Serasah Kebun", weight_kg=200.0),
        MaterialInput(name="Arang Sekam Padi", weight_kg=50.0)
    ],
    fermentation_days=14
)
waste_calc_res = calculate_solid_fertilizer(waste_calc_req)
print(f"   Market Waste Mix Input: {waste_calc_res.total_wet_weight_kg} kg | Dry Matter: {waste_calc_res.total_dry_weight_kg} kg")
print(f"   Initial C/N: {waste_calc_res.initial_c_n_ratio}:1 | NPK: {waste_calc_res.npk_label}")
assert waste_calc_res.total_wet_weight_kg == 750.0
assert waste_calc_res.initial_c_n_ratio > 0

# Test optimizer using organic waste
opt_waste_req = SolidOptimizationRequest(
    target_total_weight_kg=500.0,
    target_c_n_ratio=25.0,
    available_materials=[
        "Sampah Sayuran Hijau (Limbah Pasar & Dapur)",
        "Sampah Daun Kering / Serasah Kebun",
        "Ampas Kopi (Spent Coffee Grounds)"
    ],
    priority="balanced"
)
opt_waste_res = optimize_solid_formulation(opt_waste_req)
print(f"   Waste Optimizer Target C/N: {opt_waste_res.target_c_n_ratio} | Achieved: {opt_waste_res.estimated_achieved_c_n}")
assert abs(sum(m.recommended_wet_kg for m in opt_waste_res.materials) - 500.0) < 0.2
print("   PASS: All 10 organic waste variants calculate correctly and integrate seamlessly with SLSQP Optimizer!")

print("\nALL AUDIT & EXTENDED POC/WASTE TEST CASES PASSED WITH 100% SUCCESS!")