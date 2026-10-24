# AgriSensa BioFertilizer Studio

**Platform Cerdas Formulasi & Optimasi Pupuk Organik (Padat & Cair)** 
*Ditenagai Backend Python (FastAPI), Heuristic/AI Optimizer, dan Validasi Standar SNI*

---

## Ringkasan Proyek

**AgriSensa BioFertilizer Studio** adalah web aplikasi independen khusus untuk formulasi, monitoring fermentasi, dan analisis ekonomi pupuk organik. Dikembangkan dengan memisahkan dan mematangkan konsep agroteknologi unggulan dari ekosistem `agrisensa-api`, platform ini dirancang dengan standar industri agar siap di-deploy langsung ke **Render**, **Railway**, atau **Docker Cloud Platform**.

---

## 2 Fitur Utama

### 1. Pupuk Organik Padat (Kompos & Bokashi)
* **Smart Formulator & Analisis C/N**: Mengkalkulasi akumulasi massa karbon (C), nitrogen (N), fosfor (P), kalium (K), dan rasio C/N awal dari 14+ database bahan limbah (Kotoran Sapi, Kambing, Ayam, Puyuh, Guano, Jerami, Sekam, Arang Sekam, Dedak, Dolomit, Abu Kayu, dll).
* **Simulasi Fase Fermentasi Dinamis**: Memproyeksikan kurva degradasi C/N dari awal (~28:1) menuju kematangan stabil (12-15:1) serta tahapan suhu (Mesofilik 25-45°C → Termofilik 55-65°C → Pendinginan → Pematangan).
* ** AI Recipe Optimizer**: Algoritma optimasi terikat (Constrained Optimization / SLSQP) yang membagi takaran proporsi bahan baku secara otomatis sesuai target bobot dan target C/N tanpa risiko kegagalan fermentasi.
* ** Validasi SNI 19-7030-2004**: Audit otomatis parameter mutu kompos (C/N, C-Organik, N-total, P2O5, K2O).
* ** Ensiklopedia Resep Bokashi Lapangan**: Panduan langkah demi langkah Bokashi ROTAN 1 Hektar, Bokashi Ayam Sayuran (N-Tinggi), Bokashi Guano Buah (P-Tinggi), dan Bokashi Sapi Pembenah Tanah.

### 2. Pupuk Organik Cair (POC & Bioaktivator)
* ** Koleksi Resep POC Premium**:
 * **POC ROTAN Super (Ramuan Organik Tanaman)**: Probiotik lengkap mikroba selulolitik & penambat N berbasis cairan rumen sapi, nanas, usus ikan, molase, dan dedak.
 * **Metode Perbanyakan Masal 1:100 Liter**: Trik efisiensi biaya memperbanyak 1 Liter biang POC menjadi 100 Liter POC berkualitas setara.
 * **POC Urine Kelinci (Liquid Gold)**: Formula Nitrogen tinggi untuk percepatan klorofil dan fase vegetatif.
 * **POC Empon-Empon Plus**: Formulasi 2-in-1 nutrisi dan bio-fungisida herbal (Jahe, Kunyit, Temulawak, Lengkuas) dengan teknik pasteurisasi media.
 * **Ramuan Spesial Kelapa Sawit**: Mengatasi dominasi bunga jantan (sex ratio balance) dan meningkatkan Berat Janjang Rata-rata (BJR) 30-50%.
* ** Kalkulator Dosis Tangki & Kocor Presisi**: Menghitung kebutuhan cc/ml POC per tangki semprot (14-16 Liter) atau ember kocor sesuai fase komoditas (Padi, Sayuran Daun, Buah, Sawit) dan jam buka stomata optimal.
* ** Bank MOL & Hormon ZPT Alami**: Panduan MOL Rebung (Giberelin), MOL Bonggol Pisang (Sitokinin), MOL Keong Mas (Asam Amino), dan MOL Sabut Kelapa (Kalium).
* ** Evaluasi Standar Mutu POC (Permentan No. 261/KPTS/SR.310/M/4/2019)**: Verifikasi C-Organik (min 10%), total NPK (2-6%), pH (4-9), dan bebas cemaran patogen Salmonella.

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
