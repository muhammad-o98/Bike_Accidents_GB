# 🚴‍♂️ Great Britain Bicycle Accidents Analysis Dashboard (1979-2018)

## 📋 Project Overview

This project provides an **industry-grade interactive dashboard** for analyzing bicycle accidents in Great Britain spanning nearly four decades (1979-2018). The solution combines data engineering best practices with modern visualization techniques to deliver actionable insights for safety analysis, policy making, and research.

### 🎯 Key Features

- **Interactive Streamlit Dashboard** with real-time filtering and exploration
- **Comprehensive Data Processing Pipeline** with ETL, preprocessing, and analysis
- **Industry-Standard Architecture** with modular, maintainable code
- **Performance Optimized** using Parquet format for fast data loading
- **Rich Visualizations** including time series, demographic analysis, and severity patterns
- **Deployment Ready** for Streamlit Cloud, Heroku, or AWS

## 🗂️ Dataset Description

### **Data Sources**
- **Accidents Dataset:** Contains accident-level information (location, conditions, severity)
- **Bikers Dataset:** Contains cyclist-specific information (demographics, injuries)

### **Key Features**

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

### **Data Quality Considerations**

- **Missing Values:** Handled through imputation and categorization
- **Rare Categories:** Low-frequency values grouped as "Other" for cleaner analysis
- **Data Types:** Optimized using categorical types for memory efficiency
- **Duplicates:** Handled appropriately for accident vs. casualty level analysis

## 🏗️ Project Structure

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

## 🚀 Quick Start

### **Prerequisites**

- Python 3.8 or higher
- Git (for cloning)

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

## 🎮 Dashboard Features

### **📊 Interactive Filters**

**Sidebar Controls:**
- **Year Range:** Slider to select time period
- **Severity:** Multi-select for accident severity levels
- **Demographics:** Gender and age group filters
- **Conditions:** Road, weather, and lighting condition filters

### **📈 Visualization Sections**

#### **1. Overview KPIs**
- Total accidents, casualties, vehicles involved
- Average casualties per accident
- Breakdown by severity level
- Year range summary

#### **2. Time Trends Tab**
- **Yearly Time Series:** Accidents over time with trend analysis
- **Day of Week Patterns:** Identify high-risk days
- **Monthly Seasonality:** Seasonal accident patterns

#### **3. Severity Analysis Tab**
- **Severity Distribution:** Pie chart of accident severities
- **Severity by Weather:** Stacked bar chart showing severity patterns by weather conditions
- **Risk Factor Analysis:** Correlation between conditions and severity

#### **4. Demographics Tab**
- **Gender Distribution:** Accident rates by gender
- **Age Group Analysis:** Risk patterns across age groups
- **Demographic Insights:** Interactive exploration of victim characteristics

#### **5. Conditions Analysis Tab**
- **Road Conditions:** Impact of road surface on accidents
- **Light Conditions:** Daylight vs. darkness accident patterns
- **Environmental Factors:** Weather and road condition interactions

#### **6. Data Explorer Tab**
- **Raw Data Viewer:** Paginated table with column selection
- **Dataset Summary:** Key statistics and data quality metrics
- **Data Export:** Download filtered datasets as CSV

### **🎨 User Experience Features**

- **Responsive Design:** Works on desktop and tablet
- **Real-time Filtering:** Instant updates based on filter selections
- **Professional Styling:** Clean, modern interface
- **Performance Optimized:** Fast loading with cached data
- **Accessible:** Clear labeling and intuitive navigation

## 🔧 Technical Implementation

### **Data Processing Pipeline**

1. **ETL (`etl.py`):**
   - Loads raw CSV files
   - Performs inner join on `Accident_Index`
   - Basic data validation

2. **Preprocessing (`preprocessing.py`):**
   - Standardizes column names
   - Converts data types
   - Extracts temporal features
   - Creates severity encoding
   - Saves optimized Parquet format

3. **EDA (`eda.py`):**
   - Generates static visualization plots
   - Creates publication-ready figures
   - Saves plots for quick reference

4. **Dashboard Utils (`dashboard_utils.py`):**
   - Filtering and aggregation functions
   - Data preparation for visualizations
   - KPI calculation utilities
   - Category grouping for rare values

### **Performance Optimizations**

- **Parquet Format:** 10x faster loading than CSV
- **Categorical Data Types:** Reduced memory usage
- **Streamlit Caching:** Cached data loading and computations
- **Efficient Filtering:** Optimized pandas operations
- **Grouped Categories:** Reduced complexity for rare values

### **Code Quality Standards**

- **Modular Architecture:** Separation of concerns
- **Type Hints:** Enhanced code readability and IDE support
- **Documentation:** Comprehensive docstrings
- **Error Handling:** Graceful failure management
- **Scalable Design:** Easy to extend and modify

## 🚀 Deployment

### **Streamlit Cloud (Recommended)**

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial dashboard implementation"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select branch and main file (`app.py`)
   - Deploy automatically

### **Local Production**

```bash
# Run with production settings
streamlit run app.py --server.port 8501 --server.headless true
```

### **Docker (Optional)**

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.headless", "true"]
```

## Insights & Value

### **Safety Analysis**
- **Risk Identification:** High-risk conditions and demographics
- **Temporal Patterns:** Peak accident times and seasonal trends
- **Severity Factors:** Conditions leading to more severe accidents

### **Policy Making**
- **Infrastructure Planning:** Road improvement priorities
- **Safety Campaigns:** Target demographics and conditions
- **Resource Allocation:** Emergency response planning

### **Research Applications**
- **Trend Analysis:** Long-term safety improvements
- **Correlation Studies:** Factor relationships
- **Comparative Analysis:** Regional or temporal comparisons

## 🔄 Data Updates

### **Adding New Data**
1. Place new CSV files in `data/` folder
2. Run `python main.py` to reprocess
3. Dashboard automatically uses updated data


### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements.txt

# Run code formatting
black src/ app.py main.py

# Run linting
flake8 src/ app.py main.py

- **Documentation:** See inline code documentation
- **Contact:** [Your contact information]

## Acknowledgments
- **Data Source:** Great Britain Department for Transport
- **Tools:** Streamlit, Plotly, Pandas, Python ecosystem

---

**Built with ❤️ for safer cycling in Great Britain**