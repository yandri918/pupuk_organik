from typing import Dict, List, Any, Optional
from app.models.schemas import (
    LiquidDoseRequest, LiquidDoseResponse,
    LiquidSNIRequest, LiquidSNIResponse, SNICheckResult,
    POCBatchBrewRequest, POCBatchBrewResponse, POCBrewIngredient,
    POCFieldScheduleRequest, POCFieldScheduleResponse, POCFieldStage,
    POCTroubleshootItem, POCTankMixItem
)

POC_RECIPES_DATABASE = [
    {
        "id": "poc-rotan-premium",
        "title": "POC ROTAN (Ramuan Organik Tanaman) Premium",
        "category": "Probiotik & Nutrisi Lengkap",
        "highlights": "Mengandung konsorsium mikroba lengkap: Azotobacter, Azospirillum, Lactobacillus, Rhizobium, Streptomyces.",
        "base_batch_liters": 10.0,
        "ingredients_structured": [
            {"name": "Pisang Matang", "amount": 5.0, "unit": "buah"},
            {"name": "Pepaya Matang", "amount": 1.0, "unit": "buah"},
            {"name": "Nanas Matang", "amount": 1.0, "unit": "buah"},
            {"name": "Mangga Matang", "amount": 2.0, "unit": "buah"},
            {"name": "Kangkung Air", "amount": 3.0, "unit": "ikat"},
            {"name": "Kacang Panjang", "amount": 3.0, "unit": "ikat"},
            {"name": "Jagung Muda", "amount": 2.0, "unit": "buah"},
            {"name": "Ragi Tape", "amount": 3.0, "unit": "butir"},
            {"name": "Air Kelapa Tua", "amount": 5.0, "unit": "Liter"},
            {"name": "Air Leri (Cucian Beras)", "amount": 3.0, "unit": "Liter"},
            {"name": "Gula Merah / Gula Kelapa", "amount": 1.0, "unit": "kg"},
            {"name": "Jeroan / Usus Ikan Segar", "amount": 0.2, "unit": "kg"}
        ],
        "materials": [
            "Buah Pisang Matang: 5 buah",
            "Buah Pepaya Matang: 1 buah",
            "Buah Nanas Matang: 1 buah",
            "Buah Mangga: 2 buah",
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
        "highlights": "Dari 1 Liter biang POC ROTAN, dapat diperbanyak menjadi 100 Liter POC kualitas prima siap sebar ke lahan 2-3 hektar.",
        "base_batch_liters": 100.0,
        "ingredients_structured": [
            {"name": "Biang POC ROTAN Premium", "amount": 1.0, "unit": "Liter"},
            {"name": "Air Jernih (Sumur/Mata Air)", "amount": 85.0, "unit": "Liter"},
            {"name": "Dedak Padi Halus (Katul)", "amount": 10.0, "unit": "kg"},
            {"name": "Gula Kelapa / Molase", "amount": 5.0, "unit": "kg"},
            {"name": "Air Kelapa Tua", "amount": 10.0, "unit": "Liter"}
        ],
        "materials": [
            "Biang POC ROTAN Premium: 1 Liter",
            "Air Jernih (Sumur/Mata Air - Non PDAM): 85 Liter",
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
        "highlights": "Kadar Nitrogen (N 2.7%) & Kalium (K 1.5%) urine kelinci paling tinggi dibanding ternak sapi/kambing. Efek instan merangsang klorofil & anakan tunas.",
        "base_batch_liters": 10.0,
        "ingredients_structured": [
            {"name": "Urine Kelinci Murni", "amount": 10.0, "unit": "Liter"},
            {"name": "Starter EM4 / ROTAN", "amount": 0.2, "unit": "Liter"},
            {"name": "Molase / Tetes Tebu", "amount": 0.2, "unit": "Liter"},
            {"name": "Air Kelapa Tua", "amount": 1.0, "unit": "Liter"},
            {"name": "Rimpang Jahe & Lengkuas", "amount": 0.1, "unit": "kg"}
        ],
        "materials": [
            "Urine Kelinci Murni (Diendapkan 3 hari): 10 Liter",
            "Starter Dekomposer (EM4 Pertanian / ROTAN): 200 ml",
            "Molase / Tetes Tebu: 200 ml",
            "Air Kelapa Tua (Booster Sitokinin): 1 Liter",
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
            "Matang saat bau pesing amonia tajam hilang berganti aroma fermentasi manis segar."
        ],
        "upgrade_zpt": {
            "vegetatif": "Dosis kocor 1:10 (1 liter POC per 10 liter air) atau semprot 1:20."
        }
    },
    {
        "id": "poc-faa-asam-amino-ikan",
        "title": "POC Asam Amino Ikan Laut (Fish Amino Acid / FAA)",
        "category": "Regenerasi Sel & Anti-Stres Tanaman",
        "highlights": "Sumber polipeptida, asam amino esensial bebas, dan kolagen laut. Memicu pembentukan tunas super cepat, memulihkan tanaman pasca banjir/kekeringan.",
        "base_batch_liters": 10.0,
        "ingredients_structured": [
            {"name": "Ikan Laut Segar / Jeroan Ikan", "amount": 5.0, "unit": "kg"},
            {"name": "Gula Merah Aren / Molase", "amount": 5.0, "unit": "kg"},
            {"name": "Nanas Matang (Jus)", "amount": 1.0, "unit": "buah"},
            {"name": "Air Kelapa Tua", "amount": 2.0, "unit": "Liter"},
            {"name": "EM4 Proteolitik", "amount": 0.1, "unit": "Liter"}
        ],
        "materials": [
            "Ikan Laut Segar / Jeroan & Insang Ikan: 5 kg",
            "Gula Merah Aren Asli / Molase Kental: 5 kg (Rasio KNF 1:1)",
            "Nanas Matang (Penghasil Enzim Bromelin Pemecah Protein): 1 buah",
            "Air Kelapa: 2 Liter",
            "EM4 / Probiotik Proteolitik: 100 ml"
        ],
        "fermentation_days": "21 - 30 Hari",
        "vessel_note": "Ember/tong plastik kedap dengan kain kasa dan penutup rapat.",
        "steps": [
            "Cacah kasar ikan atau jeroan ikan (jangan dicuci dengan air PDAM berkaporit).",
            "Blender nanas matang hingga halus, nanas mengandung bromelin yang memotong rantai protein ikan menjadi asam amino bebas.",
            "Campurkan cacahan ikan, jus nanas, dan gula aren dengan rasio bobot 1:1 sampai semua ikan terselimuti gula tebal.",
            "Tambahkan air kelapa dan starter mikroba, aduk hingga larut merata.",
            "Tutup rapat dengan penutup ber-airlock. Simpan di tempat teduh bersuhu ruang.",
            "Panen di hari ke-21 atau 30. Ekstrak cairan cokelat kental beraroma seperti kecap/petis ikan manis."
        ],
        "upgrade_zpt": {
            "vegetatif": "Dosis semprot daun: 2-3 cc per Liter air (30-45 cc per tangki 15L). Disemprotkan tiap 7-10 hari."
        }
    },
    {
        "id": "poc-psb-merah-delima",
        "title": "POC PSB (Photosynthetic Bacteria / Bakteri Fotosintesis)",
        "category": "Mikroba Fotosintesis & Tenaga Matahari",
        "highlights": "Bakteri Rhodopseudomonas palustris berwarna merah rubi pekat. Membantu tanaman menyerap cahaya matahari & unsur hara secara maksimal di musim hujan / cuaca mendung.",
        "base_batch_liters": 5.0,
        "ingredients_structured": [
            {"name": "Telur Ayam / Bebek Mentah", "amount": 2.0, "unit": "butir"},
            {"name": "Penyedap Rasa (MSG)", "amount": 30.0, "unit": "gram"},
            {"name": "Saus Tiram / Terasi Halus", "amount": 30.0, "unit": "gram"},
            {"name": "Air Kolam / Sumur Non-Kaporit", "amount": 5.0, "unit": "Liter"},
            {"name": "Biang PSB Merah Indukan", "amount": 0.15, "unit": "Liter"}
        ],
        "materials": [
            "Telur Ayam / Bebek Mentah: 2 butir",
            "Penyedap Rasa (MSG / Monosodium Glutamat): 2 sendok makan",
            "Saus Tiram / Terasi Matang Halus: 2 sendok makan",
            "Air Kolam Ikan / Air Sumur Non-Kaporit: 5 - 6 Liter",
            "Biang Indukan PSB Merah (Opsional percepat): 100 - 200 ml"
        ],
        "fermentation_days": "15 - 25 Hari (Jemur Matahari Langsung)",
        "vessel_note": "Botol plastik bening transparan (ukuran 1.5 Liter x 4 botol).",
        "steps": [
            "Kocok lepas 2 butir telur bersama 2 sdm MSG dan 2 sdm saus tiram/terasi hingga larut homogen.",
            "Isi botol plastik transparan dengan air sumur atau air kolam, sisakan ruang udara sekitar 5 cm dari mulut botol.",
            "Masukkan 2-3 sendok makan adonan telur ke dalam masing-masing botol 1.5 Liter.",
            "Jika memiliki biang PSB merah lama, tambahkan 50 ml per botol untuk menginokulasi lebih cepat.",
            "Kocok botol hingga merata, tutup rapat.",
            "JEMUR DI BAWAH TERIK MATAHARI PENUH dari jam 08.00 pagi hingga 16.00 sore setiap hari.",
            "Kocok botol sehari sekali. Dalam 7-15 hari warna akan berubah dari putih keruh menjadi hijau muda, lalu merah marun/ungu delima pekat.",
            "Siap digunakan saat aroma mirip terasi matang dan warna merah gelap mengkilap."
        ],
        "upgrade_zpt": {
            "vegetatif": "Dosis semprot: 10-15 cc per Liter air (150-200 cc per tangki 14L) disemprot tepat di bawah terik matahari pagi jam 08.00 - 10.00."
        }
    },
    {
        "id": "poc-kalium-kalsium-buah",
        "title": "POC Kalium & Kalsium Organik (Pelebat & Anti-Rontok Buah)",
        "category": "Generatif, Pembungaan & Bobot Buah",
        "highlights": "Tinggi Kalium bebas (K) dan Kalsium terlarut (Ca). Menguatkan tangkai bunga agar tidak rontok, memadatkan bobot buah, dan meningkatkan kadar brix manis.",
        "base_batch_liters": 15.0,
        "ingredients_structured": [
            {"name": "Sabut Kelapa Kering (Cacah)", "amount": 2.0, "unit": "kg"},
            {"name": "Kulit Pisang Matang (Cacah)", "amount": 1.5, "unit": "kg"},
            {"name": "Cangkang Telur Sangrai Halus", "amount": 0.5, "unit": "kg"},
            {"name": "Cuka Makan / Asam Sitrat", "amount": 0.2, "unit": "Liter"},
            {"name": "Air Kelapa Tua", "amount": 10.0, "unit": "Liter"},
            {"name": "Molase / Gula Merah", "amount": 0.5, "unit": "kg"},
            {"name": "EM4 Pertanian", "amount": 0.15, "unit": "Liter"}
        ],
        "materials": [
            "Sabut Kelapa Tua Kering (Cacah): 2 kg",
            "Kulit Pisang Matang (Cacah): 1.5 kg",
            "Cangkang Telur Ayam (Cuci, Sangrai & Tumbuk Halus): 500 gram",
            "Cuka Makan Alami / Asam Sitrat: 200 ml (Mengekstrak ion Ca²⁺ dari cangkang)",
            "Air Kelapa Tua: 10 Liter",
            "Molase / Gula Merah: 500 gram",
            "EM4 Pertanian: 150 ml"
        ],
        "fermentation_days": "14 - 21 Hari",
        "vessel_note": "Tong/Drum plastik 25 - 30 Liter.",
        "steps": [
            "Larutkan tepung cangkang telur sangrai dengan 200 ml cuka. Biarkan terjadi reaksi desisan (effervescence) selama 2 jam hingga kalsium larut menjadi Kalsium Asetat bioavailable.",
            "Masukkan cacahan sabut kelapa dan kulit pisang ke dalam tong plastik.",
            "Tuang larutan cangkang telur, 10 Liter air kelapa, larutan molase, dan EM4 ke dalam tong.",
            "Aduk rata selama 3 menit. Tutup tong secara anaerob.",
            "Buka tutup tiap 2 hari sekali untuk mengeluarkan akumulasi gas CO2.",
            "Saring cairan pada hari ke 14-21. Siap diaplikasikan pada tanaman fase berbunga & pengisian buah."
        ],
        "upgrade_zpt": {
            "generatif": "Aplikasi kocor akar 50 ml per 10 L air (1:200) atau semprot daun 10 ml per Liter air setiap minggu sejak muncul bakal bunga."
        }
    },
    {
        "id": "poc-bio-silika-nabati",
        "title": "POC Bio-Silika Nabati (Perisai Alami Anti-Wereng & Blas)",
        "category": "Penguat Dinding Sel & Ketahanan Hama",
        "highlights": "Kaya Silika aktif (SiO2) dari sekam padi. Mempertebal epidermis daun dan batang padi sehingga mandibula wereng/ulat patah dan spora jamur blas tidak tembus.",
        "base_batch_liters": 20.0,
        "ingredients_structured": [
            {"name": "Abu Sekam Padi Hitam Murni", "amount": 3.0, "unit": "kg"},
            {"name": "Sekam Mentah Giling", "amount": 1.0, "unit": "kg"},
            {"name": "Kapur Pertanian / Dolomit", "amount": 0.3, "unit": "kg"},
            {"name": "Air Kelapa Tua", "amount": 5.0, "unit": "Liter"},
            {"name": "Air Sumur Bersih", "amount": 15.0, "unit": "Liter"},
            {"name": "Molase / Gula Merah", "amount": 0.5, "unit": "kg"},
            {"name": "Starter Bakteri Pelarut Silikat", "amount": 0.2, "unit": "Liter"}
        ],
        "materials": [
            "Abu Sekam Padi Hitam Murni: 3 kg",
            "Sekam Mentah Giling: 1 kg",
            "Kapur Pertanian / Dolomit: 300 gram",
            "Air Kelapa: 5 Liter",
            "Air Sumur: 15 Liter",
            "Molase: 500 gram",
            "Starter Bakteri Pelarut Silikat (Bacillus / ROTAN): 200 ml"
        ],
        "fermentation_days": "10 - 14 Hari",
        "vessel_note": "Drum plastik 30 Liter.",
        "steps": [
            "Rebus abu sekam padi dengan 5 liter air selama 20 menit untuk membantu pelepasan kristal silika amorf menjadi asam ortosilikat terlarut.",
            "Dinginkan rebusan abu hingga suhu kamar.",
            "Masukkan ke dalam drum, campurkan air sumur, air kelapa, dolomit, molase, dan starter bakteri.",
            "Aduk secara berkala searah jarum jam.",
            "Fermentasi selama 10-14 hari.",
            "Endapkan selama 24 jam sebelum disaring agar partikel abu mengendap ke dasar.",
            "Ambil cairan bening kecokelatan untuk aplikasi semprot."
        ],
        "upgrade_zpt": {
            "vegetatif": "Dosis semprot: 100-150 cc per tangki 16 Liter, semprot pada daun atas dan batang bawah pada umur 20, 35, dan 50 HST."
        }
    },
    {
        "id": "poc-eco-enzyme-citrus",
        "title": "Eco Enzyme Klasik Kulit Buah 1:3:10",
        "category": "Aktivator Biologis, Enzim & Pembersih Tanah",
        "highlights": "Formula emas Dr. Rosukon Poompanvong (1 Molase : 3 Bahan Organik Kulit Buah : 10 Air). Kaya enzim protease, lipase, dan asam asetat organik alami.",
        "base_batch_liters": 14.0,
        "ingredients_structured": [
            {"name": "Gula Merah / Molase Asli", "amount": 1.0, "unit": "kg"},
            {"name": "Limbah Kulit Buah Segar", "amount": 3.0, "unit": "kg"},
            {"name": "Air Sumur / Air Hujan", "amount": 10.0, "unit": "Liter"}
        ],
        "materials": [
            "Gula Merah / Molase Asli: 1 kg",
            "Limbah Kulit Buah Segar (Kulit Jeruk, Nanas, Pepaya, Semangka): 3 kg",
            "Air Sumur / Air Hujan: 10 Liter"
        ],
        "fermentation_days": "90 Hari (3 Bulan Matang Sempurna)",
        "vessel_note": "Wadah plastik kedap udara (botol galon / jerigen) berventilasi.",
        "steps": [
            "Larutkan 1 kg molase atau gula merah aren ke dalam 10 Liter air di dalam wadah plastik.",
            "Masukkan 3 kg kulit buah segar yang sudah dicuci dan dipotong kecil.",
            "Aduk merata hingga seluruh kulit buah terendam cairan gula.",
            "Sisakan ruang udara sekitar 20% wadah untuk akumulasi gas.",
            "Tutup rapat wadah. Pada bulan pertama, buka tutup wadah setiap hari selama beberapa detik untuk membuang gas.",
            "Bulan kedua dan ketiga wadah dibiarkan tertutup rapat tanpa dibuka.",
            "Panen di hari ke-90. Cairan berwarna cokelat tua beraroma asam manis fermentasi buah segar yang sangat khas."
        ],
        "upgrade_zpt": {
            "all_purpose": "Dosis pembenah tanah: 1 ml per 1 Liter air (1:1000) disiramkan ke tanah. Untuk pengusir hama semprot 15-30 ml per tangki."
        }
    },
    {
        "id": "poc-jakaba-umbi-perakaran",
        "title": "POC Biakan Jamur Jakaba (Keberuntungan Abadi)",
        "category": "Hormon Perakaran & Pembesar Umbi",
        "highlights": "Kaya miselium Jakaba & spora jamur menguntungkan. Mengandung asam humat, auksin perakaran, dan mineral penguat umbi kentang, wortel, dan bawang merah.",
        "base_batch_liters": 10.0,
        "ingredients_structured": [
            {"name": "Air Leri Cucian Beras Pertama", "amount": 10.0, "unit": "Liter"},
            {"name": "Dedak Padi Halus (Katul)", "amount": 0.2, "unit": "kg"},
            {"name": "Terasi Bakar Matang", "amount": 10.0, "unit": "gram"},
            {"name": "Kapur Sirih Halus", "amount": 5.0, "unit": "gram"}
        ],
        "materials": [
            "Air Leri (Cucian Beras Pertama yang Pekat): 10 Liter",
            "Dedak Padi Halus (Katul): 200 gram",
            "Terasi Bakar / Matang: 1 sendok teh",
            "Kapur Sirih Halus: 1/2 sendok teh",
            "Biang Jakaba (Opsional jika ada): 1 potongan kecil"
        ],
        "fermentation_days": "14 - 21 Hari (Tempat Gelap)",
        "vessel_note": "Ember plastik ditutup kain kaos / kain kasa tebal (aerob terbatas, terlindung dari lalat bertelur).",
        "steps": [
            "Tampung air leri cucian beras pertama yang paling kental dan pekat.",
            "Larutkan terasi bakar dan dedak padi ke dalam air leri, aduk rata.",
            "Tambahkan kapur sirih untuk menyeimbangkan pH air leri.",
            "Tuang ke ember bersih, tutup permukaan ember menggunakan kain tebal dan ikat kencang dengan karet ban.",
            "SIMPAN DI TEMPAT GELAP, LEMBAP, DAN JANGAN DIGOYANG SAMA SEKALI selama 14-21 hari.",
            "Setelah 14 hari akan terbentuk lapisan jamur seperti karang berwarna cokelat muda bertotol kemerahan di permukaan (Jamur Jakaba).",
            "Gunakan cairan di bawah jamur sebagai POC kocor dan semprot."
        ],
        "upgrade_zpt": {
            "vegetatif": "Dosis kocor: 400 ml air Jakaba per tangki 14 Liter air. Kocor pada pangkal batang perakaran tanaman."
        }
    },
    {
        "id": "poc-empon-empon-imun",
        "title": "POC Empon-Empon Plus (2-in-1 Imun Booster & Bio-Fungisida)",
        "category": "Proteksi & Nutrisi Herbal",
        "highlights": "Berfungsi ganda: 'Vaksin Alami Tanaman' terhadap jamur/bakteri layu Fusarium dan pupuk penguat jaringan sel.",
        "base_batch_liters": 20.0,
        "ingredients_structured": [
            {"name": "Jahe Merah", "amount": 1.0, "unit": "kg"},
            {"name": "Lengkuas", "amount": 1.0, "unit": "kg"},
            {"name": "Kunyit", "amount": 1.0, "unit": "kg"},
            {"name": "Temulawak", "amount": 1.0, "unit": "kg"},
            {"name": "Temu Ireng", "amount": 1.0, "unit": "kg"},
            {"name": "Kencur", "amount": 0.5, "unit": "kg"},
            {"name": "Brotowali", "amount": 0.5, "unit": "kg"},
            {"name": "Gula Merah Aren", "amount": 2.0, "unit": "kg"},
            {"name": "Air Kelapa Tua", "amount": 15.0, "unit": "Liter"},
            {"name": "Starter ROTAN / EM4", "amount": 0.5, "unit": "Liter"}
        ],
        "materials": [
            "Jahe Merah: 1 kg (Antijamur & penghangat jaringan)",
            "Lengkuas: 1 kg (Antibakteri alami)",
            "Kunyit: 1 kg (Kurkumin pelindung sel tanaman)",
            "Temulawak: 1 kg (Peningkat nafsu makan akar)",
            "Temu Ireng: 1 kg (Anti-nematoda cacing parasit tanah)",
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

MOL_COLLECTION = [
    {
        "name": "MOL Bonggol Pisang",
        "hormone": "Sitokinin Tinggi",
        "category": "Tunas & Perakaran",
        "base_batch_liters": 3.0,
        "ingredients_structured": [
            {"name": "Bonggol Pisang Cacah", "amount": 1.0, "unit": "kg"},
            {"name": "Gula Merah", "amount": 0.2, "unit": "kg"},
            {"name": "Air Beras (Leri)", "amount": 2.0, "unit": "Liter"}
        ],
        "function": "Memicu pertumbuhan tunas baru, multiplikasi anakan padi produktif, dan pembelahan sel akar aktif.",
        "recipe": "1 kg bonggol pisang dicacah halus + 200 gram gula merah + 2 liter air beras. Fermentasi 7-10 hari."
    },
    {
        "name": "MOL Rebung Bambu",
        "hormone": "Giberelin Tinggi",
        "category": "Pemanjangan Batang",
        "base_batch_liters": 4.0,
        "ingredients_structured": [
            {"name": "Rebung Bambu Muda Cacah", "amount": 1.0, "unit": "kg"},
            {"name": "Gula Merah / Pasir", "amount": 0.25, "unit": "kg"},
            {"name": "Air Kelapa Tua", "amount": 3.0, "unit": "Liter"}
        ],
        "function": "Memicu perpanjangan ruas tanaman, mempercepat pematahan masa dormansi benih, dan memperbesar ukuran sel.",
        "recipe": "1 kg rebung bambu muda cacah + 250 gram gula + 3 liter air kelapa. Fermentasi 10 hari."
    },
    {
        "name": "MOL Keong Mas / Bekicot",
        "hormone": "Asam Amino & Nitrogen Hewani",
        "category": "Pemulihan & Daun",
        "base_batch_liters": 4.0,
        "ingredients_structured": [
            {"name": "Daging Keong Mas Rebus", "amount": 1.0, "unit": "kg"},
            {"name": "Gula Kelapa", "amount": 1.0, "unit": "kg"},
            {"name": "Air Kelapa Tua", "amount": 2.0, "unit": "Liter"},
            {"name": "Dekomposer EM4", "amount": 0.1, "unit": "Liter"}
        ],
        "function": "Sumber protein tinggi untuk pemulihan tanaman kerdil, kuning daun, atau terserang hama penyakit.",
        "recipe": "1 kg daging keong mas rebus setengah matang + 1 kg gula kelapa + 2 liter air kelapa + dekomposer. Fermentasi 14 hari."
    },
    {
        "name": "MOL Sabut Kelapa",
        "hormone": "Kalium Organik Murni",
        "category": "Bunga & Buah",
        "base_batch_liters": 6.0,
        "ingredients_structured": [
            {"name": "Sabut Kelapa Kering Cacah", "amount": 1.0, "unit": "kg"},
            {"name": "Gula Merah / Pasir", "amount": 0.1, "unit": "kg"},
            {"name": "Air Sumur", "amount": 5.0, "unit": "Liter"}
        ],
        "function": "Pemanis alami buah, mempertebal dinding sel agar tahan hama kutu, dan mencegah kerontokan bunga dan bakal buah.",
        "recipe": "1 kg sabut kelapa kering dipotong kecil + 100 gram gula + 5 liter air. Rendam dan fermentasi 14 hari."
    },
    {
        "name": "MOL Nasi Basi (Trichoderma Sp.)",
        "hormone": "Bio-Fungisida & Dekomposer Selulosa",
        "category": "Bioproteksi Tanah",
        "base_batch_liters": 1.5,
        "ingredients_structured": [
            {"name": "Nasi Basi Berjamur", "amount": 0.5, "unit": "kg"},
            {"name": "Gula Pasir / Merah", "amount": 0.1, "unit": "kg"},
            {"name": "Air Bersih", "amount": 1.0, "unit": "Liter"}
        ],
        "function": "Membiakkan spora jamur Trichoderma harzianum pelindung akar dari busuk akar Phytophthora dan layu Fusarium.",
        "recipe": "500 gram nasi kepal dibiarkan di tempat gelap 4 hari sampai berjamur jingga/hijau, campur 1 liter air + 100 gram gula. Fermentasi 7 hari."
    },
    {
        "name": "MOL Daun Kelor & Daun Gamal",
        "hormone": "Zeatin & Nitrogen Nabati Super",
        "category": "Vegetatif Super Cepat",
        "base_batch_liters": 4.0,
        "ingredients_structured": [
            {"name": "Daun Kelor & Gamal Segar", "amount": 1.0, "unit": "kg"},
            {"name": "Gula Merah", "amount": 0.2, "unit": "kg"},
            {"name": "Air Leri Beras", "amount": 3.0, "unit": "Liter"}
        ],
        "function": "Hormon Zeatin alami memperlambat penuaan sel daun, membuat daun tetap hijau segar dan produktif berfotosintesis.",
        "recipe": "1 kg daun kelor + daun gamal segar ditumbuk + 200 gram gula merah + 3 liter air leri. Fermentasi anaerob 7 hari."
    },
    {
        "name": "MOL Limbah Sayur & Buah Citrus",
        "hormone": "Enzim Protease & Amilase",
        "category": "Aktivator Kompos",
        "base_batch_liters": 6.0,
        "ingredients_structured": [
            {"name": "Limbah Kubis, Sawi, Jeruk", "amount": 2.0, "unit": "kg"},
            {"name": "Gula Pasir", "amount": 0.25, "unit": "kg"},
            {"name": "Air Cucian Beras", "amount": 4.0, "unit": "Liter"}
        ],
        "function": "Mempercepat pemecahan serat lignoselulosa pada pembuatan kompos padat serta mengusir lalat buah.",
        "recipe": "2 kg limbah kubis, sawi, dan kulit jeruk + 250 gram gula pasir + 4 liter air cucian beras. Fermentasi 7 hari."
    },
    {
        "name": "MOL Tapai Singkong & Ketan",
        "hormone": "Saccharomyces & Asam Laktat",
        "category": "Bio-Fermentor Serbaguna",
        "base_batch_liters": 3.5,
        "ingredients_structured": [
            {"name": "Tapai Singkong / Ketan", "amount": 0.5, "unit": "kg"},
            {"name": "Gula Merah", "amount": 0.25, "unit": "kg"},
            {"name": "Air Kelapa Tua", "amount": 3.0, "unit": "Liter"}
        ],
        "function": "Starter fermentasi instan untuk mempercepat proses pembuatan POC rumahan tanpa perlu membeli starter komersial.",
        "recipe": "500 gram tapai matang dihaluskan + 250 gram gula merah + 3 liter air kelapa tua. Fermentasi 5 hari hingga berbusa wangi."
    }
]

TROUBLESHOOT_DATABASE: List[POCTroubleshootItem] = [
    POCTroubleshootItem(
        id="bau_busuk_bangkai",
        symptom="POC Berbau Busuk Menyengat, Bau Bangkai, atau Bau Selokan",
        cause="Terjadi pembusukan anaerobik tak sempurna akibat kelebihan biomassa protein/nitrogen tanpa diimbangi sumber gula (karbon) yang cukup, atau starter mikroba asam laktat kalah bersaing dengan bakteri pembusuk anaerob.",
        risk_level="Waspada",
        solution=[
            "Segera tambahkan molase atau gula merah cair sebanyak 50 - 100 gram per liter larutan POC.",
            "Tambahkan inokulan starter aktif (EM4 100 ml atau 1 botol Yakult) untuk merebut dominasi bakteri asam laktat.",
            "Aduk rata selama 3-5 menit, lalu tutup kembali rapat-rapat.",
            "Dalam 48-72 jam bau bangkai akan ternetralkan menjadi aroma asam cuka/tape segar."
        ],
        prevention="Selalu jaga rasio gula minimal 5-10% dari total volume cairan dan pastikan wadah bersih bebas sisa minyak goreng/detergen."
    ),
    POCTroubleshootItem(
        id="jamur_putih_khamir",
        symptom="Muncul Lapisan Selaput / Jamur Putih Halus di Permukaan Cairan",
        cause="Lapisan ini adalah koloni khamir (yeast / Saccharomyces cerevisiae) atau Actinomycetes menguntungkan yang teroksigenasi di lapisan atas cairan. Fenomena ini SANGAT NORMAL dan justru menandakan fermentasi aktif.",
        risk_level="Aman",
        solution=[
            "Tidak perlu panik atau dibuang! Lapisan putih ini bukan racun.",
            "Cukup aduk kembali cairan agar lapisan khamir menyatu kembali dengan larutan.",
            "Bila mendekati panen, lapisan putih ini cukup disaring bersama ampas padat."
        ],
        prevention="Pastikan penutup wadah benar-benar kedap udara (anaerobik) bila ingin mengurangi pertumbuhan khamir permukaan."
    ),
    POCTroubleshootItem(
        id="jamur_hijau_hitam",
        symptom="Muncul Jamur Berwarna Hijau Gelap, Biru, atau Hitam Berbulu di Permukaan",
        cause="Kontaminasi oleh kapang liar patogenik (seperti Aspergillus niger liar atau Penicillium liar) yang masuk saat penutupan wadah tidak steril atau bahan baku sudah berjamur busuk sebelum diolah.",
        risk_level="Bahaya/Gagal",
        solution=[
            "Gunakan centong bersih, segera sendok dan angkat seluruh lapisan jamur hitam/hijau tersebut dan buang jauh-jauh.",
            "Rebus 500 gram gula kelapa dengan 1 liter air hingga mendidih, dinginkan, lalu tuang ke dalam POC.",
            "Tambahkan starter EM4 pekat 200 ml untuk merevitalisasi populasi bakteri baik.",
            "Bila setelah 5 hari bau berubah menjadi busuk anyir dan warna menghitam pekat, batch POC tersebut gagal dan harus dijadikan inokulan tanah jauh dari tanaman utama."
        ],
        prevention="Cuci bersih semua wadah dan rimpang sebelum fermentasi, gunakan air sumur matang/bersih, jangan gunakan air cucian piring."
    ),
    POCTroubleshootItem(
        id="tong_kembung_meledak",
        symptom="Drum Fermentasi Menggembung Keras, Mendesah Kuat, atau Tutup Terlempar",
        cause="Akumulasi gas CO2 dan metana bertekanan tinggi akibat aktivitas mikrobiologis yang sangat pesat di ruang kosong (headspace) wadah yang tertutup rapat tanpa sistem pelepasan gas.",
        risk_level="Bahaya Fisik",
        solution=[
            "Buka tutup drum perlahan-lahan (seperti membuka botol soda berkarbonasi) untuk meredakan tekanan secara bertahap.",
            "JANGAN mengisi wadah hingga leher penuh! Selalu sisakan minimal 15-20% ruang kosong di atas permukaan cairan sebagai kantung ekspansi gas.",
            "Pasang sistem instalasi AIRLOCK sederhana: buat lubang di tutup drum, pasang selang kecil aerator akuarium, rekatkan dengan lem tembak, dan celupkan ujung selang luar ke dalam botol plastik berisi air mineral. Gas akan keluar berupa gelembung tanpa ada oksigen luar yang masuk."
        ],
        prevention="Wajib sisakan headspace 15% dan gunakan sistem aerasi airlock atau buka tutup selama 10 detik setiap pagi."
    ),
    POCTroubleshootItem(
        id="ph_tinggi_tidak_turun",
        symptom="pH POC Tetap Tinggi (pH > 5.5) Setelah Lebih dari 14 Hari Fermentasi",
        cause="Bakteri fermentor asam laktat terhambat karena media kurang karbohidrat fermentasi, suhu terlalu dingin (<20°C), atau bahan dasar mengandung zat antibakteri berkadar tinggi tanpa starter yang cukup.",
        risk_level="Waspada",
        solution=[
            "Tambahkan 1-2 liter air kelapa tua segar (sumber asam amino & glukosa pembentuk asam asetat).",
            "Tambahkan 2 botol minuman probiotik Lactobacillus (Yakult) atau ragi tape yang sudah dihaluskan.",
            "Pindahkan drum ke tempat yang lebih hangat (suhu ruang 28 - 32 °C).",
            "Ukur pH kembali setelah 4-5 hari; POC matang ideal memiliki pH antara 3.5 hingga 4.8."
        ],
        prevention="Pastikan selalu menggunakan starter mikroba berkualitas dan larutkan gula merah/molase dengan baik."
    ),
    POCTroubleshootItem(
        id="cairan_keruh_berlumpur",
        symptom="Cairan POC Sangat Keruh, Mengendap Lumpur Pekat, Sering Menyumbat Nozzle Sprayer",
        cause="Ampas biomassa buah/sayur/sabut kelapa terhancurkan terlalu halus saat blending sehingga partikel mikron melayang dan menyumbat saringan semprot.",
        risk_level="Aman",
        solution=[
            "Lakukan pengendapan pasif selama 48 jam di wadah terpisah sebelum dimasukkan ke jerigen simpan.",
            "Gunakan metode saringan bertingkat: lapis pertama kawat strimin nyamuk (menyaring serat kasar), lapis kedua kain mori/kain kaos bersih, lapis ketiga kain peras tahu atau saringan nilon 100 mesh.",
            "Saat memompa POC dari drum ke tangki semprot, jangan mengaduk endapan lumpur di dasar wadah."
        ],
        prevention="Hindari memblender bahan hingga jadi pasta halus berair; cukup tumbuk atau cacah halus 0.5 - 1 cm."
    )
]

TANK_MIX_DATABASE: List[POCTankMixItem] = [
    POCTankMixItem(
        partner_material="Pestisida Nabati (Mimba, Tembakau, Bawang Putih, Sirih, Serai)",
        status="Sangat Dianjurkan (Sinergis)",
        rule="Bisa dicampur langsung dalam satu tangki semprot sesaat sebelum aplikasi.",
        scientific_reason="Zat aktif repellent alami (azadiraktin, allicin, minyak atsiri) tidak membunuh mikroba probiotik POC, justru saling menguatkan daya tahan tanaman terhadap hama hisap."
    ),
    POCTankMixItem(
        partner_material="Perekat & Perata Alami (Getah Lidah Buaya, Putih Telur, Minyak Kelapa)",
        status="Sangat Dianjurkan (Sinergis)",
        rule="Gunakan 1-2 sendok makan per tangki semprot 16 Liter, aduk hingga berbusa halus.",
        scientific_reason="Menurunkan tegangan permukaan air semprot sehingga butiran kabut menempel kuat di permukaan daun berlapislilin (misal daun talas atau bawang) dan tahan luntur dari tetesan embun/hujan."
    ),
    POCTankMixItem(
        partner_material="Pupuk Kimia Sintetis Dosis Rendah (Urea / NPK Mutiara 10-20% Dosis Normal)",
        status="Boleh dengan Syarat (Semi-Organik)",
        rule="Larutkan butiran NPK terlebih dahulu dalam ember air terpisah hingga larut sempurna, baru campurkan POC ke dalam tangki.",
        scientific_reason="Asam organik dan asam amino dalam POC bertindak sebagai zat kelasi (chelating agent) alami yang mempermudah ion N-P-K sintetis diserap oleh stomata daun."
    ),
    POCTankMixItem(
        partner_material="Fungisida Kimia Kontak / Sistemik (Mankozeb, Karbendazim, Difenokonazol)",
        status="DILARANG KERAS",
        rule="JANGAN DICAMPUR! Berikan jeda waktu minimal 4 sampai 5 hari antara aplikasi POC dan fungisida kimia.",
        scientific_reason="Bahan aktif fungisida kimia bersifat biosida spektrum luas yang langsung membunuh jamur baik (seperti Trichoderma) dan khamir bermanfaat yang terkandung di dalam POC."
    ),
    POCTankMixItem(
        partner_material="Bakterisida / Senyawa Tembaga (Kupfer / Tembaga Oksiklorida / Streptomisin)",
        status="DILARANG KERAS",
        rule="DILARANG KERAS dicampur dalam satu tangki.",
        scientific_reason="Ion tembaga (Cu2+) dan antibiotik melumpuhkan dinding sel bakteri Bacillus, Lactobacillus, dan Pseudomonas dalam POC sehingga pupuk cair kehilangan fungsi biologisnya."
    ),
    POCTankMixItem(
        partner_material="Air PDAM yang Mengandung Kaporit / Klorin Tinggi",
        status="DILARANG KERAS",
        rule="Gunakan selalu air sumur, air hujan, atau endapkan air PDAM minimal 24 jam di wadah terbuka di bawah sinar matahari sebelum dicampur POC.",
        scientific_reason="Klorin dan kaporit dirancang khusus sebagai agen pembunuh bakteri (desinfektan) yang akan mensterilkan mikroorganisme hidup dalam pupuk organik cair seketika."
    )
]

def calculate_liquid_dosage(req: LiquidDoseRequest) -> LiquidDoseResponse:
    crop = req.crop_category.lower()
    method = req.application_method.lower()
    vol = req.volume_liters
    age = req.target_plant_age_days or 30

    if "semprot" in method or "spray" in method or "daun" in method:
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
        # Drenching / Kocor Akar
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

# --- NEW: SMART POC BREWING FORMULATOR & BATCH ENGINE ---

def calculate_poc_batch_brew(req: POCBatchBrewRequest) -> POCBatchBrewResponse:
    v = req.drum_volume_liters
    purpose = req.purpose.lower()
    ftype = req.fermentation_type.lower()

    # Headspace safety buffer: 15% of drum capacity
    headspace = round(v * 0.15, 1)
    eff_vol = round(v * 0.85, 1)

    ingredients: List[POCBrewIngredient] = []

    if "vegetatif" in purpose:
        title = "Formula POC Booster Vegetatif & Daun Hijau Pekat (Tinggi N & Sitokinin)"
        est_npk = "N: 3.2% - P2O5: 0.8% - K2O: 1.2%"
        days = "10 - 14 Hari"
        ph_t = "4.2 - 4.8"
        
        # Scaling ratios based on effective volume
        urine_l = round(eff_vol * 0.45, 1)
        kelapa_l = round(eff_vol * 0.20, 1)
        daun_kg = round(eff_vol * 0.15, 1)
        molase_kg = round(eff_vol * 0.06, 1)
        starter_l = round(max(0.2, eff_vol * 0.04), 2)
        air_l = round(eff_vol - (urine_l + kelapa_l + daun_kg + molase_kg + starter_l), 1)

        ingredients = [
            POCBrewIngredient(name="Urine Kelinci / Sapi Matang", amount=urine_l, unit="Liter", category="Cairan Dasar", role="Sumber Nitrogen amida organik & mineral makro", cost_est=urine_l * 1500),
            POCBrewIngredient(name="Air Kelapa Tua", amount=kelapa_l, unit="Liter", category="Cairan Dasar", role="Booster hormon sitokinin & kalium organik", cost_est=kelapa_l * 1000),
            POCBrewIngredient(name="Daun Gamal / Daun Kelor Halus", amount=daun_kg, unit="kg", category="Biomassa Organik", role="Kaya protein daun & hormon Zeatin alami", cost_est=daun_kg * 500),
            POCBrewIngredient(name="Molase / Tetes Tebu Murni", amount=molase_kg, unit="kg", category="Sumber Gula/Energi", role="Pakan energi untuk aktivasi mikroba probiotik", cost_est=molase_kg * 8000),
            POCBrewIngredient(name="Inokulan EM4 / Biang ROTAN", amount=starter_l, unit="Liter", category="Inokulan Starter", role="Konsorsium bakteri asam laktat & pelarut N", cost_est=starter_l * 25000),
            POCBrewIngredient(name="Air Sumur Non-Kaporit", amount=max(0.0, air_l), unit="Liter", category="Cairan Dasar", role="Pelarut penyeimbang volume", cost_est=0.0)
        ]
        prep_steps = [
            "Tampung urine ternak dan saring dari kotoran padat maupun bulu.",
            "Tumbuk atau blender daun gamal/kelor bersama 2 liter air kelapa hingga halus.",
            "Larutkan molase dengan air kelapa hangat hingga homogen, dinginkan.",
            "Masukkan seluruh cairan urine, jus daun hijau, larutan molase, dan starter ke dalam tong.",
            "Tambahkan air sumur hingga mencapai batas volume efektif (sisakan headspace 15%).",
            "Aduk merata selama 3-5 menit searah jarum jam.",
            "Tutup tong rapat-rapat. Pasang selang airlock atau klem penutup."
        ]
        degas = "Buka tutup selama 10 detik tiap pagi pada 5 hari pertama (atau gunakan airlock otomatis)."

    elif "generatif" in purpose:
        title = "Formula POC Booster Pembungaan & Pengisian Buah (Tinggi K, P & Ca)"
        est_npk = "N: 1.1% - P2O5: 2.4% - K2O: 3.5%"
        days = "14 - 18 Hari"
        ph_t = "4.5 - 5.2"

        kelapa_l = round(eff_vol * 0.40, 1)
        sabut_kg = round(eff_vol * 0.15, 1)
        kulit_pisang_kg = round(eff_vol * 0.12, 1)
        cangkang_telur_kg = round(eff_vol * 0.05, 1)
        molase_kg = round(eff_vol * 0.07, 1)
        starter_l = round(max(0.2, eff_vol * 0.04), 2)
        air_l = round(eff_vol - (kelapa_l + sabut_kg + kulit_pisang_kg + cangkang_telur_kg + molase_kg + starter_l), 1)

        ingredients = [
            POCBrewIngredient(name="Air Kelapa Tua", amount=kelapa_l, unit="Liter", category="Cairan Dasar", role="Pemasok Kalium alami dan glukosa fermentasi", cost_est=kelapa_l * 1000),
            POCBrewIngredient(name="Sabut Kelapa Kering (Cacah)", amount=sabut_kg, unit="kg", category="Biomassa Organik", role="Kandungan Kalium (K2O) organik sangat tinggi", cost_est=sabut_kg * 800),
            POCBrewIngredient(name="Kulit Pisang Matang (Cacah)", amount=kulit_pisang_kg, unit="kg", category="Biomassa Organik", role="Booster gula buah, magnesium, dan kalium bebas", cost_est=kulit_pisang_kg * 1000),
            POCBrewIngredient(name="Cangkang Telur Sangrai Halus", amount=cangkang_telur_kg, unit="kg", category="Aditif Mineral", role="Kalsium (Ca) pekat untuk memperkokoh tangkai bunga", cost_est=cangkang_telur_kg * 2000),
            POCBrewIngredient(name="Molase / Gula Merah", amount=molase_kg, unit="kg", category="Sumber Gula/Energi", role="Energi fermentasi mikroba perombak kalium", cost_est=molase_kg * 8000),
            POCBrewIngredient(name="Starter Dekomposer / EM4", amount=starter_l, unit="Liter", category="Inokulan Starter", role="Bakteri pelarut fosfat & fermentor anaerob", cost_est=starter_l * 25000),
            POCBrewIngredient(name="Air Sumur Non-Kaporit", amount=max(0.0, air_l), unit="Liter", category="Cairan Dasar", role="Pelarut penyeimbang volume", cost_est=0.0)
        ]
        prep_steps = [
            "Cacah kecil sabut kelapa dan kulit pisang agar luas kontak ekstraksi mikroba maksimal.",
            "Tumbuk halus cangkang telur yang telah disangrai hingga menjadi tepung kalsium.",
            "Larutkan molase ke dalam sebagian air kelapa, aduk hingga larut.",
            "Masukkan sabut kelapa, kulit pisang, tepung cangkang telur ke dalam drum.",
            "Tuangkan air kelapa, larutan molase, air sumur, dan starter mikroba ke dalam drum.",
            "Aduk merata hingga seluruh bahan basah terendam sempurna.",
            "Tutup rapat wadah dan simpan di area yang terlindung dari sinar matahari langsung."
        ]
        degas = "Aduk setiap 3 hari sekali selama 1-2 menit untuk memaksimalkan ekstraksi kalium dari sabut kelapa."

    elif "fish_amino" in purpose:
        title = "Formula POC Asam Amino Ikan (FAA) - Regenerasi Sel & Hormon Pertumbuhan"
        est_npk = "N: 3.8% - P2O5: 1.5% - K2O: 0.9%"
        days = "21 - 30 Hari"
        ph_t = "3.8 - 4.4"

        ikan_kg = round(eff_vol * 0.35, 1)
        gula_kg = round(eff_vol * 0.30, 1)
        nanas_kg = round(eff_vol * 0.08, 1)
        kelapa_l = round(eff_vol * 0.15, 1)
        starter_l = round(max(0.1, eff_vol * 0.03), 2)
        air_l = round(eff_vol - (ikan_kg + gula_kg + nanas_kg + kelapa_l + starter_l), 1)

        ingredients = [
            POCBrewIngredient(name="Ikan Laut Segar / Jeroan Ikan", amount=ikan_kg, unit="kg", category="Biomassa Organik", role="Polipeptida, protein kasar & asam amino murni", cost_est=ikan_kg * 4000),
            POCBrewIngredient(name="Gula Merah Aren / Molase Kental", amount=gula_kg, unit="kg", category="Sumber Gula/Energi", role="Osmotik tinggi pengekstraksi cairan sel ikan", cost_est=gula_kg * 8000),
            POCBrewIngredient(name="Nanas Matang (Jus)", amount=nanas_kg, unit="kg", category="Biomassa Organik", role="Enzim bromelin pemecah protein menjadi peptida", cost_est=nanas_kg * 3000),
            POCBrewIngredient(name="Air Kelapa Tua", amount=kelapa_l, unit="Liter", category="Cairan Dasar", role="Media cair pembawa mikroba & penstabil pH", cost_est=kelapa_l * 1000),
            POCBrewIngredient(name="Inokulan Probiotik EM4", amount=starter_l, unit="Liter", category="Inokulan Starter", role="Kultur mikroba pencerna protein hewani", cost_est=starter_l * 25000),
            POCBrewIngredient(name="Air Bersih Non-Kaporit", amount=max(0.0, air_l), unit="Liter", category="Cairan Dasar", role="Penyesuai volume", cost_est=0.0)
        ]
        prep_steps = [
            "Cacah ikan laut segar (jangan dicuci dengan air kaporit).",
            "Haluskan nanas matang menggunakan blender.",
            "Campurkan potongan ikan dan gula aren/molase dengan perbandingan 1:1 di dalam wadah hingga seluruh ikan terlumuri.",
            "Tambahkan jus nanas, air kelapa, dan inokulan probiotik.",
            "Tutup rapat wadah dengan klem kedap udara ber-airlock.",
            "Simpan di tempat teduh bersuhu ruang (25 - 30 °C).",
            "Pada hari ke-21 atau 30, panen ekstrak cairan pekat berwarna cokelat wangi gurih seperti kecap."
        ]
        degas = "Gunakan instalasi airlock selang celup air agar gas fermentasi keluar otomatis tanpa masuknya lalat."

    elif "psb" in purpose:
        title = "Formula POC Bakteri Fotosintesis / PSB (Rhodopseudomonas Palustris)"
        est_npk = "N: 1.5% - P2O5: 0.9% - K2O: 0.8%"
        days = "15 - 20 Hari (Jemur Panas Matahari)"
        ph_t = "6.5 - 7.5"

        telur_butir = round(max(2.0, eff_vol * 0.4), 0)
        msg_gram = round(telur_butir * 15, 0)
        terasi_gram = round(telur_butir * 15, 0)
        air_l = round(eff_vol * 0.92, 1)
        biang_l = round(eff_vol * 0.05, 1)

        ingredients = [
            POCBrewIngredient(name="Telur Ayam / Bebek Mentah", amount=telur_butir, unit="butir", category="Biomassa Organik", role="Kaya protein dan sulfur sebagai nutrisi bakteri sulfur", cost_est=telur_butir * 2500),
            POCBrewIngredient(name="Penyedap Rasa (MSG)", amount=msg_gram, unit="gram", category="Sumber Gula/Energi", role="Sumber asam glutamat organik pemacu klorofil", cost_est=(msg_gram / 100) * 4000),
            POCBrewIngredient(name="Terasi Matang / Saus Tiram", amount=terasi_gram, unit="gram", category="Biomassa Organik", role="Penyedia fosfor organik & senyawa volatil perangsang PSB", cost_est=(terasi_gram / 100) * 3000),
            POCBrewIngredient(name="Biang PSB Merah Indukan", amount=biang_l, unit="Liter", category="Inokulan Starter", role="Starter indukan Rhodopseudomonas aktif", cost_est=biang_l * 10000),
            POCBrewIngredient(name="Air Sumur / Kolam Ikan", amount=air_l, unit="Liter", category="Cairan Dasar", role="Media jernih transparan untuk penetrasi sinar UV", cost_est=0.0)
        ]
        prep_steps = [
            "Kocok lepas seluruh butir telur bersama MSG dan terasi hingga larut homogen.",
            "Tuangkan adonan telur ke dalam wadah bening transparan (galon/botol bening).",
            "Tambahkan air sumur atau air kolam hingga mendekati batas atas (sisakan ruang udara 5 cm).",
            "Tambahkan biang PSB merah indukan lalu kocok botol hingga merata.",
            "Tutup botol rapat-rapat.",
            "Letakkan di area terbuka yang terkena sinar matahari terik langsung dari pagi hingga sore.",
            "Kocok botol sehari sekali setiap pagi.",
            "Panen saat cairan berubah menjadi merah rubi atau ungu tua pekat mengkilap."
        ]
        degas = "Cukup kocok botol di pagi hari; bila terlalu kencang tekanannya kendurkan tutup 2 detik."

    else:
        # ALL PURPOSE / ROTAN STYLE
        title = "Formula POC All-Purpose Komplit (Nutrisi Seimbang & Probiotik Tanah)"
        est_npk = "N: 2.5% - P2O5: 1.8% - K2O: 2.2%"
        days = "10 - 14 Hari"
        ph_t = "4.0 - 4.6"

        kelapa_l = round(eff_vol * 0.25, 1)
        leri_l = round(eff_vol * 0.25, 1)
        buah_kg = round(eff_vol * 0.15, 1)
        sayur_kg = round(eff_vol * 0.10, 1)
        molase_kg = round(eff_vol * 0.07, 1)
        starter_l = round(max(0.2, eff_vol * 0.04), 2)
        air_l = round(eff_vol - (kelapa_l + leri_l + buah_kg + sayur_kg + molase_kg + starter_l), 1)

        ingredients = [
            POCBrewIngredient(name="Air Kelapa Tua", amount=kelapa_l, unit="Liter", category="Cairan Dasar", role="Kalium alami & ZPT sitokinin", cost_est=kelapa_l * 1000),
            POCBrewIngredient(name="Air Cucian Beras (Leri)", amount=leri_l, unit="Liter", category="Cairan Dasar", role="Vitamin B kompleks & inokulan pati", cost_est=0.0),
            POCBrewIngredient(name="Limbah Buah Matang Manis", amount=buah_kg, unit="kg", category="Biomassa Organik", role="Pemasok gula alami, enzim, & mineral buah", cost_est=buah_kg * 800),
            POCBrewIngredient(name="Sayuran Hijau / Kangkung", amount=sayur_kg, unit="kg", category="Biomassa Organik", role="Klorofil, zat besi, & nitrogen nabati", cost_est=sayur_kg * 500),
            POCBrewIngredient(name="Molase / Gula Merah", amount=molase_kg, unit="kg", category="Sumber Gula/Energi", role="Bahan bakar energi utama mikroba probiotik", cost_est=molase_kg * 8000),
            POCBrewIngredient(name="Starter ROTAN / EM4", amount=starter_l, unit="Liter", category="Inokulan Starter", role="Kultur mikroba majemuk teruji", cost_est=starter_l * 25000),
            POCBrewIngredient(name="Air Bersih Non-Kaporit", amount=max(0.0, air_l), unit="Liter", category="Cairan Dasar", role="Penyeimbang volume drum", cost_est=0.0)
        ]
        prep_steps = [
            "Blender atau cacah halus limbah buah dan sayuran hijau.",
            "Rebus molase atau gula merah dengan sedikit air hingga larut, lalu dinginkan.",
            "Campurkan jus buah-sayur, air kelapa, air leri, larutan gula dingin, dan starter mikroba ke dalam drum.",
            "Aduk rata selama 5 menit hingga homogen.",
            "Tutup drum secara rapat anaerobik.",
            "Buka tutup selama 10 detik setiap 2 hari sekali untuk mengeluarkan desisan gas fermentasi.",
            "Panen pada hari ke 10-14 saat bau berubah menjadi harum tape asam segar."
        ]
        degas = "Degassing rutin 2 hari sekali atau gunakan selang airlock peredam gas."

    total_cost = sum(i.cost_est for i in ingredients)
    cost_per_l = round(total_cost / eff_vol, 0) if eff_vol > 0 else 0

    indicators = [
        "Aroma berubah drastis dari bau bahan mentah menjadi aroma asam segar mirip tape ketan atau wine.",
        f"Derajat keasaman (pH) turun ke rentang target {ph_t}.",
        "Tidak ada lagi letupan atau desisan gas aktif saat wadah dibuka.",
        "Terbentuk lapisan khamir/selaput putih halus di permukaan atas cairan (tanda koloni menguntungkan).",
        "Warna cairan matang menjadi cokelat keemasan / cokelat teh pekat yang homogen."
    ]

    return POCBatchBrewResponse(
        drum_volume_liters=v,
        effective_liquid_liters=eff_vol,
        headspace_liters=headspace,
        purpose_title=title,
        fermentation_type="Anaerobik Kedap Udara" if "anaerob" in ftype else "Aerobik / Terang Terbuka",
        estimated_duration_days=days,
        target_ph=ph_t,
        estimated_npk=est_npk,
        estimated_total_cost=round(total_cost, 0),
        estimated_cost_per_liter=cost_per_l,
        ingredients=ingredients,
        preparation_steps=prep_steps,
        degassing_protocol=degas,
        maturation_indicators=indicators
    )

# --- NEW: FIELD-SCALE SPRAY & DRENCH CALENDAR SCHEDULER ---

def calculate_field_schedule(req: POCFieldScheduleRequest) -> POCFieldScheduleResponse:
    crop = req.crop_name.strip()
    area = req.land_area_sqm
    tank_cap = req.tank_capacity_liters

    # Standard water volume per hectare (10,000 m²) is typically 300 - 400 Liters for foliar spray
    # For 1,000 m² = ~35 Liters (approx 2 - 2.5 tanks of 16L)
    water_factor = (area / 10000.0) * 350.0  # liters of water per round
    tanks_per_round = max(1, round(water_factor / tank_cap))

    stages: List[POCFieldStage] = []
    crop_lower = crop.lower()

    if "padi" in crop_lower:
        stages = [
            POCFieldStage(
                stage_name="Fase 1: Perlakuan Benih (Seed Soaking)",
                timing="Pra-Tanam (Rendam Benih 12-24 Jam)",
                target_focus="Pematahan dormansi biji, sterilisasi patogen tular-benih, memicu kecambah serempak",
                dose_per_tank="10 ml per Liter air (1 : 100)",
                method="Perendaman Gabah Benih",
                water_volume_est=round(area * 0.015, 1),
                poc_volume_est=round((area * 0.015) * 0.01, 2),
                tank_count_est=1,
                notes="Tiriskan benih setelah direndam, lalu peram 24 jam hingga bintik putih calon akar muncul."
            ),
            POCFieldStage(
                stage_name="Fase 2: Vegetatif Awal & Pembentukan Anakan",
                timing="10 - 15 HST (Hari Setelah Tanam)",
                target_focus="Merangsang akar baru mengcengkeram tanah dan memicu anakan tunas produktif",
                dose_per_tank=f"{round(tank_cap * 15, 0)} cc per tangki ({round(15.0, 1)} cc/L)",
                method="Semprot Kabut Daun Pagi Hari",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.015, 2),
                tank_count_est=tanks_per_round,
                notes="Semprotkan merata di bawah jam 09.00 pagi saat stomata daun padi terbuka sempurna."
            ),
            POCFieldStage(
                stage_name="Fase 3: Multiplikasi Anakan Maksimal",
                timing="25 - 30 HST",
                target_focus="Memaksimalkan anakan produktif menjadi batang utama pembawa malai",
                dose_per_tank=f"{round(tank_cap * 15, 0)} cc per tangki ({round(15.0, 1)} cc/L)",
                method="Semprot Daun & Pangkal Batang",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.015, 2),
                tank_count_est=tanks_per_round,
                notes="Bisa dikombinasikan dengan MOL Bonggol Pisang untuk dorongan hormon sitokinin."
            ),
            POCFieldStage(
                stage_name="Fase 4: Primordia / Bunting Kecil",
                timing="45 - 50 HST",
                target_focus="Persiapan bakal malai bulir padi, memperkuat leher malai agar tidak patah/busuk",
                dose_per_tank=f"{round(tank_cap * 12, 0)} cc per tangki ({round(12.0, 1)} cc/L)",
                method="Semprot Kabut Halus Permukaan Daun",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.012, 2),
                tank_count_est=tanks_per_round,
                notes="Gunakan formula POC tinggi Kalium & Kalsium. Hentikan pemakaian nitrogen tinggi."
            ),
            POCFieldStage(
                stage_name="Fase 5: Pengisian Bulir Padi (Prematur Padi Menguning)",
                timing="65 - 70 HST (Pasca Bunga Mekar Serempak)",
                target_focus="Mengisi bulir gabah hingga ke pangkal malai agar padi bernas padat dan tidak hampa",
                dose_per_tank=f"{round(tank_cap * 10, 0)} cc per tangki ({round(10.0, 1)} cc/L)",
                method="Semprot Kabut Halus Daun Bendera",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.010, 2),
                tank_count_est=tanks_per_round,
                notes="Jaga daun bendera tetap hijau segar berfotosintesis. JANGAN semprot saat padi sedang berbunga mekar jam 09.30-11.30!"
            )
        ]
    elif "cabai" in crop_lower or "tomat" in crop_lower:
        stages = [
            POCFieldStage(
                stage_name="Fase 1: Bibit & Adaptasi Tanam",
                timing="7 - 10 HST",
                target_focus="Mencegah stres bibit pindah tanam dan merangsang serabut akar",
                dose_per_tank=f"{round(tank_cap * 8, 0)} cc per tangki ({round(8.0, 1)} cc/L)",
                method="Kocor 100 ml per lubang tanam",
                water_volume_est=round(water_factor * 0.8, 1),
                poc_volume_est=round(water_factor * 0.8 * 0.008, 2),
                tank_count_est=max(1, tanks_per_round - 1),
                notes="Kocorkan tepat di pangkal batang basah."
            ),
            POCFieldStage(
                stage_name="Fase 2: Vegetatif & Percabangan Y",
                timing="20 - 25 HST",
                target_focus="Memperbanyak cabang produktif dan mempertebal helai daun hijau",
                dose_per_tank=f"{round(tank_cap * 15, 0)} cc per tangki ({round(15.0, 1)} cc/L)",
                method="Semprot Daun Merata",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.015, 2),
                tank_count_est=tanks_per_round,
                notes="Semprotkan ke bagian bawah daun tempat stomata berada."
            ),
            POCFieldStage(
                stage_name="Fase 3: Muncul Kuncup Bunga Pertama",
                timing="35 - 40 HST",
                target_focus="Mencegah kerontokan bunga dan memperkuat tangkai bunga",
                dose_per_tank=f"{round(tank_cap * 12, 0)} cc per tangki ({round(12.0, 1)} cc/L)",
                method="Semprot Kabut Halus",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.012, 2),
                tank_count_est=tanks_per_round,
                notes="Campurkan POC Kalsium & Kalium (cangkang telur + sabut kelapa)."
            ),
            POCFieldStage(
                stage_name="Fase 4: Pembesaran Buah & Pematangan",
                timing="55 - 65 HST",
                target_focus="Mempercepat pembesaran buah cabai, mengkilapkan kulit buah, dan menambah bobot",
                dose_per_tank=f"{round(tank_cap * 15, 0)} cc per tangki ({round(15.0, 1)} cc/L)",
                method="Semprot Daun & Kocor Bergantian",
                water_volume_est=round(water_factor * 1.2, 1),
                poc_volume_est=round(water_factor * 1.2 * 0.015, 2),
                tank_count_est=tanks_per_round + 1,
                notes="Ulangi aplikasi setiap 7 hari sekali pasca pemetikan panen cabai."
            )
        ]
    elif "bawang" in crop_lower:
        stages = [
            POCFieldStage(
                stage_name="Fase 1: Tunas & Perakaran Awal",
                timing="7 - 10 HST",
                target_focus="Mempercepat kemunculan daun dan perakaran kuat",
                dose_per_tank=f"{round(tank_cap * 10, 0)} cc per tangki ({round(10.0, 1)} cc/L)",
                method="Semprot Kabut Pagi",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.010, 2),
                tank_count_est=tanks_per_round,
                notes="Tambahkan perekat lidah buaya karena daun bawang berlapis lilin licin."
            ),
            POCFieldStage(
                stage_name="Fase 2: Pertumbuhan Anakan Rumpun",
                timing="20 - 25 HST",
                target_focus="Memperbanyak jumlah anakan umbi dalam satu rumpun",
                dose_per_tank=f"{round(tank_cap * 15, 0)} cc per tangki ({round(15.0, 1)} cc/L)",
                method="Semprot Kabut Daun & Pangkal Umbi",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.015, 2),
                tank_count_est=tanks_per_round,
                notes="Kombinasikan dengan POC Empon-Empon untuk cegah jamur trotol (Alternaria porri)."
            ),
            POCFieldStage(
                stage_name="Fase 3: Pembesaran Umbi & Pengerasan Dinding",
                timing="35 - 45 HST",
                target_focus="Mengisi umbi bawang agar padat, merah mengkilap, dan tidak menyusut saat simpan",
                dose_per_tank=f"{round(tank_cap * 15, 0)} cc per tangki ({round(15.0, 1)} cc/L)",
                method="Semprot Daun & Kocor Lembap",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.015, 2),
                tank_count_est=tanks_per_round,
                notes="Gunakan formula tinggi Kalium & Silika. Hentikan aplikasi 10 hari menjelang panen."
            )
        ]
    elif "sayur" in crop_lower:
        stages = [
            POCFieldStage(
                stage_name="Fase 1: Pertumbuhan Daun Awal",
                timing="5 - 7 HST",
                target_focus="Memicu fotosintesis cepat dan penguatan perakaran sayuran daun",
                dose_per_tank=f"{round(tank_cap * 8, 0)} cc per tangki ({round(8.0, 1)} cc/L)",
                method="Semprot Halus Pagi Hari",
                water_volume_est=round(water_factor * 0.8, 1),
                poc_volume_est=round(water_factor * 0.8 * 0.008, 2),
                tank_count_est=tanks_per_round,
                notes="Konsentrasi ringan agar daun muda tidak terbakar."
            ),
            POCFieldStage(
                stage_name="Fase 2: Pembesaran Helai Daun & Batang",
                timing="14 - 16 HST",
                target_focus="Memperlebar daun, warna hijau royo-royo, dan tekstur renyah",
                dose_per_tank=f"{round(tank_cap * 12, 0)} cc per tangki ({round(12.0, 1)} cc/L)",
                method="Semprot Merata Atas & Bawah Daun",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.012, 2),
                tank_count_est=tanks_per_round,
                notes="Gunakan POC Urine Kelinci atau POC Asam Amino Ikan."
            ),
            POCFieldStage(
                stage_name="Fase 3: Pra-Panen Sehat",
                timing="21 - 25 HST (5-7 Hari Sebelum Panen)",
                target_focus="Mempertahankan kesegaran daun pasca panen dan bebas residu kimia",
                dose_per_tank=f"{round(tank_cap * 10, 0)} cc per tangki ({round(10.0, 1)} cc/L)",
                method="Semprot Kabut Embun Pagi",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.010, 2),
                tank_count_est=tanks_per_round,
                notes="Organik 100%, aman langsung dikonsumsi setelah dicuci bersih."
            )
        ]
    else:
        # Generic / Hortikultura Umum
        stages = [
            POCFieldStage(
                stage_name="Fase 1: Vegetatif Awal",
                timing="10 - 15 HST",
                target_focus="Pertumbuhan daun, akar, dan batang",
                dose_per_tank=f"{round(tank_cap * 10, 0)} cc per tangki ({round(10.0, 1)} cc/L)",
                method="Semprot Daun Pagi Hari",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.010, 2),
                tank_count_est=tanks_per_round,
                notes="Semprot saat stomata terbuka."
            ),
            POCFieldStage(
                stage_name="Fase 2: Vegetatif Aktif",
                timing="25 - 30 HST",
                target_focus="Percabangan dan penguatan struktur tanaman",
                dose_per_tank=f"{round(tank_cap * 15, 0)} cc per tangki ({round(15.0, 1)} cc/L)",
                method="Semprot Daun & Kocor",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.015, 2),
                tank_count_est=tanks_per_round,
                notes="Gunakan formula seimbang."
            ),
            POCFieldStage(
                stage_name="Fase 3: Generatif (Bunga & Buah)",
                timing="45 - 55 HST",
                target_focus="Mencegah kerontokan bunga dan pengisian bobot buah",
                dose_per_tank=f"{round(tank_cap * 15, 0)} cc per tangki ({round(15.0, 1)} cc/L)",
                method="Semprot Kabut Halus",
                water_volume_est=round(water_factor, 1),
                poc_volume_est=round(water_factor * 0.015, 2),
                tank_count_est=tanks_per_round,
                notes="Tingkatkan Kalium dan Kalsium."
            )
        ]

    total_poc = round(sum(s.poc_volume_est for s in stages), 2)
    total_water = round(sum(s.water_volume_est for s in stages), 1)
    total_rounds = len(stages)

    area_desc = f"{area:,.0f} m² ({round(area / 10000.0, 2)} Hektar)" if area >= 10000 else f"{area:,.0f} m² ({round(area / 100.0, 1)} Ru / Bata)"

    savings = f"Penggunaan POC rutin di lahan {area_desc} menghemat hingga 40% - 60% kebutuhan pupuk sintetis (Urea/NPK) dengan estimasi penghematan biaya Rp {(area/10000.0)*1800000:,.0f} per musim tanam."

    rules = [
        "Selalu gunakan air sumur/mata air (bebas kaporit/klorin).",
        "Waktu penyemprotan terbaik: 06.30 - 09.00 pagi atau 15.30 - 17.30 sore.",
        "Arahkan nozzle sprayer ke arah bawah daun dengan kabut halus (mist) untuk penyerapan stomata maksimal.",
        "Gunakan perekat alami (putih telur / lidah buaya) saat musim hujan agar nutrisi tidak tercuci.",
        "Beri jeda minimal 4-5 hari apabila lahan diaplikasikan fungisida kimia keras."
    ]

    return POCFieldScheduleResponse(
        crop_name=crop,
        land_area_sqm=area,
        land_area_desc=area_desc,
        tank_capacity_liters=tank_cap,
        total_seasonal_poc_liters=total_poc,
        total_seasonal_water_liters=total_water,
        total_spraying_rounds=total_rounds,
        stages=stages,
        economic_savings_est=savings,
        application_rules=rules
    )

def get_troubleshoot_database() -> List[POCTroubleshootItem]:
    return TROUBLESHOOT_DATABASE

def get_tank_mix_guide() -> List[POCTankMixItem]:
    return TANK_MIX_DATABASE
