import math
from typing import Dict, List, Any
from app.models.schemas import (
    SolidCalculationRequest, SolidCalculationResponse,
    MaterialDetail, SNICheckResult
)

# Scientific nutrient database (Dry-weight & typical standard references: FAO, Balittanah, Deptan RI)
ORGANIC_DATABASE: Dict[str, Dict[str, Any]] = {
    "Kotoran Sapi": {
        "carbon": 36.0,
        "n": 1.40,
        "p": 0.80,
        "k": 1.20,
        "c_n": 25.7,
        "moisture_typical": 65.0,
        "character": "Dingin, kaya serat, sangat baik untuk pembenah struktur tanah liat/berpasir.",
        "category": "Kotoran Ternak"
    },
    "Kotoran Kambing/Domba": {
        "carbon": 40.0,
        "n": 2.00,
        "p": 1.20,
        "k": 1.80,
        "c_n": 20.0,
        "moisture_typical": 50.0,
        "character": "Kering berbentuk butiran, nutrisi seimbang, cocok untuk pupuk dasar tanaman buah.",
        "category": "Kotoran Ternak"
    },
    "Kotoran Ayam (Broiler/Petelur)": {
        "carbon": 35.0,
        "n": 3.20,
        "p": 2.60,
        "k": 1.60,
        "c_n": 10.9,
        "moisture_typical": 45.0,
        "character": "Panas, amonia tinggi, cepat terurai, wajib dicampur bahan tinggi karbon (sekam/jerami).",
        "category": "Kotoran Ternak"
    },
    "Kotoran Burung Puyuh": {
        "carbon": 34.0,
        "n": 3.80,
        "p": 3.20,
        "k": 2.10,
        "c_n": 8.9,
        "moisture_typical": 40.0,
        "character": "Sangat pekat & mudah membakar akar jika belum matang. Butuh waktu fermentasi lebih lama (21-30 hari).",
        "category": "Kotoran Ternak"
    },
    "Kotoran Kelinci (Padat)": {
        "carbon": 38.0,
        "n": 2.40,
        "p": 1.50,
        "k": 1.10,
        "c_n": 15.8,
        "moisture_typical": 45.0,
        "character": "Kualitas tinggi, dingin, aman, sangat disukai cacing tanah.",
        "category": "Kotoran Ternak"
    },
    "Guano (Kotoran Kelelawar)": {
        "carbon": 22.0,
        "n": 2.00,
        "p": 10.50,
        "k": 1.50,
        "c_n": 11.0,
        "moisture_typical": 25.0,
        "character": "Emas Hitam fosfor alami! Paling ampuh memicu pembungaan dan pembuahan lebat.",
        "category": "Kotoran Ternak"
    },
    "Sekam Padi Mentah": {
        "carbon": 42.0,
        "n": 0.50,
        "p": 0.25,
        "k": 0.55,
        "c_n": 84.0,
        "moisture_typical": 12.0,
        "character": "Porositas tinggi, sumber karbon lambat urai, menggemburkan media agar tidak padat.",
        "category": "Bahan Karbon / Bulking Agent"
    },
    "Arang Sekam Padi": {
        "carbon": 38.0,
        "n": 0.30,
        "p": 0.35,
        "k": 1.30,
        "c_n": 126.0,
        "moisture_typical": 10.0,
        "character": "Biochar alami! Memperbaiki KTK tanah, rumah bagi mikroba baik, menaikkan pH tanah masam.",
        "category": "Bahan Karbon / Bulking Agent"
    },
    "Jerami Padi (Cacah)": {
        "carbon": 40.0,
        "n": 0.70,
        "p": 0.20,
        "k": 1.60,
        "c_n": 57.1,
        "moisture_typical": 20.0,
        "character": "Kaya Kalium alami & silika, menstabilkan kelembaban tumpukan kompos.",
        "category": "Bahan Karbon / Bulking Agent"
    },
    "Dedak Padi Halus (Katul)": {
        "carbon": 40.0,
        "n": 2.20,
        "p": 1.50,
        "k": 1.30,
        "c_n": 18.2,
        "moisture_typical": 13.0,
        "character": "Makanan utama & energi starter mikroba dekomposer (starter booster).",
        "category": "Suplemen Mikroba"
    },
    "Hijauan Daun Leguminosa (Gamal/Lamtoro)": {
        "carbon": 42.0,
        "n": 3.60,
        "p": 0.40,
        "k": 2.10,
        "c_n": 11.6,
        "moisture_typical": 75.0,
        "character": "Biomassa kaya nitrogen hijau, sangat cepat terurai dan memicu suhu termofilik.",
        "category": "Biomassa Hijau"
    },
    "Abu Kayu Dapur": {
        "carbon": 5.0,
        "n": 0.05,
        "p": 1.80,
        "k": 7.50,
        "c_n": 10.0,
        "moisture_typical": 5.0,
        "character": "Sumber Kalium instan tinggi dan menaikkan pH tanah masam secara alami.",
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
        "p": 0.30,
        "k": 0.20,
        "c_n": 20.0,
        "moisture_typical": 5.0,
        "character": "Kaya Kalsium Karbonat (>90%), mencegah penyakit 'blossom end rot' pada cabai/tomat.",
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
            {"name": "Guano (Kotoran Kelelawar)", "qty": "300 kg"},
            {"name": "Kotoran Kambing/Domba", "qty": "500 kg"},
            {"name": "Arang Sekam Padi", "qty": "200 kg"},
            {"name": "Abu Kayu Dapur", "qty": "50 kg"},
            {"name": "Cangkang Telur (Tumbuk)", "qty": "30 kg"},
            {"name": "Bioaktivator + Molase", "qty": "2 Liter"}
        ],
        "fermentation_time": "14 - 21 Hari",
        "steps": [
            "Campurkan guano bersama kohe kambing dan arang sekam sebagai adsorben unsur hara.",
            "Tambahkan abu dapur untuk suntikan Kalium dan cangkang telur untuk Kalsium pembobotan buah.",
            "Basahi dengan campuran bioaktivator hingga kelembaban 40%.",
            "Fermentasikan secara semi-aerob selama 14-21 hari dengan 2 kali pembalikan.",
            "Pupuk sangat efektif diaplikasikan saat tanaman memasuki peralihan vegetatif ke generatif."
        ]
    },
    {
        "id": "bokashi-sapi-soil-conditioner",
        "title": "Bokashi Sapi Pembenah Tanah (Soil Conditioner)",
        "summary": "Pupuk dingin serat tinggi untuk memperbaiki struktur tanah liat padat atau tanah pasir tandus.",
        "materials": [
            {"name": "Kotoran Sapi", "qty": "1000 kg"},
            {"name": "Jerami Padi (Cacah)", "qty": "400 kg"},
            {"name": "Arang Sekam Padi", "qty": "150 kg"},
            {"name": "Dedak Padi Halus (Katul)", "qty": "40 kg"},
            {"name": "Inokulan Trichoderma sp.", "qty": "500 gram (Perlindungan jamur akar)"},
            {"name": "Bioaktivator ROTAN", "qty": "3 Liter"}
        ],
        "fermentation_time": "14 - 21 Hari",
        "steps": [
            "Cacah jerami padi menjadi ukuran 3-5 cm agar bakteri selulolitik mudah mencerna.",
            "Campurkan kotoran sapi, jerami, dan arang sekam.",
            "Larutkan ROTAN dan taburkan biang jamur Trichoderma secara merata saat pencampuran.",
            "Atur kadar air hingga 40-50%.",
            "Tutup terpal dan diamkan. Suhu tumpukan akan stabil di rentang hangat mesofilik-termofilik.",
            "Menghasilkan humus hitam gembur yang tahan lama di dalam tanah."
        ]
    }
]

