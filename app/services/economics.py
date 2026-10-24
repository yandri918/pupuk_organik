from app.models.schemas import EconomicsRequest, EconomicsResponse

def calculate_economics(req: EconomicsRequest) -> EconomicsResponse:
    vol = req.batch_volume
    if vol <= 0:
        raise ValueError("Volume batch harus lebih besar dari 0.")

    # 1. Variable Costs (Biaya Variabel Proporsional Terhadap Volume)
    # Meliputi: Bahan baku, bioaktivator/inokulan, dan energi/kemasan
    variable_opex = (
        req.raw_material_cost +
        req.bioactivator_cost +
        req.energy_packaging_cost
    )

    # 2. Fixed Costs per Batch (Biaya Tetap per Siklus Batch)
    # Meliputi: Upah tenaga kerja tetap per batch dan alokasi overhead operasional
    fixed_batch_cost = req.labor_cost + req.fixed_overhead_cost

    # 3. CAPEX Depreciation per batch (Dihitung berdasarkan siklus produksi bulanan aktual)
    batches_per_mo = max(0.5, req.batches_per_month)
    monthly_depreciation = req.capex_equipment / max(1, req.depreciation_months)
    batch_depreciation = monthly_depreciation / batches_per_mo

    # 4. Total Cost of Goods Sold (HPP Total per Batch)
    total_cogs = variable_opex + fixed_batch_cost + batch_depreciation

    # 5. HPP per Unit
    hpp_unit = total_cogs / vol

    # 6. Revenue & Profit
    total_revenue = vol * req.target_selling_price
    gross_profit = total_revenue - (variable_opex + fixed_batch_cost)
    net_profit = total_revenue - total_cogs

    profit_margin = (net_profit / total_revenue) * 100.0 if total_revenue > 0 else 0.0
    roi = (net_profit / total_cogs) * 100.0 if total_cogs > 0 else 0.0

    # 7. Akuntansi Break-Even Point (BEP Unit Berbasis Margin Kontribusi)
    # Variable cost per unit
    var_cost_per_unit = variable_opex / vol
    unit_contribution_margin = req.target_selling_price - var_cost_per_unit

    total_fixed_burden = fixed_batch_cost + batch_depreciation

    if unit_contribution_margin > 0:
        bep_units = total_fixed_burden / unit_contribution_margin
    else:
        # Harga jual di bawah biaya variabel per unit (defisit per unit)
        bep_units = float('inf')

    # Status Kelayakan Finansial
    if net_profit > 0 and profit_margin >= 25.0:
        status = "Sangat Layak (High Margin)"
    elif net_profit > 0:
        status = "Layak Beroperasi (Moderate Margin)"
    elif unit_contribution_margin <= 0:
        status = "Kritis: Harga jual di bawah biaya bahan variabel per unit"
    else:
        status = "Defisit: Volume penjualan belum menutup biaya tetap & depresiasi"

    unit_name = "kg" if "padat" in req.fertilizer_type.lower() else "Liter / Botol"

    insights = [
        f"Harga Pokok Produksi (HPP): Rp {hpp_unit:,.0f} per {unit_name}.",
        f"Margin Kontribusi Satuan: Rp {unit_contribution_margin:,.0f} per {unit_name} (Harga Jual - Biaya Variabel).",
        f"Keuntungan bersih per batch ({vol:,.0f} {unit_name}): Rp {net_profit:,.0f} (Margin Bersih: {profit_margin:.1f}%).",
        f"Titik Impas (BEP): {bep_units:,.1f} {unit_name} per siklus produksi (berdasarkan kapasitas {batches_per_mo:.1f} batch/bulan)."
    ]

    return EconomicsResponse(
        fertilizer_type=req.fertilizer_type,
        batch_volume=vol,
        variable_opex=round(variable_opex, 2),
        fixed_batch_cost=round(fixed_batch_cost, 2),
        batch_depreciation=round(batch_depreciation, 2),
        total_production_cost=round(total_cogs, 2),
        unit_cost_hpp=round(hpp_unit, 2),
        target_selling_price=req.target_selling_price,
        total_revenue=round(total_revenue, 2),
        gross_profit=round(gross_profit, 2),
        net_profit=round(net_profit, 2),
        profit_margin_pct=round(profit_margin, 2),
        roi_pct=round(roi, 2),
        break_even_units=round(bep_units, 1) if bep_units != float('inf') else -1.0,
        feasibility_status=status,
        insights=insights
    )
