# AgriSensa BioFertilizer Studio

**Platform Cerdas Formulasi & Optimasi Pupuk Organik (Padat & Cair)** 
*Ditenagai Backend Python (FastAPI), Heuristic/AI Optimizer, dan Validasi Standar SNI*

---

## Ringkasan Proyek

**AgriSensa BioFertilizer Studio** adalah web aplikasi independen khusus untuk formulasi, monitoring fermentasi, dan analisis ekonomi pupuk organik. Dikembangkan dengan memisahkan dan mematangkan konsep agroteknologi unggulan dari ekosistem `agrisensa-api`, platform ini dirancang dengan standar industri agar siap di-deploy langsung ke **Render**, **Railway**, atau **Docker Cloud Platform**.

---

## 2 Fitur Utama

### 1. Pupuk Organik Padat (Kompos & Bokashi)
* **Smart Formulator & Analisis C/N**: Mengkalkulasi akumulasi massa karbon (C), nitrogen (N), fosfor (P), kalium (K), dan rasio C/N awal dari **24+ database bahan baku** lengkap:
  * **Kotoran Ternak**: Sapi, Kambing/Domba, Ayam, Burung Puyuh, Kelinci, Guano Kelelawar.
  * **Karbon & Bulking Agent**: Sekam Mentah, Arang Sekam, Jerami Cacah, Dedak Halus, Serbuk Gergaji, Abu Kayu, Dolomit, Cangkang Telur.
  * **Limbah Organik Sampah Pasar & Dapur**: Sampah Sayuran Hijau Segar, Sampah Kulit Buah-Buahan, Sampah Sisa Makanan Dapur (*Food Waste*), Ampas Kopi (*Spent Coffee Grounds*), Ampas Tahu Basah, Limbah Baglog Jamur Tiram, Sampah Daun Kering / Serasah Taman, Eceng Gondok Rawa, Tandan Kosong Kelapa Sawit (TKKS), dan Limbah Kulit Bawang.
* **Simulasi Fase Fermentasi Dinamis**: Memproyeksikan kurva degradasi C/N dari awal (~28:1) menuju kematangan stabil (12-15:1) serta tahapan suhu (Mesofilik 25-45°C → Termofilik 55-65°C → Pendinginan → Pematangan).
* ** AI Recipe Optimizer**: Algoritma optimasi terikat (*Constrained Optimization* / SLSQP) yang membagi takaran proporsi bahan baku secara otomatis sesuai target bobot dan target C/N tanpa risiko kegagalan fermentasi.
* ** Validasi SNI 19-7030-2004**: Audit otomatis parameter mutu kompos (C/N, C-Organik, N-total, P2O5, K2O, dan kadar air).
* ** Ensiklopedia Resep Bokashi Lapangan**: Panduan Bokashi ROTAN 1 Hektar, Bokashi Ayam Sayuran (N-Tinggi), Bokashi Guano Buah (P-Tinggi), Bokashi Sapi Pembenah Tanah, Kompos Sampah Pasar Aerob Cepat, dan Kompos Rumah Tangga Dapur & Ampas Kopi.

### 2. Pupuk Organik Cair (POC & Bioaktivator)
* ** Resep Dinamis & Smart Volume Scaler**: 10 Formula spesialis (ROTAN, Urine Kelinci, Asam Amino Ikan FAA, PSB Delima, Bio-Silika Bambu, Kalium-Kalsium Buah, Eco Enzyme, Jamur Jakaba, Empon-Empon Plus, dan Booster Sawit) dengan fitur pengali takaran otomatis proporsional (5L, 10L, 20L, 50L, 100L, 200L hingga kustom).
* ** Formulator Batch Drum Cerdas**: Kalkulator peracikan batch drum besar dengan proteksi ruang ekspansi gas (*headspace safety margin 15%*), estimasi NPK, protokol *degassing*, dan HPP per liter.
* ** Kalender Aplikasi & Jadwal Lapangan (HST)**: Manajemen penyemprotan presisi skala lahan (100 m² - 10 Hektar) atau tangki solo (16 L) terintegrasi fase vegetatif s/d panen untuk Padi, Cabai/Tomat, Bawang Merah, Sayuran Daun, Melon, Jagung, dan Kelapa Sawit.
* ** Bank MOL & Hormon ZPT Nabati**: 8 isolat biakan mandiri (Auksin, Sitokinin, Giberelin, Kalium, Bio-Proteksi).
* ** Dokter POC & Kompatibilitas Campuran Tangki**: Diagnostik kegagalan fermentasi (bau busuk, khamir putih, tong kembung, dll) beserta panduan ilmiah pencampuran tangki semprot (*tank-mix guide*).
* ** Uji Mutu Lab (Permentan No. 261/KPTS/SR.310/M/4/2019)**: Verifikasi C-Organik (min 10%), total NPK (2-6%), pH (4-9), dan bebas cemaran patogen *E. coli* & *Salmonella*.

---

## Fitur Pendukung: Analisis Finansial & HPP
* Menghitung Harga Pokok Produksi (HPP) per kg kompos atau per botol POC.
* Analisis CAPEX (mesin pencacah/rumah kompos), OPEX dinamis (bahan, starter, upah tenaga kerja, kemasan).
* Proyeksi Laba Bersih, Margin Keuntungan, dan Titik Impas (*Break-Even Point / BEP*).

---

## ️ Arsitektur Teknologi

* **Backend**: Python 3.12, FastAPI, Uvicorn, Pydantic, NumPy, SciPy (Optimization).
* **Frontend**: Single Page Application (SPA) responsive modern dengan Glassmorphism, Chart.js live visualizer, dan Plus Jakarta Sans typography.
* **Deployment Ready**: Render (`render.yaml`, `Procfile`), Docker (`Dockerfile`).

---

## Panduan Menjalankan Secara Lokal

### 1. Masuk ke Folder Proyek
```bash
cd "c:\Users\yandr\OneDrive\Desktop\agrisensa-pupuk-organik"
```

### 2. Buat & Aktifkan Virtual Environment (Opsional tapi Direkomendasikan)
```bash
py -m venv .venv
.\.venv\Scripts\activate
```

### 3. Install Dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan Server FastAPI
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Buka browser Anda di:
 **http://127.0.0.1:8000** 
(Dokumentasi Swagger API interaktif tersedia di: **http://127.0.0.1:8000/docs**)

---

## Panduan Deploy ke Render (Render.com)

Aplikasi ini sudah dilengkapi dengan konfigurasi otomatis Render:

1. **Upload ke GitHub**:
 ```bash
 git init
 git add .
 git commit -m "feat: AgriSensa BioFertilizer Studio launch"
 git branch -M main
 git remote add origin https://github.com/USERNAME/agrisensa-pupuk-organik.git
 git push -u origin main
 ```

2. **Buka Render Dashboard**:
 * Login ke [dashboard.render.com](https://dashboard.render.com).
 * Klik **"New +"** lalu pilih **"Web Service"**.
 * Hubungkan repositori GitHub Anda.

3. **Konfigurasi Web Service**:
 * **Name**: `agrisensa-pupuk-organik`
 * **Runtime**: `Python 3`
 * **Build Command**: `pip install -r requirements.txt`
 * **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
 *(Render akan otomatis mendeteksi konfigurasi dari file `render.yaml` atau `Procfile`)*.
 * Klik **"Deploy Web Service"**.

Dalam hitungan 2-3 menit, website pembuatan pupuk organik Anda sudah online dan dapat diakses dari mana saja!

---
© 2026 **AgriSensa BioFertilizer Studio**