def calculate_solid_fertilizer(req: SolidCalculationRequest) -> SolidCalculationResponse:
    total_weight = sum(m.weight_kg for m in req.materials)
    if total_weight <= 0:
        raise ValueError("Total berat bahan harus lebih besar dari 0 kg.")

    total_c_kg = 0.0
    total_n_kg = 0.0
    total_p_kg = 0.0
    total_k_kg = 0.0

    breakdown: List[MaterialDetail] = []

    for mat in req.materials:
        db = ORGANIC_DATABASE.get(mat.name)
        if not db:
            # Fallback default estimation
            c_val, n_val, p_val, k_val, cn_val, desc = 30.0, 1.0, 0.5, 1.0, 30.0, "Bahan Organik Umum"
        else:
            c_val = db["carbon"]
            n_val = db["n"]
            p_val = db["p"]
            k_val = db["k"]
            cn_val = db["c_n"]
            desc = db["character"]

        c_kg = mat.weight_kg * (c_val / 100.0)
        n_kg = mat.weight_kg * (n_val / 100.0)
        p_kg = mat.weight_kg * (p_val / 100.0)
        k_kg = mat.weight_kg * (k_val / 100.0)

        total_c_kg += c_kg
        total_n_kg += n_kg
        total_p_kg += p_kg
        total_k_kg += k_kg

        breakdown.append(MaterialDetail(
            name=mat.name,
            weight_kg=mat.weight_kg,
            carbon_pct=c_val,
            nitrogen_pct=n_val,
            phosphorus_pct=p_val,
            potassium_pct=k_val,
            carbon_kg=round(c_kg, 2),
            nitrogen_kg=round(n_kg, 2),
            phosphorus_kg=round(p_kg, 2),
            potassium_kg=round(k_kg, 2),
            c_n_ratio=round(cn_val, 1),
            function_desc=desc
        ))

    final_c_pct = (total_c_kg / total_weight) * 100.0
    final_n_pct = (total_n_kg / total_weight) * 100.0
    final_p_pct = (total_p_kg / total_weight) * 100.0
    final_k_pct = (total_k_kg / total_weight) * 100.0

    initial_c_n = total_c_kg / total_n_kg if total_n_kg > 0 else 0.0

    # Fermentation dynamic decay modeling
    # Over 21 days, C/N typically decays from ~30:1 down towards 12-15:1
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

    # Label NPK
    npk_label = f"N-P-K: {final_n_pct:.2f}% - {final_p_pct:.2f}% - {final_k_pct:.2f}%"

    # Suitability & Recommendations
    recommendations = []
    if initial_c_n > 35:
        recommendations.append("️ C/N Rasio Awal Terlalu Tinggi (>35:1): Tambahkan kotoran ternak ayam/puyuh atau dedak padi untuk memacu pertumbuhan bakteri pengurai.")
    elif initial_c_n < 20:
        recommendations.append("️ C/N Rasio Awal Terlalu Rendah (<20:1): Campuran terlalu banyak nitrogen (bisa timbul bau pesing amonia). Tambahkan sekam padi atau jerami kering.")
    else:
        recommendations.append(" C/N Rasio Awal Ideal (20:1 - 35:1): Fermentasi akan berjalan optimal tanpa bau busuk.")

    if final_n_pct >= 2.0:
        suitability = "Kaya Nitrogen (Vegetatif): Sangat baik untuk sayuran daun, persemaian bibit, dan pemicu anakan padi."
    elif final_p_pct >= 2.0 or final_k_pct >= 2.0:
        suitability = "Kaya Fosfor & Kalium (Generatif): Sangat baik untuk fase pembungaan, pembesaran buah cabai, tomat, dan sawit."
    else:
        suitability = "Kompos Seimbang / Pembenah Tanah: Memperbaiki KTK tanah, retensi air, dan struktur tanah tandus."

    # SNI 19-7030-2004 Evaluation
    sni_eval: List[SNICheckResult] = []

    # 1. C/N Ratio
    cn_status = "Lolos SNI" if (10.0 <= current_c_n <= 20.0) else ("Perlu Fermentasi Lanjutan" if current_c_n > 20 else "Lolos SNI")
    sni_eval.append(SNICheckResult(
        parameter="Rasio C/N",
        measured_value=round(current_c_n, 1),
        standard_range="10 - 20",
        unit="Rasio",
        status=cn_status,
        note="Standar SNI mensyaratkan C/N 10-20 untuk memastikan tidak terjadi imobilisasi nitrogen di tanah."
    ))

    # 2. Nitrogen (N)
    n_status = "Lolos SNI" if final_n_pct >= 0.40 else "Kurang"
    sni_eval.append(SNICheckResult(
        parameter="Nitrogen Total (N)",
        measured_value=round(final_n_pct, 2),
        standard_range="≥ 0.40",
        unit="%",
        status=n_status,
        note="Kadar minimum SNI adalah 0.40%."
    ))

    # 3. Fosfor (P2O5)
    p_status = "Lolos SNI" if final_p_pct >= 0.10 else "Kurang"
    sni_eval.append(SNICheckResult(
        parameter="Fosfor Total (P2O5)",
        measured_value=round(final_p_pct, 2),
        standard_range="≥ 0.10",
        unit="%",
        status=p_status,
        note="Kadar minimum SNI adalah 0.10%."
    ))

    # 4. Kalium (K2O)
    k_status = "Lolos SNI" if final_k_pct >= 0.20 else "Kurang"
    sni_eval.append(SNICheckResult(
        parameter="Kalium Total (K2O)",
        measured_value=round(final_k_pct, 2),
        standard_range="≥ 0.20",
        unit="%",
        status=k_status,
        note="Kadar minimum SNI adalah 0.20%."
    ))

    # 5. Karbon Organik
    c_status = "Lolos SNI" if final_c_pct >= 9.80 else "Perlu Tambah Karbon"
    sni_eval.append(SNICheckResult(
        parameter="C-Organik",
        measured_value=round(final_c_pct, 2),
        standard_range="9.80 - 32.00",
        unit="%",
        status=c_status,
        note="C-organik adalah indikator bahan pembenah tanah."
    ))

    return SolidCalculationResponse(
        total_weight_kg=round(total_weight, 1),
        total_carbon_kg=round(total_c_kg, 2),
        total_nitrogen_kg=round(total_n_kg, 2),
        total_phosphorus_kg=round(total_p_kg, 2),
        total_potassium_kg=round(total_k_kg, 2),
        final_carbon_pct=round(final_c_pct, 2),
        final_n_pct=round(final_n_pct, 2),
        final_p_pct=round(final_p_pct, 2),
        final_k_pct=round(final_k_pct, 2),
        initial_c_n_ratio=round(initial_c_n, 1),
        estimated_current_c_n_ratio=round(current_c_n, 1),
        fermentation_phase=phase,
        temperature_range=temp_range,
        npk_label=npk_label,
        suitability=suitability,
        recommendations=recommendations,
        sni_evaluation=sni_eval,
        materials_breakdown=breakdown
    )
