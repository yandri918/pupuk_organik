import os

class Settings:
    PROJECT_NAME: str = "AgriSensa BioFertilizer Studio"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "Platform Pembuatan & Optimasi Pupuk Organik (Padat & Cair) Berbasis Python & AI"
    PORT: int = int(os.environ.get("PORT", 8000))
    HOST: str = "0.0.0.0"

settings = Settings()
