from typing import Dict, List, Any, Optional
from app.models.schemas import (
    ChemicalFertilizerInput, FermentedChemicalPOCRequest, FermentedChemicalPOCResponse
)

# Database of standard chemical fertilizers used in agriculture and bio-fermentation
CHEMICAL_FERTILIZERS_CATALOG: Dict[str, Dict[str, Any]] = {
    "NPK Mutiara 16-16-16": {
        "N": 16.0,
        "P2O5": 16.0,
        "K2O": 16.0,
        "S": 0.0,
        "price_per_kg": 18000,
        "color": "#3b82f6",
        "type": "Majemuk Seimbang",
        "character": "Pupuk NPK premium mudah larut air. Sangat ideal untuk semua fase pertumbuhan."
    },
    "NPK Phonska 15-15-15": {
        "N": 15.0,
        "P2O5": 15.0,
        "K2O": 15.0,
        "S": 10.0,
        "price_per_kg": 13000,
        "color": "#8b5cf6",
        "type": "Majemuk Seimbang + Sulfur",
        "character": "Pupuk majemuk populer dengan kandungan Sulfur ekstra untuk kesuburan tanah."
    },
    "Urea (46-0-0)": {
        "N": 46.0,
        "P2O5": 0.0,
        "K2O": 0.0,
        "S": 0.0,
        "price_per_kg": 8500,
        "color": "#10b981",
        "type": "Tinggi Nitrogen (Vegetatif)",
        "character": "Sumber Nitrogen tercepat. Saat difermentasi, senyawa urea diubah menjadi N-organik yang tidak panas membakar akar."
    },
    "ZA (21-0-0 + 24S)": {
        "N": 21.0,
        "P2O5": 0.0,
        "K2O": 0.0,
        "S": 24.0,
        "price_per_kg": 7500,
        "color": "#06b6d4",
        "type": "Amonium & Sulfur Tinggi",
        "character": "Meningkatkan pembentukan klorofil daun, aroma tanaman hortikultura (bawang/cabai), dan kekebalan fisiologis."
    },
    "SP-36 (0-36-0)": {
        "N": 0.0,
        "P2O5": 36.0,
        "K2O": 0.0,
        "S": 5.0,
        "price_per_kg": 9000,
        "color": "#f59e0b",
        "type": "Tinggi Fosfat (Akar & Bunga)",
        "character": "Fosfat pekat. Fermentasi mikroba melarutkan fosfat lambat urai menjadi ion ortofosfat yang langsung diserap akar."
    },
    "KCl / MOP (0-0-60)": {
        "N": 0.0,
        "P2O5": 0.0,
        "K2O": 60.0,
        "S": 0.0,
        "price_per_kg": 14000,
        "color": "#ef4444",
        "type": "Tinggi Kalium (Bobot & Manis)",
        "character": "Kalium konsentrat tinggi pengisi bobot biji/buah, penguat dinding sel batang, dan ketahanan terhadap kekeringan."
    },
    "MKP (0-52-34)": {
        "N": 0.0,
        "P2O5": 52.0,
        "K2O": 34.0,
        "S": 0.0,
        "price_per_kg": 55000,
        "color": "#ec4899",
        "type": "Ultra Fosfat & Kalium",
        "character": "Pupuk foliar premium bebas Nitrogen untuk memicu bunga serempak dan mencegah kerontokan bakal buah."
    },
    "KNO3 Putih (13-0-45)": {
        "N": 13.0,
        "P2O5": 0.0,
        "K2O": 45.0,
        "S": 0.0,
        "price_per_kg": 38000,
        "color": "#6366f1",
        "type": "Kalium Nitrat Bebas Klor",
        "character": "Nitrat cepat serap dan kalium bebas klorin. Meningkatkan kadar gula brix buah, daya simpan, dan bobot panen."
    }
}

