# Great Britain Bicycle Accidents Dashboard (1979-2018)

## Project Overview
An interactive dashboard analyzing bicycle accidents in Great Britain over four decades. Designed for policymakers, researchers, and safety analysis, combining modular data pipelines with modern visualizations.

## Key Features
- Streamlit dashboard with real-time filters  
- ETL and preprocessing pipeline for clean, optimized data  
- Rich visualizations: time trends, severity, demographics, conditions  
- Performance optimized with Parquet and caching  
- Deployment-ready for Streamlit Cloud or local use  

## Dataset
- **Accidents Dataset:** Location, conditions, severity  
- **Bikers Dataset:** Cyclist demographics and injuries  

**Data Quality:** Missing values handled, rare categories grouped, optimized types, duplicates managed.

| Column | Description | Data Type | Processing Notes |
|--------|-------------|-----------|------------------|
| `Accident_Index` | Unique accident identifier | String | Primary merge key |
| `Date` | Accident date | Date | Extracted year, month, day of week |
| `Time` | Accident time | Time | Optional hour extraction |
| `Number_of_Vehicles` | Vehicles involved | Integer | Risk analysis metric |
| `Number_of_Casualties` | Total casualties | Integer | Key performance indicator |
| `Speed_limit` | Road speed limit (mph) | Integer | Correlation with severity |
| `Road_conditions` | Road surface state | Categorical | Grouped rare categories |
| `Weather_conditions` | Weather at time of accident | Categorical | Grouped rare categories |
| `Light_conditions` | Lighting conditions | Categorical | Important for severity analysis |
| `Road_type` | Type of road | Categorical | Risk factor analysis |
| `Severity` | Accident severity level | Categorical | Slight/Serious/Fatal |
| `Gender` | Cyclist gender | Categorical | Demographic analysis |
| `Age_Grp` | Age group range | Categorical | Demographic analysis |

## Project Structure

```
Accidents_GB/
│
├── data/                      # Raw datasets (not tracked in git)
│   ├── Accidents.csv         # Main accidents dataset
│   └── Bikers.csv            # Cyclist-specific data
│
├── processed/                 # Generated processed data and visualizations
│   ├── bicycle_accidents.parquet  # Preprocessed dataset
│   ├── accidents_over_time.png     # Time series plot
│   ├── severity_distribution.png   # Severity distribution plot
│   └── accidents_by_gender_age.png # Demographics plot
│
├── src/                      # Source code modules
│   ├── __init__.py
│   ├── etl.py               # Data extraction, transformation, loading
│   ├── preprocessing.py      # Feature engineering and data cleaning
│   ├── eda.py               # Exploratory data analysis functions
│   ├── dashboard_utils.py    # Dashboard helper functions
│   └── utils.py             # General utilities
│
├── Tableau/                  # Tableau workbooks (optional)
│   └── GBAccidents.twb
│
├── app.py                   # Main Streamlit dashboard application
├── main.py                  # Data processing pipeline script
├── notebook.ipynb          # Jupyter notebook for exploration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Quick Start

### **Prerequisites**

- Python 3.8 or higher
  
### **Installation**

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Accidents_GB
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure data files are available:**
   - Place `Accidents.csv` and `Bikers.csv` in the `data/` folder
   - Or download from the original data source

### **Running the Application**

1. **Process the data (first time only):**
   ```bash
   python main.py
   ```
   This will:
   - Merge the datasets
   - Clean and preprocess the data
   - Generate the Parquet file
   - Create initial EDA plots

2. **Launch the dashboard:**
   ```bash
   streamlit run app.py
   ```

3. **Open your browser to:**
   ```
   http://localhost:8501
   ```

## Dashboard Features

- **KPIs:** Total accidents, casualties, vehicles, severity breakdown  
- **Time Trends:** Yearly, monthly, weekly patterns  
- **Severity Analysis:** Distribution and correlations with conditions  
- **Demographics:** Age and gender risk patterns  
- **Conditions:** Road, weather, light impact  
- **Data Explorer:** Interactive table and CSV export  

## Deployment

- **Streamlit Cloud:** Connect GitHub, select `app.py`  
- **Local:** `streamlit run app.py --server.headless true`  
- **Docker (Optional):** Dockerfile included for containerized deployment  

## Insights
Supports safety analysis, policy planning, and research applications with temporal, environmental, and demographic trends.

- **Data Source:** Great Britain Department for Transport  
- **Tools:** Streamlit, Plotly, Pandas, Python
---

**Built with ❤️ for safer cycling in Great Britain**
