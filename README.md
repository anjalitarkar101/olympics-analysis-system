# 🏅 Olympics Analysis System

## 📖 Overview
An interactive Olympics Analysis System built with Streamlit that provides comprehensive insights into Olympic Games data from 1896 to 2016. The system allows users to explore medal tallies, country performances, athlete statistics, and historical trends across both Summer and Winter Olympics.


---

## ✨ Features
- 🏅 Medal Tally - View medal counts by country and year with interactive filters
- 📊 Overall Analysis - Comprehensive statistics with visual trends over time
- 🌍 Country-wise Analysis - Deep dive into specific country performances
- 👤 Athlete-wise Analysis - Demographic insights and performance metrics
- ☀️❄️ Season Toggle - Switch between Summer and Winter Olympics
- 🎯 Interactive Visualizations - Plotly charts, heatmaps, and distribution plots


---

## 🛠️ Technologies Used
- Python 3.10+ - Core programming language
- Streamlit - Web application framework
- Pandas - Data manipulation and analysis
- NumPy - Numerical operations
- Plotly - Interactive visualizations
- Matplotlib/Seaborn - Static visualizations and heatmaps
- Scipy - Statistical computations


---

## 📁 Project Structure
```
olympics-analysis-system/
├── app.py                    # Main Streamlit application (UI)
├── helper_functions.py       # Analysis and helper functions
├── preprocessor.py           # Data preprocessing script
├── requirements.txt          # Python dependencies
├── setup.sh           tem        # Setup script
├── .gitignore               # Git ignore file
├── data/                     # CSV files (gitignored)
│   ├── athlete_events.csv
│   └── noc_regions.csv
├── images/                   # Static images
│   └── logo.png
├── saved_visualizations/     # Generated plots (gitignored)
│   ├── events_heatmap_Summer.png
│   ├── events_heatmap_Winter.png
│   └── ...
└── README.md                 # Project documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/anjalitarkar101/olympics-analysis-system.git
cd olympics-analysis
```

### Step 2: Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create required directories (data/, images/, saved_visualizations/)
- Install all dependencies

### Step 3: Download Dataset
- **Source:** Kaggle
- **Link:** https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
- **Name:** 120 Years of Olympic History: Athletes and Results
- **Files:** athlete_events.csv, noc_regions.csv
- **Rows:** 271,116 rows (athlete_events.csv) + 230 rows (noc_regions.csv)
- **Columns:** 15 (athlete_events.csv) + 5 (noc_regions.csv)

After downloading, place the files in the `data/` folder:
```
data/
├── athlete_events.csv
└── noc_regions.csv
```

### Step 4: Add Logo (Optional)
Place your Olympic rings logo in the images/ folder as logo.png

### Step 5: Run the Application
```bash
streamlit run app.py
Open your browser and navigate to http://localhost:8501
```


---
## 📊 How It Works
1. Data Preprocessing
- Merges athlete data with country codes
- Removes duplicate entries
- One-hot encodes medal columns
- Handles missing values

2. Medal Tally
- Filters by year and country
- Calculates Gold, Silver, Bronze, and Total medals
- Ranks countries by medal count

3. Overall Analysis
- Displays key statistics (Editions, Cities, Sports, etc.)
- Shows trends over time (Participating Nations, Events, Athletes)
- Heatmap of events by sport and year
- Lists most successful athletes

4. Country-wise Analysis
- Year-wise medal performance
- Sport-wise performance heatmap
- Top athletes from the country

5. Athlete-wise Analysis
- Age distribution by medal category
- Age distribution by sport (Gold medalists)
- Height vs Weight analysis
- Gender participation trends


---

## 🔧 Dependencies
```txt
streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
matplotlib==3.7.2
seaborn==0.12.2
scipy==1.10.1
```

---

## 📝 Usage Guide
1. Select Season - Choose Summer or Winter Olympics from the sidebar
2. Navigate - Use the radio buttons to switch between analysis views
3. Medal Tally - Filter by year and country to view medal counts
4. Overall Analysis - Explore statistics and trends with interactive charts
5. Country-wise Analysis - Select a country to see detailed performance
6. Athlete-wise Analysis - Explore athlete demographics and statistics


---

## 📊 Dataset Information

### athlete_events.csv Columns

| Column | Type | Description |
|--------|------|-------------|
| ID | Numerical | Unique identifier for each athlete |
| Name | Text | Athlete's full name |
| Sex | Categorical | Male or Female |
| Age | Numerical | Athlete's age at the time of the event |
| Height | Numerical | Athlete's height in cm |
| Weight | Numerical | Athlete's weight in kg |
| Team | Text | Team/Country name |
| NOC | Categorical | National Olympic Committee 3-letter code |
| Games | Text | Year and season of the games |
| Year | Numerical | Year of the Olympics |
| Season | Categorical | Summer or Winter |
| City | Text | Host city of the Olympics |
| Sport | Text | Sport category |
| Event | Text | Specific event name |
| Medal | Categorical | Gold, Silver, Bronze, or NA |

### noc_regions.csv Columns

| Column | Type | Description |
|--------|------|-------------|
| NOC | Categorical | National Olympic Committee 3-letter code |
| Region | Text | Country/Region name |
| Notes | Text | Additional notes about the region |

---

## 📄 License

This project is licensed under the MIT License.

© 2026 Anjali Tarkar. All rights reserved.


---

## 👩‍💻 Author
**Anjali Tarkar**
- GitHub: https://github.com/anjalitarkar101
- Email: anjalitarkar101@gmail.com


---

## ⭐ Show Your Support
If you find this project useful, please give it a star on GitHub!


---

## 🙏 Acknowledgments
- rgriffin  - For the 120 Years of Olympic History : Athletes and Results Dataset on Kaggle
- Streamlit - For the awesome web framework
- Plotly - For interactive visualizations