# Standard recipe presets calibrated for 100 Liter base drum
PRESET_CHEMICAL_FORMULAS = {
    "npk_mutiara_balanced": {
        "title": "POC Bio-NPK Mutiara 16-16-16 Universal (Formula Seimbang)",
        "category": "All-Purpose (Vegetatif & Generatif)",
        "description": "Mengubah garam NPK anorganik menjadi senyawa organo-kimia biologis siap serap dengan proteksi asam amino dan enzim.",
        "chemicals_100l": [
            {"name": "NPK Mutiara 16-16-16", "weight_kg": 5.0}
        ],
        "molasses_100l": 3.0,      # kg
        "coconut_water_100l": 10.0, # Liter
        "rice_water_100l": 10.0,    # Liter
        "bioactivator_100l": 1.0,   # Liter
        "water_100l": 60.0          # Liter
    },
    "urea_vegetatif_booster": {
        "title": "POC Bio-Vegetatif Daun Hijau & Anakan (Tinggi N & Sulfur)",
        "category": "Fase Pertumbuhan Awal / Vegetatif",
        "description": "Percepatan anakan padi, pembentukan klorofil sayuran daun, dan tunas baru tanpa risiko membakar perakaran.",
        "chemicals_100l": [
            {"name": "Urea (46-0-0)", "weight_kg": 3.0},
            {"name": "NPK Mutiara 16-16-16", "weight_kg": 2.0},
            {"name": "ZA (21-0-0 + 24S)", "weight_kg": 1.0}
        ],
        "molasses_100l": 3.0,
        "coconut_water_100l": 10.0,
        "rice_water_100l": 10.0,
        "bioactivator_100l": 1.0,
        "water_100l": 60.0
    },
    "generatif_pk_booster": {
        "title": "POC Bio-Generatif Bunga, Buah & Umbi (Tinggi P & K)",
        "category": "Fase Pembungaan & Pengisian Buah",
        "description": "Memicu primordia bunga, mencegah rontok pentil buah cabai/tomat/melon, dan memperpadat bulir padi.",
        "chemicals_100l": [
            {"name": "NPK Mutiara 16-16-16", "weight_kg": 2.5},
            {"name": "SP-36 (0-36-0)", "weight_kg": 2.0},
            {"name": "KCl / MOP (0-0-60)", "weight_kg": 2.0}
        ],
        "molasses_100l": 3.0,
        "coconut_water_100l": 15.0,
        "rice_water_100l": 5.0,
        "bioactivator_100l": 1.0,
        "water_100l": 60.0
    },
    "mkp_kno3_fruit_booster": {
        "title": "POC Sultan Booster Buah Manis Bebas Klor (MKP + KNO3)",
        "category": "Fase Pematangan & Pembesaran Buah Premium",
        "description": "Formula kalium nitrat dan fosfat larut air murni untuk melon, semangka, cabai, jeruk, dan durian.",
        "chemicals_100l": [
            {"name": "MKP (0-52-34)", "weight_kg": 2.0},
            {"name": "KNO3 Putih (13-0-45)", "weight_kg": 2.0},
            {"name": "NPK Mutiara 16-16-16", "weight_kg": 2.0}
        ],
        "molasses_100l": 3.0,
        "coconut_water_100l": 15.0,
        "rice_water_100l": 5.0,
        "bioactivator_100l": 1.0,
        "water_100l": 60.0
    }
}

def get_chemical_catalog() -> List[Dict[str, Any]]:
    """Return catalog of available chemical fertilizers."""
    catalog = []
    for name, data in CHEMICAL_FERTILIZERS_CATALOG.items():
        catalog.append({
            "name": name,
            "type": data["type"],
            "n_pct": data["N"],
            "p2o5_pct": data["P2O5"],
            "k2o_pct": data["K2O"],
            "s_pct": data.get("S", 0.0),
            "price_per_kg": data["price_per_kg"],
            "character": data["character"],
            "color": data["color"]
        })
    return catalog

