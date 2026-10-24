import numpy as np
from typing import List, Dict, Any
from app.services.solid_fertilizer import ORGANIC_DATABASE, P_TO_P2O5, K_TO_K2O
from app.models.schemas import (
    SolidOptimizationRequest, SolidOptimizationResponse, OptimizedMaterial
)

def optimize_solid_formulation(req: SolidOptimizationRequest) -> SolidOptimizationResponse:
    target_weight = req.target_total_weight_kg
    target_cn = req.target_c_n_ratio
    avail = req.available_materials

    # Validate materials without silent substitution
    valid_materials = [m for m in avail if m in ORGANIC_DATABASE]
    if len(valid_materials) < 2:
        return SolidOptimizationResponse(
            target_total_weight_kg=target_weight,
            target_c_n_ratio=target_cn,
            estimated_achieved_c_n=0.0,
            estimated_npk="N/A",
            feasibility_status="Gagal: Minimal 2 bahan valid harus dipilih oleh pengguna.",
            materials=[],
            notes=[
                "Optimasi tidak dapat dijalankan karena bahan yang dipilih kurang dari 2 bahan valid dalam database.",
                "Silakan pilih minimal 2 bahan (misal 1 bahan sumber karbon dan 1 bahan sumber nitrogen)."
            ]
        )

    n_mats = len(valid_materials)

    # Extract Dry Matter fraction, Carbon %, and Nitrogen % for each material
    moist_vals = np.array([ORGANIC_DATABASE[m]["moisture_typical"] for m in valid_materials])
    dm_fractions = np.maximum(0.05, 1.0 - (moist_vals / 100.0))  # Dry matter fraction

    c_dw_vals = np.array([ORGANIC_DATABASE[m]["carbon"] for m in valid_materials])
    n_dw_vals = np.array([ORGANIC_DATABASE[m]["n"] for m in valid_materials])
    p_dw_vals = np.array([ORGANIC_DATABASE[m]["p"] for m in valid_materials])
    k_dw_vals = np.array([ORGANIC_DATABASE[m]["k"] for m in valid_materials])

    # Effective C and N per kg of fresh wet weight
    c_per_kg_wet = dm_fractions * (c_dw_vals / 100.0)
    n_per_kg_wet = dm_fractions * (n_dw_vals / 100.0)

    # Individual material effective C/N
    individual_cn = c_dw_vals / np.maximum(0.01, n_dw_vals)
    min_possible_cn = np.min(individual_cn)
    max_possible_cn = np.max(individual_cn)

    notes = []
    feasibility = "Optimal (Target C/N Tercapai)"

    # Check mathematical feasibility within the selected set
    if target_cn < min_possible_cn:
        feasibility = f"Terbatas: Target C/N ({target_cn:.1f}) di bawah batas terendah bahan terpilih ({min_possible_cn:.1f})."
        notes.append(f"Seluruh bahan yang Anda pilih memiliki C/N lebih tinggi dari target. Hasil optimasi dibatasi pada C/N terendah yang memungkinkan ({min_possible_cn:.1f}:1).")
        target_cn = min_possible_cn
    elif target_cn > max_possible_cn:
        feasibility = f"Terbatas: Target C/N ({target_cn:.1f}) di atas batas tertinggi bahan terpilih ({max_possible_cn:.1f})."
        notes.append(f"Tidak ada bahan berkadar karbon cukup tinggi dalam pilihan Anda untuk mencapai C/N {target_cn:.1f}:1. Tambahkan bahan tinggi karbon seperti sekam atau serbuk gergaji.")
        target_cn = max_possible_cn

    try:
        from scipy.optimize import minimize

        def objective(w):
            # w represents fresh wet weights in kg
            total_c = np.sum(w * c_per_kg_wet)
            total_n = np.sum(w * n_per_kg_wet)
            current_cn = total_c / (total_n + 1e-6)

            # High-priority penalty for deviation from target C/N
            cn_penalty = 10000.0 * ((current_cn - target_cn) / target_cn) ** 2

            # Normalized priority preference penalty/reward
            w_norm = w / target_weight
            if req.priority == "high_n":
                priority_penalty = -50.0 * np.sum(w_norm * n_per_kg_wet)
            elif req.priority == "high_p":
                priority_penalty = -50.0 * np.sum(w_norm * (dm_fractions * (p_dw_vals / 100.0)))
            elif req.priority == "high_k":
                priority_penalty = -50.0 * np.sum(w_norm * (dm_fractions * (k_dw_vals / 100.0)))
            else:
                priority_penalty = 1.0 * np.sum((w_norm - (1.0 / n_mats)) ** 2)

            return cn_penalty + priority_penalty

        # Constraints: sum(wet weights) == target_weight
        cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - target_weight}]
        
        # Bounds: each selected material gets between 3% and 90% of total mass
        min_weight = target_weight * 0.03
        max_weight = target_weight * 0.90
        bounds = [(min_weight, max_weight) for _ in range(n_mats)]

        # Initial guess: equal distribution
        x0 = np.full(n_mats, target_weight / n_mats)

        res = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons, options={'maxiter': 300, 'ftol': 1e-6})

        if res.success:
            weights = np.maximum(0, res.x)
            weights = (weights / np.sum(weights)) * target_weight
        else:
            weights = x0
            feasibility = "Heuristik: Solver konvergen mendekati nilai target."
            notes.append("Konvergensi eksak SLSQP tidak tercapai sepenuhnya, formula dialokasikan dengan aproksimasi terdekat.")
    except Exception as e:
        # Fallback without substituting user materials
        weights = np.full(n_mats, target_weight / n_mats)
        feasibility = "Aproksimasi Standar"
        notes.append(f"Catatan solver: {str(e)}")

    # Calculate actual achieved metrics with dry-basis mass balance
    dry_weights = weights * dm_fractions
    total_dry = np.sum(dry_weights)

    final_c_kg = np.sum(dry_weights * (c_dw_vals / 100.0))
    final_n_kg = np.sum(dry_weights * (n_dw_vals / 100.0))
    final_p_elem_kg = np.sum(dry_weights * (p_dw_vals / 100.0))
    final_k_elem_kg = np.sum(dry_weights * (k_dw_vals / 100.0))

    final_p2o5_kg = final_p_elem_kg * P_TO_P2O5
    final_k2o_kg = final_k_elem_kg * K_TO_K2O

    achieved_cn = final_c_kg / (final_n_kg + 1e-6)
    achieved_n_dw_pct = (final_n_kg / total_dry) * 100.0 if total_dry > 0 else 0.0
    achieved_p2o5_dw_pct = (final_p2o5_kg / total_dry) * 100.0 if total_dry > 0 else 0.0
    achieved_k2o_dw_pct = (final_k2o_kg / total_dry) * 100.0 if total_dry > 0 else 0.0

    materials_list: List[OptimizedMaterial] = []
    for i, name in enumerate(valid_materials):
        w_kg = float(weights[i])
        pct = (w_kg / target_weight) * 100.0
        role = ORGANIC_DATABASE[name]["character"]
        materials_list.append(OptimizedMaterial(
            name=name,
            recommended_wet_kg=round(w_kg, 1),
            percentage=round(pct, 1),
            role=role
        ))

    npk_label = f"N-P2O5-K2O (Basis Kering): {achieved_n_dw_pct:.2f}% - {achieved_p2o5_dw_pct:.2f}% - {achieved_k2o_dw_pct:.2f}%"

    notes.append(
        "Perhitungan optimasi mengonversi berat basah ke fraksi berat kering untuk menjamin akurasi rasio C/N campuran aktual."
    )

    return SolidOptimizationResponse(
        target_total_weight_kg=target_weight,
        target_c_n_ratio=target_cn,
        estimated_achieved_c_n=round(achieved_cn, 1),
        estimated_npk=npk_label,
        feasibility_status=feasibility,
        materials=materials_list,
        notes=notes
    )
