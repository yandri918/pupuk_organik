import math
from typing import Dict, List, Any
from app.models.schemas import (
    SolidCalculationRequest, SolidCalculationResponse,
    MaterialDetail, SNICheckResult
)

# Stoichiometric conversion factors (Elemental to Oxide)
P_TO_P2O5 = 2.2914
K_TO_K2O = 1.2046

# Scientific nutrient database
# All nutrient percentages (carbon, n, p, k) are defined on Dry Weight Basis (% DW).
# moisture_typical is percentage of water in wet fresh material (% as-is).
ORGANIC_DATABASE: Dict[str, Dict[str, Any]] = {
    "Kotoran Sapi": {
        "carbon": 36.0,
        "n": 1.40,
        "p": 0.35,  # elemental P (DW) -> ~0.80% P2O5
        "k": 1.00,  # elemental K (DW) -> ~1.20% K2O
        "c_n": 25.7,
        "moisture_typical": 65.0,
        "character": "Dingin, kaya serat, sangat baik untuk pembenah struktur tanah liat/berpasir.",
        "category": "Kotoran Ternak"
    },
    "Kotoran Kambing/Domba": {
        "carbon": 40.0,
        "n": 2.00,
        "p": 0.52,  # elemental P -> ~1.20% P2O5
        "k": 1.50,  # elemental K -> ~1.80% K2O
        "c_n": 20.0,
        "moisture_typical": 50.0,
        "character": "Kering berbentuk butiran, nutrisi seimbang, cocok untuk pupuk dasar tanaman buah.",
        "category": "Kotoran Ternak"
    },
    "Kotoran Ayam (Broiler/Petelur)": {
        "carbon": 35.0,
        "n": 3.20,
        "p": 1.13,  # elemental P -> ~2.60% P2O5
        "k": 1.33,  # elemental K -> ~1.60% K2O
        "c_n": 10.9,
        "moisture_typical": 45.0,
        "character": "Panas, amonia tinggi, cepat terurai, wajib dicampur bahan tinggi karbon (sekam/jerami).",
        "category": "Kotoran Ternak"
    },
    "Kotoran Burung Puyuh": {
        "carbon": 34.0,
        "n": 3.80,
        "p": 1.40,  # elemental P -> ~3.20% P2O5
        "k": 1.74,  # elemental K -> ~2.10% K2O
        "c_n": 8.9,
        "moisture_typical": 40.0,
        "character": "Sangat pekat, butuh waktu fermentasi lebih lama (21-30 hari) untuk sanitasi.",
        "category": "Kotoran Ternak"
    },
    "Kotoran Kelinci (Padat)": {
        "carbon": 38.0,
        "n": 2.40,
        "p": 0.65,  # elemental P -> ~1.50% P2O5
        "k": 0.91,  # elemental K -> ~1.10% K2O
        "c_n": 15.8,
        "moisture_typical": 45.0,
        "character": "Kualitas tinggi, dingin, aman, sangat disukai cacing tanah.",
        "category": "Kotoran Ternak"
    },
    "Guano (Kotoran Kelelawar)": {
        "carbon": 22.0,
        "n": 2.00,
        "p": 4.58,  # elemental P -> ~10.50% P2O5
        "k": 1.25,  # elemental K -> ~1.50% K2O
        "c_n": 11.0,
        "moisture_typical": 25.0,
        "character": "Sumber fosfor alami tinggi untuk memicu pembungaan dan pembuahan lebat.",
        "category": "Kotoran Ternak"
    },
    "Sekam Padi Mentah": {
        "carbon": 42.0,
        "n": 0.50,
        "p": 0.11,  # elemental P -> ~0.25% P2O5
        "k": 0.46,  # elemental K -> ~0.55% K2O
        "c_n": 84.0,
        "moisture_typical": 12.0,
        "character": "Porositas tinggi, sumber karbon lambat urai, menggemburkan media agar tidak padat.",
        "category": "Bahan Karbon / Bulking Agent"
    },
    "Arang Sekam Padi": {
        "carbon": 38.0,
        "n": 0.30,
        "p": 0.15,  # elemental P -> ~0.35% P2O5
        "k": 1.08,  # elemental K -> ~1.30% K2O
        "c_n": 126.0,
        "moisture_typical": 10.0,
        "character": "Biochar alami! Memperbaiki KTK tanah, rumah bagi mikroba baik, menaikkan pH tanah masam.",
        "category": "Bahan Karbon / Bulking Agent"
    },
    "Jerami Padi (Cacah)": {
        "carbon": 40.0,
        "n": 0.70,
        "p": 0.09,  # elemental P -> ~0.20% P2O5
        "k": 1.33,  # elemental K -> ~1.60% K2O
        "c_n": 57.1,
        "moisture_typical": 20.0,
        "character": "Kaya Kalium alami & silika, menstabilkan kelembaban tumpukan kompos.",
        "category": "Bahan Karbon / Bulking Agent"
    },
    "Dedak Padi Halus (Katul)": {
        "carbon": 44.0,
        "n": 2.10,
        "p": 0.87,  # elemental P -> ~2.00% P2O5
        "k": 0.91,  # elemental K -> ~1.10% K2O
        "c_n": 21.0,
        "moisture_typical": 12.0,
        "character": "Pakan super bagi mikroorganisme pengurai. Mempercepat lonjakan suhu termofilik.",
        "category": "Akselerator / Pakan Mikroba"
    },
    "Serbuk Gergaji Kayu Lunak": {
        "carbon": 50.0,
        "n": 0.15,
        "p": 0.04,
        "k": 0.17,
        "c_n": 333.0,
        "moisture_typical": 15.0,
        "character": "Sangat tinggi lignin & selulosa. Gunakan sedikit sebagai penyerap cairan rembesan.",
        "category": "Bahan Karbon / Bulking Agent"
    },
    "Abu Kayu Dapur": {
        "carbon": 5.0,
        "n": 0.00,
        "p": 0.87,  # elemental P -> ~2.00% P2O5
        "k": 4.15,  # elemental K -> ~5.00% K2O
        "c_n": 0.0,
        "moisture_typical": 5.0,
        "character": "Sumber Kalium instan dan penetral asam alami (pH basa tinggi 9-10).",
        "category": "Mineral Alami"
    },
    "Dolomit (Kapur Pertanian)": {
        "carbon": 0.0,
        "n": 0.00,
        "p": 0.00,
        "k": 0.00,
        "c_n": 0.0,
        "moisture_typical": 2.0,
        "character": "Penyumbang Kalsium (CaO ~30%) dan Magnesium (MgO ~18%), menstabilkan pH.",
        "category": "Mineral Alami"
    },
    "Cangkang Telur (Tumbuk)": {
        "carbon": 12.0,
        "n": 0.60,
        "p": 0.13,  # elemental P -> ~0.30% P2O5
        "k": 0.17,  # elemental K -> ~0.20% K2O
        "c_n": 20.0,
        "moisture_typical": 5.0,
        "character": "Kaya Kalsium Karbonat (>90%), mencegah penyakit fisiologis pada tanaman.",
        "category": "Mineral Alami"
    }
}

