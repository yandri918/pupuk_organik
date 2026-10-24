from app.models.schemas import EconomicsRequest, EconomicsResponse

def calculate_economics(req: EconomicsRequest) -> EconomicsResponse:
    vol = req.batch_volume
    if vol <= 0:
        raise ValueError("Volume batch harus lebih besar dari 0.")

    # 1. Total OPEX
    total_opex = (
        req.raw_material_cost +
        req.bioactivator_cost +
        req.labor_cost +
        req.energy_packaging_cost
    )

    # 2. CAPEX Depreciation per batch
    # Assume 4 batches per month
    monthly_depreciation = req.capex_equipment / max(1, req.depreciation_months)
    batch_depreciation = monthly_depreciation / 4.0

    # 3. Total Production Cost (COGS / HPP Total)
    total_cogs = total_opex + batch_depreciation

    # 4. HPP Unit
    hpp_unit = total_cogs / vol

    # 5. Revenue & Profit
    total_revenue = vol * req.target_selling_price
    gross_profit = total_revenue - total_opex
    net_profit = total_revenue - total_cogs

    profit_margin = (net_profit / total_revenue) * 100.0 if total_revenue > 0 else 0.0
    roi = (net_profit / total_cogs) * 100.0 if total_cogs > 0 else 0.0

    # 6. Break-Even Point (Units)
    unit_margin = req.target_selling_price - (total_opex / vol)
    if unit_margin > 0:
        bep_units = batch_depreciation / unit_margin
    else:
        bep_units = float('inf')

    # Feasibility Status
    if net_profit > 0 and profit_margin >= 25.0:
        status = "Sangat Layak (High Margin)"
    elif net_profit > 0:
        status = "Layak Beroperasi (Moderate Margin)"
    else:
        status = "Defisit / Perlu Penyesuaian Harga/Biaya"

    unit_name = "kg" if "padat" in req.fertilizer_type.lower() else "Liter / Botol"

    insights = [
        f"Harga Pokok Produksi (HPP): Rp {hpp_unit:,.0f} per {unit_name}.",
        f"Keuntungan bersih per batch ({vol:,.0f} {unit_name}): Rp {net_profit:,.0f} (Margin: {profit_margin:.1f}%).",
        f"Titik Impas (BEP) tercapai pada volume penjualan {bep_units:,.1f} {unit_name} per siklus batch."
    ]

    return EconomicsResponse(
        fertilizer_type=req.fertilizer_type,
        batch_volume=vol,
        total_opex=round(total_opex, 2),
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
