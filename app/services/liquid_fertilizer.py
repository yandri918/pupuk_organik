from typing import Dict, List, Any
from app.models.schemas import (
    LiquidDoseRequest, LiquidDoseResponse,
    LiquidSNIRequest, LiquidSNIResponse, SNICheckResult
)

POC_RECIPES_DATABASE = [
    {
        "id": "poc-rotan-premium",
        "title": "POC ROTAN (Ramuan Organik Tanaman) Premium",
        "category": "Probiotik & Nutrisi Lengkap",
        "highlights": "Mengandung mikroba lengkap: Azotobacter, Azospirillum, Lactobacillus, Rhizobium, Streptomyces",
        "materials": [
            "Buah Pisang Matang: 5 buah",
            "Buah Pepaya Matang: 1 buah",
            "Buah Nanas Matang: 1 buah",
            "Buah Mangga / Buah Manis Lain: 2 buah",
            "Kangkung Air: 3 ikat",
            "Kacang Panjang: 3 ikat",
            "Jagung Muda: 2 buah",
            "Ragi Tape: 3 butir",
            "Air Kelapa Tua: 5 Liter",
            "Air Leri (Cucian Beras): 3 Liter",
            "Gula Merah / Gula Kelapa: 1 kg",
            "Usus / Jeroan Ikan Segar: 2 ons"
        ],
        "fermentation_days": "10 - 14 Hari",
        "vessel_note": "Gunakan wadah plastik atau gerabah tembikar (DILARANG wadah logam).",
        "steps": [
            "Blender halus semua bahan buah-buahan, sayuran, jagung muda, dan usus ikan sampai teksturnya seperti jus pekat.",
            "Rebus 1 kg gula kelapa dengan 1 liter air hingga larut, lalu dinginkan hingga benar-benar suhu ruang.",
            "Campurkan jus buah/sayur, air gula dingin, air kelapa, air leri, dan ragi tape yang sudah dihaluskan ke dalam drum plastik.",
            "Aduk rata selama 5 menit. Tutup wadah secara rapat (fermentasi anaerob).",
            "Setiap 2 hari sekali, buka tutup selama 3-5 menit untuk membuang akumulasi gas fermentasi lalu aduk sebentar.",
            "Panen di hari ke 10-14 saat bau berubah menjadi asam harum segar mirip tape/wine dan tidak ada desisan gas.",
            "Saring cairan bening untuk POC semprot. Ampas padatnya JANGAN DIBUANG, gunakan sebagai inokulan kompos padat."
        ],
        "upgrade_zpt": {
            "vegetatif": "Tambahkan ZPT Auksin 1L + ZPT Sitokinin 1L per 100L POC",
            "generatif": "Tambahkan ZPT Sitokinin 0.5L + ZPT Giberelin 1.5L per 100L POC"
        }
    },
    {
        "id": "poc-rotan-perbanyakan-100l",
        "title": "Metode Perbanyakan Masal POC ROTAN (1 : 100 Liter)",
        "category": "Penghematan Biaya Produksi Skala Luas",
        "highlights": "Dari 1 Liter biang POC ROTAN, dapat diperbanyak menjadi 100 Liter POC kualitas prima",
        "materials": [
            "Biang POC ROTAN Premium: 1 Liter",
            "Air Jernih (Sumur/Mata Air - Non PDAM): 100 Liter",
            "Dedak Padi Halus (Katul): 10 kg",
            "Gula Kelapa / Molase: 5 kg",
            "Air Kelapa Tua: 10 Liter"
        ],
        "fermentation_days": "7 Hari",
        "vessel_note": "Drum plastik 120-150 Liter berpenutup klem.",
        "steps": [
            "Panaskan/rebus 10 kg dedak dan 5 kg gula kelapa bersama 15 liter air hingga larut mendidih untuk mengekstrak nutrisi mikroba.",
            "Biarkan rebusan dedak dingin total hingga suhu ruang (penting agar mikroba tidak mati kepanasan).",
            "Masukkan rebusan dingin ke dalam drum plastik, tambahkan sisa air sumur (85 Liter), 10 Liter air kelapa, dan 1 Liter Biang POC ROTAN.",
            "Aduk hingga tercampur rata ke dasar drum.",
            "Tutup rapat drum secara anaerob selama 7 hari.",
            "Setelah 7 hari, 100 Liter POC siap digunakan dengan khasiat setara biang awal."
        ],
        "upgrade_zpt": None
    },
    {
        "id": "poc-urine-kelinci-liquid-gold",
        "title": "POC Urine Kelinci (Liquid Gold Booster N)",
        "category": "Vegetatif & Daun Hijau Pekat",
        "highlights": "Kadar Nitrogen (N) urine kelinci paling tinggi dibanding ternak sapi/kambing. Efek instan merangsang klorofil.",
        "materials": [
            "Urine Kelinci Murni (Diendapkan 3 hari): 10 Liter",
            "Starter Dekomposer (EM4 Pertanian / ROTAN): 200 ml",
            "Molase / Tetes Tebu: 200 ml",
            "Air Kelapa (Opsional Booster Sitokinin): 1 Liter",
            "Rimpang Jahe & Lengkuas (Parut): 100 gram (Pestisida Nabati Alami)"
        ],
        "fermentation_days": "7 - 14 Hari",
        "vessel_note": "Jerigen plastik 10-15 Liter.",
        "steps": [
            "Saring urine kelinci untuk memisahkan kotoran padat atau bulu kelinci.",
            "Campurkan molase dan EM4/ROTAN ke dalam 1 liter air kelapa, aduk hingga larut.",
            "Masukkan urine kelinci dan larutan starter ke dalam jerigen.",
            "Tambahkan perasan jahe dan lengkuas sebagai anti-bakteri patogen alami.",
            "Tutup rapat jerigen. Buka tutup 10 detik setiap pagi untuk degassing.",
            "Matang saat bau pesing amonia tajam hilang berganti aroma fermentasi segar."
        ],
        "upgrade_zpt": {
            "vegetatif": "Dosis kocor 1:10 (1 liter POC per 10 liter air) atau semprot 1:20."
        }
    },
    {
        "id": "poc-empon-empon-imun",
        "title": "POC Empon-Empon Plus (2-in-1 Imun Booster & Bio-Fungisida)",
        "category": "Proteksi & Nutrisi Herbal",
        "highlights": "Berfungsi ganda: 'Vaksin Alami Tanaman' terhadap jamur/bakteri layu Fusarium dan pupuk penguat jaringan.",
        "materials": [
            "Jahe Merah: 1 kg (Antijamur & penghangat jaringan)",
            "Lengkuas: 1 kg (Antibakteri alami)",
            "Kunyit: 1 kg (Kurkumin pelindung sel tanaman)",
            "Temulawak: 1 kg (Peningkat nafsu makan akar)",
            "Temu Ireng: 1 kg (Anti-nematoda cacing tanah parasit)",
            "Kencur: 0.5 kg (Minyak atsiri anti-hama)",
            "Brotowali: 0.5 kg (Rasa pahit pencegah serangga hisap)",
            "Gula Merah: 2 kg",
            "Air Kelapa: 15 Liter",
            "Starter ROTAN / EM4: 500 ml"
        ],
        "fermentation_days": "14 - 21 Hari",
        "vessel_note": "Drum 30-50 Liter.",
        "steps": [
            "Tumbuk atau giling kasar semua rimpang empon-empon (jangan terlalu halus seperti bubur).",
            "Rebus rimpang bersama 5 liter air hingga hangat 70-80°C selama 15 menit untuk pasteurisasi media dari telur lalat.",
            "Dinginkan rebusan hingga benar-benar dingin suhu ruang.",
            "Masukkan ke dalam drum, tambahkan 15 Liter air kelapa, larutan gula, dan starter mikroba.",
            "Tutup rapat selama 14-21 hari.",
            "Gunakan dengan konsentrasi 150-200 ml per tangki 14 Liter disemprotkan rutin 1 minggu sekali pada tanaman cabai, melon, bawang merah."
        ],
        "upgrade_zpt": None
    }
]