SOLID_PRESET_RECIPES = [
    {
        "id": "bokashi-rotan-1ha",
        "title": "Bokashi Super ROTAN (Skala Lahan 1 Hektar)",
        "summary": "Resep legendaris mencukupi kebutuhan 16 unsur hara makro & mikro tanaman pangan/hortikultura.",
        "materials": [
            {"name": "Kotoran Kambing/Domba", "qty": "1000 kg (1 Ton)"},
            {"name": "Jerami Padi (Cacah)", "qty": "1000 kg (1 Ton)"},
            {"name": "Sekam Padi Mentah", "qty": "300 kg"},
            {"name": "Dedak Padi Halus (Katul)", "qty": "50 kg"},
            {"name": "Dolomit (Kapur Pertanian)", "qty": "100 kg"},
            {"name": "Bioaktivator ROTAN", "qty": "4 Liter"},
            {"name": "Air Kelapa / Air Bersih", "qty": "Secukupnya (mamel 30-40%)"}
        ],
        "fermentation_time": "5 - 7 Hari",
        "steps": [
            "Campur rata semua bahan padat (Kohe, Dolomit, Dedak, Sekam, Jerami cacah).",
            "Larutkan 4 Liter Bioaktivator ROTAN ke dalam air kelapa/air bersih.",
            "Siramkan larutan secara bertahap ke tumpukan bahan padat sambil diaduk hingga kadar air 30-40% (mamel: digenggam mengepal, disentuh buyar, tidak menetes).",
            "Tutup rapat dengan terpal kedap udara di tempat teduh (tidak terkena sinar matahari langsung).",
            "Cek suhu hari ke-2 s/d ke-4 (harus hangat-panas 50-60°C). Lakukan pembalikan jika suhu melebihi 65°C.",
            "Panen di hari ke 5-7 saat suhu sudah turun dingin dan berbau harum tape."
        ]
    },
    {
        "id": "bokashi-ayam-sayuran",
        "title": "Bokashi Kohe Ayam N-Tinggi (Spesialis Sayuran Daun)",
        "summary": "Formula percepatan pertumbuhan vegetatif untuk bayam, kangkung, pakcoy, selada, dan sawi.",
        "materials": [
            {"name": "Kotoran Ayam (Broiler/Petelur)", "qty": "1000 kg"},
            {"name": "Sekam Padi Mentah / Serbuk Gergaji", "qty": "500 kg (Wajib tinggi penyerap amonia)"},
            {"name": "Dolomit (Kapur Pertanian)", "qty": "100 kg"},
            {"name": "Dedak Padi Halus (Katul)", "qty": "30 kg"},
            {"name": "Decomposer (EM4/ROTAN)", "qty": "2 Liter"}
        ],
        "fermentation_time": "10 - 14 Hari",
        "steps": [
            "Hamparkan kotoran ayam lalu taburi sekam padi untuk mengikat amonia berlebih.",
            "Taburkan dolomit dan dedak halus secara merata.",
            "Siramkan larutan dekomposer yang telah diaktifkan dengan air gula/molase.",
            "Aduk tumpukan secara bolak-balik sampai homogen.",
            "Tutup dengan terpal. Lakukan pembalikan tiap 3 hari sekali karena kohe ayam menghasilkan panas sangat tinggi.",
            "Matang ditandai bau amonia pesing hilang berganti wangi fermentasi tanah hutan."
        ]
    },
    {
        "id": "bokashi-guano-buah",
        "title": "Bokashi Guano P-Tinggi (Spesialis Bunga & Buah)",
        "summary": "Formulasi emas hitam dengan kandungan Fosfat & Kalium tinggi untuk cabai, tomat, melon, durian.",
        "materials": [
            {"name": "Guano (Kotoran Kelelawar)", "qty": "500 kg"},
            {"name": "Kotoran Kambing/Domba", "qty": "500 kg"},
            {"name": "Arang Sekam Padi", "qty": "300 kg"},
            {"name": "Abu Kayu Dapur", "qty": "50 kg"},
            {"name": "Dedak Padi Halus (Katul)", "qty": "30 kg"}
        ],
        "fermentation_time": "10 - 14 Hari",
        "steps": [
            "Campurkan guano dan kotoran kambing secara merata.",
            "Tambahkan arang sekam dan abu kayu untuk suplai Kalium dan Silika tinggi.",
            "Inokulasikan bakteri pelarut fosfat (Pseudomonas / Trichoderma).",
            "Jaga kadar air 40-50%.",
            "Fermentasikan selama 14 hari dengan pembalikan pada hari ke-4 dan hari ke-8."
        ]
    },
    {
        "id": "bokashi-sapi-pembenah",
        "title": "Bokashi Sapi Humus Dingin (Soil Conditioner / Pembenah Tanah)",
        "summary": "Pemulih kesuburan fisik, biologi, dan kimia untuk tanah kritis, tandus, keras, atau terdegradasi.",
        "materials": [
            {"name": "Kotoran Sapi", "qty": "1000 kg"},
            {"name": "Jerami Padi (Cacah)", "qty": "500 kg"},
            {"name": "Arang Sekam Padi", "qty": "200 kg"},
            {"name": "Dolomit (Kapur Pertanian)", "qty": "50 kg"},
            {"name": "Bakteri Selulolitik & Trichoderma", "qty": "1 Liter"}
        ],
        "fermentation_time": "14 - 21 Hari",
        "steps": [
            "Cacah jerami padi menjadi ukuran 3-5 cm agar bakteri selulolitik mudah mencerna.",
            "Campurkan kotoran sapi, jerami, dan arang sekam.",
            "Larutkan dekomposer dan taburkan biang jamur Trichoderma secara merata saat pencampuran.",
            "Atur kadar air hingga 40-50%.",
            "Tutup terpal dan diamkan. Suhu tumpukan akan stabil di rentang hangat mesofilik-termofilik.",
            "Menghasilkan humus hitam gembur yang tahan lama di dalam tanah."
        ]
    }
]

