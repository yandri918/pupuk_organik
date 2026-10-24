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
            "Temulawak: 1 kg (Memacu nafsu makan / penyerapan hara akar)",
            "Temu Ireng: 1 kg (Anti nematoda / cacing perusak akar)",
            "Puyang & Kencur: Masing-masing 1 kg (Aroma repellent hama)",
            "Batang Pisang Cincang: 2 kg (Kalium organik)",
            "Buah Nanas: 2 buah (Enzim bromelain pelarut dinding sel jamur)",
            "Urine Sapi/Kambing: 50 Liter",
            "Decomposer (EM4/ROTAN): 1 Liter"
        ],
        "fermentation_days": "14 - 21 Hari",
        "vessel_note": "Drum fermentasi kapasitas 100 Liter.",
        "steps": [
            "Giling atau parut halus seluruh rimpang empon-empon dan buah nanas.",
            "Campurkan parutan rimpang bersama cincangan batang pisang dan urine ternak di dalam drum.",
            "Teknik Pasteurisasi: Didihkan campuran menggunakan pemanas rendam (immersion heater) agar telur hama dan patogen mati.",
            "Biarkan dingin hingga suhu ruang.",
            "Inokulasikan 1 Liter dekomposer ROTAN/EM4 ke dalam cairan dingin.",
            "Tutup drum rapat-rapat secara anaerob selama 14-21 hari.",
            "Siap digunakan saat bau berubah menjadi aroma jamu segar herbal."
        ],
        "upgrade_zpt": None
    },
    {
        "id": "poc-sawit-spesial",
        "title": "Ramuan Spesial Kelapa Sawit (Sex Ratio Balance & Bobot Buah)",
        "category": "Spesialis Perkebunan Sawit",
        "highlights": "Mengatasi sawit jantan dominan dan meningkatkan Berat Janjang Rata-rata (BJR) 30-50%.",
        "materials": [
            "MOL Daun Gamal / Rumput Hijau: 1 Liter (Sumber Nitrogen kuat)",
            "ROTAN Generatif (Fosfor-Kalium tinggi): 250 cc",
            "Air Bersih: 10 - 15 Liter",
            "Molase / Air Gula: 50 ml"
        ],
        "fermentation_days": "Siap racik dari biang matang",
        "vessel_note": "Ember kocor atau tangki semprot solo.",
        "steps": [
            "Untuk Pohon Dominan Bunga Jantan: Larutkan 1L MOL Gamal + 200cc POC ROTAN Generatif dalam 10L air.",
            "Kocorkan di sekeliling piringan pohon sawit (jarak 0.5 - 1 meter dari pangkal batang).",
            "Semprotkan 250cc ROTAN per tangki 15L ke pelepah daun dan calon bunga jantan.",
            "Hasil: Bunga jantan rontok dalam 15 hari dan tunas baru memunculkan bunga betina produktif.",
            "Untuk Pembesaran Buah: Semprotkan POC ROTAN 250cc per 15L air langsung ke tandan buah 30 hari sebelum panen untuk memacu rendemen minyak dan bobot tandan."
        ],
        "upgrade_zpt": None
    }
]

MOL_COLLECTION = [
    {
        "name": "MOL Bonggol Pisang",
        "hormone": "Sitokinin Tinggi",
        "function": "Memicu pertumbuhan tunas baru, anakan padi, dan pembelahan sel akar.",
        "recipe": "1 kg bonggol pisang dicacah halus + 200 gram gula merah + 2 liter air beras. Fermentasi 7-10 hari."
    },
    {
        "name": "MOL Rebung Bambu",
        "hormone": "Giberelin Tinggi",
        "function": "Memicu perpanjangan batang, pembesaran ruas tanaman, dan pematahan dormansi biji.",
        "recipe": "1 kg rebung bambu muda cacah + 250 gram gula + 3 liter air kelapa. Fermentasi 10 hari."
    },
    {
        "name": "MOL Keong Mas / Bekicot",
        "hormone": "Asam Amino & Nitrogen Hewani",
        "function": "Sumber protein tinggi untuk pemulihan tanaman kerdil atau terserang penyakit.",
        "recipe": "1 kg daging keong mas rebus setengah matang + 1 kg gula kelapa + 2 liter air kelapa + dekomposer. Fermentasi 14 hari."
    },
    {
        "name": "MOL Sabut Kelapa",
        "hormone": "Kalium Organik Murni",
        "function": "Pemanis alami buah, mempertebal dinding sel agar tahan hama, dan mencegah kerontokan bunga.",
        "recipe": "1 kg sabut kelapa kering dipotong kecil + 100 gram gula + 5 liter air. Rendam dan fermentasi 14 hari."
    }
]