def calculate_liquid_dosage(req: LiquidDoseRequest) -> LiquidDoseResponse:
    crop = req.crop_category.lower()
    method = req.application_method.lower()
    vol = req.volume_liters
    age = req.target_plant_age_days or 30

    if "semprot" in method or "spray" in method or "daun" in method:
        # Foliar Spraying: safe dilution typically 1:70 to 1:100 (10-15 cc per Liter)
        # Younger plants need lighter dose to avoid foliar burn
        if age < 20:
            cc_per_liter = 7.5
            freq = "7 hari sekali pada pagi hari (fase bibit)"
        elif "padi" in crop:
            cc_per_liter = 15.0
            freq = "7 - 10 hari sekali pada fase 15, 30, dan 45 HST"
        elif "sayur" in crop:
            cc_per_liter = 10.0
            freq = "5 - 7 hari sekali (semprot kabut halus)"
        elif "buah" in crop or "palawija" in crop:
            cc_per_liter = 15.0
            freq = "7 hari sekali pada awal pembungaan dan pembesaran buah"
        elif "sawit" in crop or "keras" in crop:
            cc_per_liter = 20.0
            freq = "14 hari sekali pada daun piringan bawah"
        else:
            cc_per_liter = 12.0
            freq = "7 - 10 hari sekali"

        total_poc_cc = vol * cc_per_liter
        ratio = f"1 : {int(1000 / cc_per_liter)}"

    else:
        # Drenching / Kocor Akar (dilution 1:25 to 1:40 or 25-40 cc per Liter)
        if "sayur" in crop:
            cc_per_liter = 25.0
            freq = "7 - 10 hari sekali (200 ml larutan per lubang tanam)"
        elif "sawit" in crop or "keras" in crop:
            cc_per_liter = 50.0
            freq = "1 bulan sekali (2 - 5 liter larutan per pohon di piringan)"
        else:
            cc_per_liter = 30.0
            freq = "10 hari sekali (250 ml larutan per tanaman)"

        total_poc_cc = vol * cc_per_liter
        ratio = f"1 : {int(1000 / cc_per_liter)}"

    tips = [
        "Gunakan air non-kaporit (air sumur atau air hujan). Kaporit/klorin membunuh mikroba aktif POC.",
        "Selalu aplikasikan di pagi hari (06.00 - 09.00) atau sore hari (15.30 - 17.30) saat stomata daun terbuka.",
        "Untuk aplikasi semprot daun, semprotkan kabut halus terutama ke bagian bawah permukaan daun.",
        "Bila dicampur dengan perekat perata alami, gunakan putih telur atau getah lidah buaya 1 sendok per tangki."
    ]

    return LiquidDoseResponse(
        poc_type=req.poc_type,
        crop_category=req.crop_category,
        application_method=req.application_method,
        water_volume_liters=vol,
        recommended_poc_cc=round(total_poc_cc, 1),
        dilution_ratio=ratio,
        application_frequency=freq,
        optimal_time="Pagi Hari (06.00 - 09.00) atau Sore Hari (15.30 - 17.30)",
        special_tips=tips
    )

