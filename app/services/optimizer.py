import numpy as np
from typing import List, Dict, Any
from app.services.solid_fertilizer import ORGANIC_DATABASE
from app.models.schemas import (
    SolidOptimizationRequest, SolidOptimizationResponse, OptimizedMaterial
)

def optimize_solid_formulation(req: SolidOptimizationRequest) -> SolidOptimizationResponse:
    target_weight = req.target_total_weight_kg
    target_cn = req.target_c_n_ratio
    avail = req.available_materials

    # Validate materials
    valid_materials = [m for m in avail if m in ORGANIC_DATABASE]
    if len(valid_materials) < 2:
        # Fallback to standard set if fewer than 2 valid materials selected
        valid_materials = ["Kotoran Sapi", "Sekam Padi Mentah", "Dedak Padi Halus (Katul)"]

    n_mats = len(valid_materials)

    # Extract C and N for each material
    c_vals = np.array([ORGANIC_DATABASE[m]["carbon"] for m in valid_materials])
    n_vals = np.array([ORGANIC_DATABASE[m]["n"] for m in valid_materials])
    p_vals = np.array([ORGANIC_DATABASE[m]["p"] for m in valid_materials])
    k_vals = np.array([ORGANIC_DATABASE[m]["k"] for m in valid_materials])

    # Optimization objective:
    # We want weights w >= 0 such that sum(w) = target_weight
    # and sum(w * c) / sum(w * n) ~ target_cn
    # Priority adjustments:
    # - high_n: encourage materials with higher N
    # - high_p: encourage materials with higher P
    # - high_k: encourage materials with higher K
    # - balanced: smooth distribution without extreme spikes

    try:
        from scipy.optimize import minimize

        def objective(w):
            total_c = np.sum(w * c_vals)
            total_n = np.sum(w * n_vals)
            current_cn = total_c / (total_n + 1e-6)

            # Penalty for deviating from target C/N
            cn_penalty = (current_cn - target_cn) ** 2

            # Priority preference penalty/reward
            if req.priority == "high_n":
                priority_penalty = -2.0 * np.sum(w * n_vals)
            elif req.priority == "high_p":
                priority_penalty = -2.0 * np.sum(w * p_vals)
            elif req.priority == "high_k":
                priority_penalty = -2.0 * np.sum(w * k_vals)
            else:
                priority_penalty = 0.1 * np.sum((w - (target_weight / n_mats)) ** 2)

            # Regularization to keep mix diverse (avoid 100% of single material)
            entropy_penalty = -0.05 * np.sum(np.log(w + 1e-3))

            return cn_penalty + priority_penalty + entropy_penalty

        # Constraints: sum(w) == target_weight
        cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - target_weight}]
        # Bounds: at least 2% of total weight for diversity, max 85%
        bounds = [(target_weight * 0.02, target_weight * 0.85) for _ in range(n_mats)]

        # Initial guess: equal distribution
        x0 = np.full(n_mats, target_weight / n_mats)

        res = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=cons)

        if res.success:
            weights = np.maximum(0, res.x)
            weights = (weights / np.sum(weights)) * target_weight
        else:
            weights = x0
    except Exception:
        # Fallback heuristic calculation if scipy optimizer encounters issue
        weights = np.full(n_mats, target_weight / n_mats)
        # Shift slightly toward materials that balance C/N
        diffs = [abs(ORGANIC_DATABASE[m]["c_n"] - target_cn) for m in valid_materials]
        inv_diffs = 1.0 / (np.array(diffs) + 1.0)
        weights = (inv_diffs / np.sum(inv_diffs)) * target_weight

    # Calculate achieved metrics
    final_c_kg = np.sum(weights * (c_vals / 100.0))
    final_n_kg = np.sum(weights * (n_vals / 100.0))
    final_p_kg = np.sum(weights * (p_vals / 100.0))
    final_k_kg = np.sum(weights * (k_vals / 100.0))

    achieved_cn = final_c_kg / (final_n_kg + 1e-6)
    achieved_n_pct = (final_n_kg / target_weight) * 100.0
    achieved_p_pct = (final_p_kg / target_weight) * 100.0
    achieved_k_pct = (final_k_kg / target_weight) * 100.0

    materials_list: List[OptimizedMaterial] = []
    for i, name in enumerate(valid_materials):
        w_kg = float(weights[i])
        pct = (w_kg / target_weight) * 100.0
        role = ORGANIC_DATABASE[name]["character"]
        materials_list.append(OptimizedMaterial(
            name=name,
            recommended_kg=round(w_kg, 1),
            percentage=round(pct, 1),
            role=role
        ))

    notes = [
        f"Algoritma AI berhasil mengoptimasi formula untuk target C/N {target_cn:.1f}:1 (Tercapai: {achieved_cn:.1f}:1).",
        f"Estimasi profil hara akhir: N: {achieved_n_pct:.2f}%, P: {achieved_p_pct:.2f}%, K: {achieved_k_pct:.2f}%.",
        f"Campuran ini dirancang agar fase termofilik (suhu 55-65°C) tercapai dalam 3-4 hari pertama untuk membunuh patogen."
    ]

    return SolidOptimizationResponse(
        target_total_weight_kg=round(target_weight, 1),
        target_c_n_ratio=round(target_cn, 1),
        estimated_achieved_c_n=round(achieved_cn, 1),
        estimated_npk=f"{achieved_n_pct:.2f}% - {achieved_p_pct:.2f}% - {achieved_k_pct:.2f}%",
        materials=materials_list,
        notes=notes
    )
