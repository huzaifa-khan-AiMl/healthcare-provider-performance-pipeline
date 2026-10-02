# Healthcare Provider Performance & Outlier Analysis Pipeline

This is an end-to-end ELT data pipeline designed to analyze CMS Medicare Part B provider billing patterns, utilization rates, and statistical payment anomalies using PostgreSQL, dbt, and Docker.

---

## Architecture & Data Flow (In Progress)
- **Phase 1: Environment & Repository Setup** (Completed)
- **Phase 2: Data Acquisition (ELT - Extract)** (Completed)
- **Phase 3: Source Data Profiling & Quality Validation** (Active)
- **Phase 4: Warehouse Ingestion (PostgreSQL)** (Upcoming)
- **Phase 5: Analytical Modeling (dbt)** (Upcoming)

---

## Getting Started

### 1. Prerequisites
- A Linux, WSL2, or Windows environment
- Python version 3.10 or higher
- An active internet connection with outbound access to `*.cms.gov`. Depending on your region, you may need to route terminal traffic through a VPN to access CMS endpoints.

### 2. Environment Setup
Clone the repository and set up the virtual environment:

```bash
# Clone the repository
git clone https://github.com/<your-username>/healthcare-provider-performance-pipeline.git
cd healthcare-provider-performance-pipeline

# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
# On Linux / WSL2:
source .venv/bin/activate

# On Windows PowerShell:
# .venv\Scripts\Activate.ps1

# On Windows CMD:
# .venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

## 3. Data Acquisition / Extraction

### On Linux / WSL2:
python3 src/ingestion/extract_cms.py --year 2022

### On Windows:
python src\ingestion\extract_cms.py --year 2022