def calculate_fermented_chemical_poc(req: FermentedChemicalPOCRequest) -> FermentedChemicalPOCResponse:
    drum_vol = float(req.drum_volume_liters)
    if drum_vol <= 0:
        raise ValueError("Volume drum harus lebih besar dari 0 Liter.")

    # 15% headspace safety margin for gas accumulation during microbial fermentation
    effective_vol = round(drum_vol * 0.85, 1)
    headspace_vol = round(drum_vol * 0.15, 1)

    scale_factor = drum_vol / 100.0

    preset_key = req.recipe_preset or "npk_mutiara_balanced"
    is_custom = preset_key == "custom" or (req.chemical_fertilizers is not None and len(req.chemical_fertilizers) > 0 and preset_key == "custom")

    # 1. Resolve chemical fertilizers list
    chemical_items: List[Dict[str, Any]] = []
    if is_custom and req.chemical_fertilizers:
        recipe_title = "POC Formulasi Kimia Kustom Terfermentasi"
        for item in req.chemical_fertilizers:
            w = float(item.weight_kg)
            if w > 0:
                spec = CHEMICAL_FERTILIZERS_CATALOG.get(item.name, {
                    "N": 15.0, "P2O5": 15.0, "K2O": 15.0, "S": 0.0, "price_per_kg": 15000, "type": "Kustom"
                })
                chemical_items.append({
                    "name": item.name,
                    "weight_kg": round(w, 2),
                    "n_pct": spec.get("N", 0.0),
                    "p2o5_pct": spec.get("P2O5", 0.0),
                    "k2o_pct": spec.get("K2O", 0.0),
                    "s_pct": spec.get("S", 0.0),
                    "price_per_kg": spec.get("price_per_kg", 15000),
                    "cost": round(w * spec.get("price_per_kg", 15000))
                })
        molasses_kg = round(3.0 * scale_factor, 2)
        coconut_water_l = round(10.0 * scale_factor, 1)
        rice_water_l = round(10.0 * scale_factor, 1)
        bioactivator_l = round(1.0 * scale_factor, 2)
        water_l = round(max(0.0, effective_vol - (coconut_water_l + rice_water_l + bioactivator_l + molasses_kg)), 1)
    else:
        preset = PRESET_CHEMICAL_FORMULAS.get(preset_key, PRESET_CHEMICAL_FORMULAS["npk_mutiara_balanced"])
        recipe_title = preset["title"]
        for c in preset["chemicals_100l"]:
            spec = CHEMICAL_FERTILIZERS_CATALOG.get(c["name"], {})
            w = round(c["weight_kg"] * scale_factor, 2)
            chemical_items.append({
                "name": c["name"],
                "weight_kg": w,
                "n_pct": spec.get("N", 0.0),
                "p2o5_pct": spec.get("P2O5", 0.0),
                "k2o_pct": spec.get("K2O", 0.0),
                "s_pct": spec.get("S", 0.0),
                "price_per_kg": spec.get("price_per_kg", 15000),
                "cost": round(w * spec.get("price_per_kg", 15000))
            })
        molasses_kg = round(preset["molasses_100l"] * scale_factor, 2)
        coconut_water_l = round(preset["coconut_water_100l"] * scale_factor, 1)
        rice_water_l = round(preset["rice_water_100l"] * scale_factor, 1)
        bioactivator_l = round(preset["bioactivator_100l"] * scale_factor, 2)
        water_l = round(preset["water_100l"] * scale_factor, 1)

    # 2. Biological carrier ingredients
    starter_name = req.starter_bioactivator or "ROTAN Rumen Sapi / EM4"
    bio_items = [
        {
            "name": "Molase (Tetes Tebu) / Gula Merah",
            "amount": molasses_kg,
            "unit": "kg",
            "role": "Sumber C-Organik & Energi Glukosa Makanan Mikroba Pengurai",
            "price_per_unit": 12000,
            "cost": round(molasses_kg * 12000)
        },
        {
            "name": "Air Kelapa Tua Murni",
            "amount": coconut_water_l,
            "unit": "Liter",
            "role": "Sumber Kalium Alami, Fitohormon Sitokinin & Asam Amino Bebas",
            "price_per_unit": 2000,
            "cost": round(coconut_water_l * 2000)
        },
        {
            "name": "Air Leri (Cucian Beras) / Rebusan Dedak",
            "amount": rice_water_l,
            "unit": "Liter",
            "role": "Vitamin B-Kompleks & Prebiotik Starter Mikroba",
            "price_per_unit": 500,
            "cost": round(rice_water_l * 500)
        },
        {
            "name": f"Bioaktivator Inokulan ({starter_name})",
            "amount": bioactivator_l,
            "unit": "Liter",
            "role": "Kultur Konsorsium Bakteri Pelarut Hara & Penghelat Senyawa Kimia",
            "price_per_unit": 25000,
            "cost": round(bioactivator_l * 25000)
        },
        {
            "name": "Air Bersih Bebas Kaporit",
            "amount": water_l,
            "unit": "Liter",
            "role": "Media Pelarut Utama Fermentasi",
            "price_per_unit": 0,
            "cost": 0
        }
    ]

    # 3. Nutrient and Salinity Calculations
    total_chem_kg = sum(c["weight_kg"] for c in chemical_items)
    salinity_g_per_l = round((total_chem_kg * 1000.0) / effective_vol, 1) if effective_vol > 0 else 0.0

    # Osmotic threshold check: Microbial tolerance in aqueous fermentation is typically <80 g/L (8% salt)
    if salinity_g_per_l <= 60.0:
        osmotic_status = f"Sangat Aman ({salinity_g_per_l} g/L): Tekanan osmotik optimal bagi perkembangbiakan mikroba pengurai."
        is_safe = True
    elif salinity_g_per_l <= 80.0:
        osmotic_status = f"Aman Terkendali ({salinity_g_per_l} g/L): Dalam batas toleransi osmotik inokulan bakteri Lactobacillus & ragi."
        is_safe = True
    else:
        osmotic_status = f"Peringatan Salinitas ({salinity_g_per_l} g/L): Garam kimia terlalu pekat (>80 g/L). Berisiko menidurkan sebagian mikroba. Disarankan tambah volume air."
        is_safe = False

    total_n_kg = sum(c["weight_kg"] * (c["n_pct"] / 100.0) for c in chemical_items)
    total_p2o5_kg = sum(c["weight_kg"] * (c["p2o5_pct"] / 100.0) for c in chemical_items)
    total_k2o_kg = sum(c["weight_kg"] * (c["k2o_pct"] / 100.0) for c in chemical_items)
    total_s_kg = sum(c["weight_kg"] * (c["s_pct"] / 100.0) for c in chemical_items)

    # Dissolved nutrient concentration in liquid (% w/v basis)
    n_pct = round((total_n_kg / effective_vol) * 100.0, 2)
    p2o5_pct = round((total_p2o5_kg / effective_vol) * 100.0, 2)
    k2o_pct = round((total_k2o_kg / effective_vol) * 100.0, 2)
    s_pct = round((total_s_kg / effective_vol) * 100.0, 2)

    npk_label = f"N: {n_pct:.2f}% | P2O5: {p2o5_pct:.2f}% | K2O: {k2o_pct:.2f}%"
    if s_pct > 0:
        npk_label += f" | S: {s_pct:.2f}%"
    npk_label += " (Bio-Chelated Liquid)"

    # 4. Economics & Cost-Benefit
    chem_cost = sum(c["cost"] for c in chemical_items)
    bio_cost = sum(b["cost"] for b in bio_items)
    total_cost = chem_cost + bio_cost
    cost_per_liter = round(total_cost / effective_vol, 0) if effective_vol > 0 else 0.0

    # Conventional comparison: Buying commercial chemical liquid fertilizer (Rp 40.000 - 65.000 / Liter)
    commercial_equiv_cost = round(effective_vol * 45000)
    savings_rp = max(0, commercial_equiv_cost - total_cost)
    savings_pct = round((savings_rp / commercial_equiv_cost) * 100.0, 1) if commercial_equiv_cost > 0 else 0.0

    # 5. SOP & Protocols
    protocol = [
        "Larutkan pupuk kimia secara bertahap dalam ember terpisah berisi 10-15 Liter air hingga benar-benar larut (tidak ada butiran kasar menggumpal).",
        "Dalam ember lain, campurkan molase (gula merah cair), air kelapa tua, air leri, dan bioaktivator inokulan hingga homogen.",
        "Tuangkan larutan pupuk kimia dan larutan biologis secara bersamaan ke dalam drum fermentasi.",
        f"Tambahkan air bersih hingga total volume cairan mencapai {effective_vol} Liter (sisakan ruang kosong {headspace_vol} Liter di bagian atas untuk ruang ekspansi gas fermentasi).",
        "Aduk tumpukan cairan searah jarum jam selama 3-5 menit.",
        "Tutup drum secara rapat. Pasang selang aerasi (airlock) yang diarahkan ke botol air mineral bekas untuk membuang gas CO2 otomatis tanpa masuknya udara luar.",
        "Jika tanpa selang aerasi, buka tutup drum selama 2 menit setiap 2 hari sekali untuk membuang desisan gas lalu tutup rapat kembali.",
        f"Fermentasi berlangsung selama {req.fermentation_days} hari di tempat teduh terhindar dari sinar matahari langsung."
    ]

    indicators = [
        "Aroma asam manis segar khas fermentasi alkoholik/tape (bau menyengat kimia/amonia tajam sudah hilang).",
        "Warna cairan berubah menjadi coklat tua keemasan atau hijau tua jernih merata.",
        "Desisan gas CO2 sudah melambat atau mereda (menandakan proses asimilasi hara telah stabil).",
        "Nilai pH cairan turun dan stabil pada rentang asam-netral (pH 5.0 - 6.5).",
        "Larutan dingin pada suhu ruang, tidak ada endapan kerak kasar."
    ]

    guide = {
        "foliar_spray": {
            "dose": "3 - 5 ml per Liter air (50 - 80 ml per tangki semprot 16 Liter)",
            "timing": "Pagi hari pukul 06.00 - 09.00 saat stomata daun terbuka sempurna",
            "filter_note": "Wajib disaring dengan kain kasa halus sebelum dituang ke tangki semprot agar nozzle tidak tersumbat."
        },
        "root_drench": {
            "dose": "10 - 20 ml per Liter air (200 - 300 ml per ember siram 15 Liter)",
            "volume_per_plant": "200 - 250 ml larutan encer per lubang tanam",
            "interval": "Aplikasi setiap 7 - 10 hari sekali di sekeliling perakaran"
        },
        "agronomic_benefits": [
            "Hara anorganik terkelat (chelated) oleh asam amino dan asam organik, mencegah pencucian air hujan (leaching).",
            "Tidak membakar daun dan perakaran tanaman (burn-free).",
            "Melipatgandakan efisiensi serapan pupuk kimia hingga 200-300%, menghemat belanja pupuk hingga 60-70%.",
            "Menjaga populasi cacing tanah dan mikoriza alami tetap aktif."
        ]
    }

    return FermentedChemicalPOCResponse(
        recipe_title=recipe_title,
        preset_id=preset_key,
        drum_volume_liters=drum_vol,
        effective_liquid_liters=effective_vol,
        headspace_liters=headspace_vol,
        osmotic_safety_status=osmotic_status,
        is_osmotic_safe=is_safe,
        salinity_grams_per_liter=salinity_g_per_l,
        chemical_ingredients=chemical_items,
        biological_ingredients=bio_items,
        estimated_npk_label=npk_label,
        dissolved_nutrients={
            "n_pct": n_pct,
            "p2o5_pct": p2o5_pct,
            "k2o_pct": k2o_pct,
            "s_pct": s_pct,
            "total_n_kg": round(total_n_kg, 2),
            "total_p2o5_kg": round(total_p2o5_kg, 2),
            "total_k2o_kg": round(total_k2o_kg, 2),
            "total_s_kg": round(total_s_kg, 2)
        },
        estimated_total_cost=total_cost,
        estimated_cost_per_liter=cost_per_liter,
        conventional_comparison={
            "commercial_chemical_poc_equiv_cost": commercial_equiv_cost,
            "our_production_cost": total_cost,
            "cost_savings_rp": savings_rp,
            "cost_savings_pct": savings_pct
        },
        fermentation_protocol=protocol,
        maturation_indicators=indicators,
        application_guide=guide
    )