def calculate_liquid_dosage(req: LiquidDoseRequest) -> LiquidDoseResponse:
    # Calculation logic based on crop category and method
    crop = req.crop_category.lower()
    method = req.application_method.lower()
    vol = req.volume_liters

    # Standard rule of thumb
    if "semprot" in method:
        # Spraying (dilution usually 1:50 to 1:100 or 10-20 cc per Liter)
        if "sayur" in crop or "semai" in crop:
            cc_per_liter = 10.0
            freq = "5 - 7 hari sekali (Pagi 06.30 - 08.30 saat stomata daun terbuka)"
        elif "padi" in crop:
            cc_per_liter = 15.0
            freq = "7 - 10 hari sekali pada fase 15, 30, dan 45 HST"
        elif "sawit" in crop or "keras" in crop:
            cc_per_liter = 20.0
            freq = "14 hari sekali disemprotkan ke piringan dan pelepah"
        else:
            cc_per_liter = 15.0
            freq = "7 hari sekali"

        total_poc_cc = vol * cc_per_liter
        ratio = f"1 : {int(1000 / cc_per_liter)}"

    else:
        # Drenching / Kocor Akar (dilution usually 1:20 to 1:40 or 25-50 cc per Liter)
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
        f"Gunakan air non-kaporit (air sumur atau air hujan). Kaporit/klorin membunuh mikroba aktif POC.",
        f"Selalu aplikasikan di pagi hari (06.00 - 09.00) atau sore hari (15.30 - 17.30) saat suhu tidak terik.",
        f"Untuk aplikasi semprot daun, semprotkan kabut halus terutama ke bagian bawah daun tempat stomata berada.",
        f"Bila dicampur dengan perekat alami, gunakan putih telur atau lidah buaya 1 sendok per tangki."
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

    # 1. C-Organik (Min 10%)
    c_pass = req.c_organic_pct >= 10.0
    if not c_pass:
        is_pass = False
        advice.append("Tingkatkan C-Organik dengan menambah molase atau air kelapa tua pada saat fermentasi.")
    evals.append(SNICheckResult(
        parameter="C-Organik Cair",
        measured_value=round(req.c_organic_pct, 2),
        standard_range="≥ 10.0",
        unit="%",
        status="Lolos SNI" if c_pass else "Kurang",
        note="Standar baku mutu Permentan 261/2019 mensyaratkan C-organik minimal 10%."
    ))

    # 2. Total N + P2O5 + K2O (2 - 6%)
    npk_pass = (2.0 <= req.total_npk_pct <= 6.0)
    if req.total_npk_pct < 2.0:
        is_pass = False
        advice.append("Total hara NPK kurang dari 2%. Tambahkan urine ternak kelinci (N), guano/usus ikan (P), atau abu sabut kelapa (K).")
    elif req.total_npk_pct > 6.0:
        advice.append("Total NPK di atas 6%. Pupuk sangat pekat, pastikan rasio pengenceran ditingkatkan saat aplikasi agar daun tidak terbakar.")
    evals.append(SNICheckResult(
        parameter="Total Hara Makro (N + P2O5 + K2O)",
        measured_value=round(req.total_npk_pct, 2),
        standard_range="2.0 - 6.0",
        unit="%",
        status="Lolos SNI" if npk_pass else "Di Luar Rentang",
        note="Rentang standar hara makro pupuk organik cair adalah 2% s/d 6%."
    ))

    # 3. Derajat Keasaman (pH: 4 - 9)
    ph_pass = (4.0 <= req.ph <= 9.0)
    if not ph_pass:
        is_pass = False
        advice.append("pH pupuk di luar batas aman (4 - 9). Tambahkan air kapur dolomit jika terlalu asam (<4).")
    evals.append(SNICheckResult(
        parameter="Derajat Keasaman (pH)",
        measured_value=round(req.ph, 2),
        standard_range="4.0 - 9.0",
        unit="pH",
        status="Lolos SNI" if ph_pass else "Di Luar Batas",
        note="pH ramah mikroba dan jaringan stomata daun."
    ))

    # 4. Cemaran Mikroba Salmonella (Harus Negatif)
    salm_pass = (req.pathogen_salmonella.strip().lower() == "negatif")
    if not salm_pass:
        is_pass = False
        advice.append("Terdeteksi Salmonella! Pasteurisasi bahan baku dan pastikan suhu fermentasi mencapai fasa termofilik.")
    evals.append(SNICheckResult(
        parameter="Cemaran Salmonella sp.",
        measured_value=0.0 if salm_pass else 1.0,
        standard_range="Negatif",
        unit="deteksi",
        status="Lolos SNI" if salm_pass else "Tercemar (Bahaya)",
        note="Wajib negatif untuk keamanan biologis manusia dan tanaman."
    ))

    return LiquidSNIResponse(
        overall_status="Memenuhi Standar Mutu POC (Permentan 261/2019)" if is_pass else "Perlu Penyempurnaan Formula",
        details=evals,
        improvement_advice=advice if advice else ["Formula POC Anda telah memenuhi seluruh parameter teknis standar baku mutu nasional!"]
    )