def check_liquid_sni(req: LiquidSNIRequest) -> LiquidSNIResponse:
    # Evaluasi berdasarkan Keputusan Menteri Pertanian (Permentan) No. 261/KPTS/SR.310/M/4/2019
    evals: List[SNICheckResult] = []
    advice: List[str] = []
    is_pass = True

    # 1. C-Organik (Permentan 261/2019: Min 10%)
    c_pass = (req.c_organic_pct >= 10.0)
    if not c_pass:
        is_pass = False
        advice.append(f"C-Organik ({req.c_organic_pct:.2f}%) di bawah batas minimal (10%). Tambahkan molase, air kelapa tua, atau gula merah saat fermentasi.")
        c_status = "Kurang dari Standar (<10%)"
    else:
        c_status = "Lolos SNI"

    evals.append(SNICheckResult(
        parameter="C-Organik Cair",
        measured_value=round(req.c_organic_pct, 2),
        standard_range="≥ 10.0",
        unit="%",
        status=c_status,
        note="Standar baku mutu Permentan 261/2019 mensyaratkan C-organik cair minimal 10%."
    ))

    # 2. Total N + P2O5 + K2O (Permentan 261/2019: 2.0 - 6.0%)
    npk_pass = (2.0 <= req.total_npk_pct <= 6.0)
    if not npk_pass:
        is_pass = False
        if req.total_npk_pct < 2.0:
            npk_status = "Kurang dari Standar (<2.0%)"
            advice.append(f"Total hara makro ({req.total_npk_pct:.2f}%) kurang dari 2%. Tambahkan urine ternak kelinci (N), guano/jeroan ikan (P), atau abu sabut kelapa (K).")
        else:
            npk_status = "Melebihi Batas Standar (>6.0%)"
            advice.append(f"Total hara makro ({req.total_npk_pct:.2f}%) melebihi 6%. Menurut Permentan 261/2019, POC komersial dibatasi maks 6% untuk mencegah toksisitas dan plasmolisis stomata daun.")
    else:
        npk_status = "Lolos SNI"

    evals.append(SNICheckResult(
        parameter="Total Hara Makro (N + P2O5 + K2O)",
        measured_value=round(req.total_npk_pct, 2),
        standard_range="2.0 - 6.0",
        unit="%",
        status=npk_status,
        note="Rentang standar hara makro pupuk organik cair nasional adalah 2.0% s/d 6.0%."
    ))

    # 3. Derajat Keasaman (pH: 4.0 - 9.0)
    ph_pass = (4.0 <= req.ph <= 9.0)
    if not ph_pass:
        is_pass = False
        advice.append(f"pH pupuk ({req.ph:.2f}) di luar batas aman (4.0 - 9.0). Tambahkan air kapur dolomit/abu kayu jika terlalu asam (<4.0).")
        ph_status = "Di Luar Batas Standar"
    else:
        ph_status = "Lolos SNI"

    evals.append(SNICheckResult(
        parameter="Derajat Keasaman (pH)",
        measured_value=round(req.ph, 2),
        standard_range="4.0 - 9.0",
        unit="pH",
        status=ph_status,
        note="Rentang pH aman untuk jaringan stomata daun dan viabilitas mikroba bermanfaat."
    ))

    # 4. Cemaran Mikroba Salmonella (Wajib Negatif)
    salm_pass = (req.pathogen_salmonella.strip().lower() == "negatif")
    if not salm_pass:
        is_pass = False
        advice.append("Terdeteksi Salmonella sp.! Wajib pasteurisasi bahan baku dan pastikan sanitasi fermentasi terjaga.")
        salm_status = "Tercemar (Bahaya)"
    else:
        salm_status = "Lolos SNI"

    evals.append(SNICheckResult(
        parameter="Cemaran Salmonella sp.",
        measured_value=0.0 if salm_pass else 1.0,
        standard_range="Negatif",
        unit="deteksi",
        status=salm_status,
        note="Baku mutu mewajibkan cemaran Salmonella negatif untuk keamanan hayati."
    ))

    # 5. Cemaran Mikroba Escherichia coli (Maks < 1x10^2 CFU/ml atau MPN/ml)
    ecoli_pass = (req.pathogen_ecoli_cfu < 100.0)
    if not ecoli_pass:
        is_pass = False
        advice.append(f"Cemaran E. coli ({req.pathogen_ecoli_cfu:.0f} CFU/ml) melebihi batas baku mutu (< 100 CFU/ml). Lakukan perpanjangan waktu fermentasi atau pasteurisasi.")
        ecoli_status = "Melebihi Ambang Batas (Tercemar)"
    else:
        ecoli_status = "Lolos SNI"

    evals.append(SNICheckResult(
        parameter="Cemaran Escherichia coli",
        measured_value=round(req.pathogen_ecoli_cfu, 1),
        standard_range="< 100",
        unit="CFU/ml",
        status=ecoli_status,
        note="Batas cemaran coliform patogenik E. coli menurut Permentan 261/2019 adalah maksimum < 1x10^2 CFU/ml."
    ))

    overall = "Memenuhi Standar Mutu POC (Permentan 261/2019)" if is_pass else "Belum Memenuhi Standar Mutu POC (Perlu Tindakan Korektif)"

    return LiquidSNIResponse(
        overall_status=overall,
        is_passed=is_pass,
        details=evals,
        improvement_advice=advice if advice else ["Formula POC Anda telah memenuhi seluruh parameter teknis baku mutu Permentan 261/2019."]
    )