def calculate_solid_fertilizer(req: SolidCalculationRequest) -> SolidCalculationResponse:
    total_wet_weight = sum(m.weight_kg for m in req.materials)
    if total_wet_weight <= 0:
        raise ValueError("Total berat bahan harus lebih besar dari 0 kg.")

    total_dry_weight = 0.0
    total_water_kg = req.moisture_added_liters or 0.0

    total_c_kg = 0.0
    total_n_kg = 0.0
    total_p_elem_kg = 0.0
    total_k_elem_kg = 0.0

    breakdown: List[MaterialDetail] = []

    for mat in req.materials:
        db = ORGANIC_DATABASE.get(mat.name)
        if not db:
            c_val, n_val, p_val, k_val, cn_val, moist, desc = 30.0, 1.0, 0.22, 0.83, 30.0, 50.0, "Bahan Organik Umum"
        else:
            c_val = db["carbon"]
            n_val = db["n"]
            p_val = db["p"]
            k_val = db["k"]
            cn_val = db["c_n"]
            moist = db["moisture_typical"]
            desc = db["character"]

        # Mass Balance: Convert fresh wet weight to dry matter
        mat_wet_kg = mat.weight_kg
        dry_fraction = max(0.01, 1.0 - (moist / 100.0))
        mat_dry_kg = mat_wet_kg * dry_fraction
        mat_water_kg = mat_wet_kg * (moist / 100.0)

        total_dry_weight += mat_dry_kg
        total_water_kg += mat_water_kg

        # Nutrient mass (Dry Weight Basis)
        c_kg = mat_dry_kg * (c_val / 100.0)
        n_kg = mat_dry_kg * (n_val / 100.0)
        p_kg = mat_dry_kg * (p_val / 100.0)
        k_kg = mat_dry_kg * (k_val / 100.0)

        total_c_kg += c_kg
        total_n_kg += n_kg
        total_p_elem_kg += p_kg
        total_k_elem_kg += k_kg

        breakdown.append(MaterialDetail(
            name=mat.name,
            weight_wet_kg=round(mat_wet_kg, 2),
            moisture_pct=round(moist, 1),
            weight_dry_kg=round(mat_dry_kg, 2),
            carbon_pct_dw=round(c_val, 2),
            nitrogen_pct_dw=round(n_val, 2),
            phosphorus_pct_dw=round(p_val, 2),
            potassium_pct_dw=round(k_val, 2),
            carbon_kg=round(c_kg, 3),
            nitrogen_kg=round(n_kg, 3),
            phosphorus_kg=round(p_kg, 3),
            potassium_kg=round(k_kg, 3),
            c_n_ratio=round(cn_val, 1),
            function_desc=desc
        ))

    # Calculate initial mixture moisture content
    initial_moisture_pct = (total_water_kg / (total_wet_weight + (req.moisture_added_liters or 0.0))) * 100.0

    # Convert elemental P to P2O5 and K to K2O
    total_p2o5_kg = total_p_elem_kg * P_TO_P2O5
    total_k2o_kg = total_k_elem_kg * K_TO_K2O

    # Dry basis percentages (Standard Laboratory & SNI Reporting)
    dry_c_pct = (total_c_kg / total_dry_weight) * 100.0 if total_dry_weight > 0 else 0.0
    dry_n_pct = (total_n_kg / total_dry_weight) * 100.0 if total_dry_weight > 0 else 0.0
    dry_p2o5_pct = (total_p2o5_kg / total_dry_weight) * 100.0 if total_dry_weight > 0 else 0.0
    dry_k2o_pct = (total_k2o_kg / total_dry_weight) * 100.0 if total_dry_weight > 0 else 0.0

    initial_c_n = total_c_kg / total_n_kg if total_n_kg > 0 else 0.0

    # Fermentation dynamic decay modeling (Theoretical Kinetic Curve)
    days = req.fermentation_days or 0
    decay_factor = math.exp(-0.035 * days)
    target_stable_cn = 12.5
    current_c_n = target_stable_cn + (initial_c_n - target_stable_cn) * decay_factor
    current_c_n = max(10.0, current_c_n)

    # Fermentation phase and temperature modeling
    if days == 0:
        phase = "Hari 0: Persiapan Campuran (Inokulasi Awal)"
        temp_range = "25 - 30 °C (Suhu Ruang)"
    elif 1 <= days <= 3:
        phase = "Fase 1: Mesofilik Awal (Akselerasi Mikroba)"
        temp_range = "35 - 45 °C"
    elif 4 <= days <= 12:
        phase = "Fase 2: Termofilik Puncak (Sanitasi Patogen & Penguraian Serat)"
        temp_range = "55 - 65 °C"
    elif 13 <= days <= 20:
        phase = "Fase 3: Pendinginan & Humifikasi (Penurunan Suhu)"
        temp_range = "35 - 45 °C"
    else:
        phase = "Fase 4: Pematangan Stabil (Kompos Siap Panen)"
        temp_range = "Suhu Ruang / Air Tanah (< 32 °C)"

    # Label NPK (Dry Weight Basis, P2O5 & K2O)
    npk_label = f"N-P2O5-K2O (Basis Kering): {dry_n_pct:.2f}% - {dry_p2o5_pct:.2f}% - {dry_k2o_pct:.2f}%"

    # Suitability & Recommendations
    recommendations = []
    if initial_c_n > 35:
        recommendations.append("C/N Rasio Awal Terlalu Tinggi (>35:1): Tambahkan kotoran ternak ayam/puyuh atau dedak padi untuk memacu pertumbuhan bakteri pengurai.")
    elif initial_c_n < 20:
        recommendations.append("C/N Rasio Awal Terlalu Rendah (<20:1): Campuran terlalu banyak nitrogen (risiko penguapan gas amonia berlebih). Tambahkan sekam padi atau jerami kering.")
    else:
        recommendations.append("C/N Rasio Awal Ideal (20:1 - 35:1): Fermentasi akan berjalan optimal tanpa bau busuk amonia.")

    if initial_moisture_pct > 65.0:
        recommendations.append("Kadar Air Awal Terlalu Basah (>65%): Risiko kondisi anaerobik berbau busuk. Tambahkan sekam mentah kering untuk aerasi.")
    elif initial_moisture_pct < 40.0:
        recommendations.append("Kadar Air Awal Kurang (<40%): Mikroorganisme melambat. Siramkan air bioaktivator hingga tumpukan berkelembaban mamel (50-60%).")
    else:
        recommendations.append("Kadar Air Campuran Ideal (40-60%): Kelembaban optimal untuk fase termofilik mikroba.")

    if dry_n_pct >= 2.0:
        suitability = "Kaya Nitrogen (Vegetatif): Sangat baik untuk sayuran daun, persemaian bibit, dan pemicu anakan padi."
    elif dry_p2o5_pct >= 2.0 or dry_k2o_pct >= 2.0:
        suitability = "Kaya Fosfor & Kalium (Generatif): Sangat baik untuk fase pembungaan, pembesaran buah cabai, tomat, dan sawit."
    else:
        suitability = "Kompos Seimbang / Pembenah Tanah: Memperbaiki KTK tanah, retensi air, dan struktur tanah tandus."

    # SNI 19-7030-2004 Evaluation (Strict Bounds Check)
    sni_eval: List[SNICheckResult] = []

    # 1. C/N Ratio (Standard 10 - 20)
    if 10.0 <= current_c_n <= 20.0:
        cn_status = "Lolos SNI"
        cn_note = "Rasio C/N berada dalam rentang ideal kematangan kompos (10-20)."
    elif current_c_n > 20.0:
        cn_status = "Perlu Fermentasi Lanjutan"
        cn_note = f"C/N saat ini ({current_c_n:.1f}) di atas 20. Perlu waktu dekomposisi lanjutan agar tidak terjadi imobilisasi nitrogen di tanah."
    else:
        cn_status = "Di Bawah Batas Ideal (<10)"
        cn_note = "C/N di bawah 10 menunjukkan mineralisasi sangat lanjut."

    sni_eval.append(SNICheckResult(
        parameter="Rasio C/N",
        measured_value=round(current_c_n, 1),
        standard_range="10 - 20",
        unit="Rasio",
        status=cn_status,
        note=cn_note
    ))

    # 2. Karbon Organik (Standard SNI 19-7030-2004: 9.80 - 32.00%)
    if 9.80 <= dry_c_pct <= 32.00:
        c_status = "Lolos SNI"
        c_note = "Kadar C-Organik memenuhi rentang baku mutu SNI (9.80 - 32.00%)."
    elif dry_c_pct > 32.00:
        c_status = "Melebihi Batas SNI (>32%)"
        c_note = f"C-Organik ({dry_c_pct:.1f}%) di atas 32%. Menandakan bahan mentah belum terhumifikasi sempurna."
    else:
        c_status = "Kurang dari Batas SNI (<9.80%)"
        c_note = f"C-Organik ({dry_c_pct:.1f}%) di bawah 9.80%. Nilai pembenah tanah rendah."

    sni_eval.append(SNICheckResult(
        parameter="C-Organik (Basis Kering)",
        measured_value=round(dry_c_pct, 2),
        standard_range="9.80 - 32.00",
        unit="%",
        status=c_status,
        note=c_note
    ))

    # 3. Nitrogen Total (N >= 0.40%)
    n_status = "Lolos SNI" if dry_n_pct >= 0.40 else "Kurang dari Standar (<0.40%)"
    sni_eval.append(SNICheckResult(
        parameter="Nitrogen Total (N)",
        measured_value=round(dry_n_pct, 2),
        standard_range="≥ 0.40",
        unit="%",
        status=n_status,
        note="Standar minimum SNI 19-7030-2004 adalah 0.40%."
    ))

    # 4. Fosfor Total (P2O5 >= 0.10%)
    p_status = "Lolos SNI" if dry_p2o5_pct >= 0.10 else "Kurang dari Standar (<0.10%)"
    sni_eval.append(SNICheckResult(
        parameter="Fosfor Total (P2O5)",
        measured_value=round(dry_p2o5_pct, 2),
        standard_range="≥ 0.10",
        unit="%",
        status=p_status,
        note="Standar minimum SNI 19-7030-2004 adalah 0.10% P2O5."
    ))

    # 5. Kalium Total (K2O >= 0.20%)
    k_status = "Lolos SNI" if dry_k2o_pct >= 0.20 else "Kurang dari Standar (<0.20%)"
    sni_eval.append(SNICheckResult(
        parameter="Kalium Total (K2O)",
        measured_value=round(dry_k2o_pct, 2),
        standard_range="≥ 0.20",
        unit="%",
        status=k_status,
        note="Standar minimum SNI 19-7030-2004 adalah 0.20% K2O."
    ))

    # 6. Kadar Air Tumpukan (Kadar air kompos matang SNI <= 50%)
    moist_status = "Lolos SNI" if initial_moisture_pct <= 50.0 else "Terlalu Basah (>50%)"
    sni_eval.append(SNICheckResult(
        parameter="Kadar Air Campuran",
        measured_value=round(initial_moisture_pct, 1),
        standard_range="≤ 50.0",
        unit="%",
        status=moist_status,
        note="Standar kadar air kompos matang SNI adalah maksimum 50%."
    ))

    disclaimer = (
        "Catatan Metodologi: Perhitungan ini menggunakan neraca massa basis kering (dry basis mass balance) "
        "yang dikoreksi dari kadar air bahan baku segar. Nilai peluruhan C/N adalah proyeksi matematis "
        "pada kondisi aerobik terkelola (pembalikan tumpukan rutin dan kelembaban 40-60%). Kematangan fisik "
        "wajib diverifikasi di lapangan berdasarkan suhu mendekati suhu ruang, warna coklat kehitaman, aroma humus, "
        "serta uji laboratorium resmi untuk sertifikasi mutu komersial."
    )

    return SolidCalculationResponse(
        total_wet_weight_kg=round(total_wet_weight, 1),
        total_dry_weight_kg=round(total_dry_weight, 1),
        initial_moisture_pct=round(initial_moisture_pct, 1),
        total_carbon_kg=round(total_c_kg, 2),
        total_nitrogen_kg=round(total_n_kg, 2),
        total_p2o5_kg=round(total_p2o5_kg, 2),
        total_k2o_kg=round(total_k2o_kg, 2),
        dry_basis_c_pct=round(dry_c_pct, 2),
        dry_basis_n_pct=round(dry_n_pct, 2),
        dry_basis_p2o5_pct=round(dry_p2o5_pct, 2),
        dry_basis_k2o_pct=round(dry_k2o_pct, 2),
        initial_c_n_ratio=round(initial_c_n, 1),
        estimated_current_c_n_ratio=round(current_c_n, 1),
        fermentation_phase=phase,
        temperature_range=temp_range,
        npk_label=npk_label,
        suitability=suitability,
        recommendations=recommendations,
        sni_evaluation=sni_eval,
        materials_breakdown=breakdown,
        scientific_disclaimer=disclaimer
    )
