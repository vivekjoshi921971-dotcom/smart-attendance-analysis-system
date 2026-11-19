# Smart Attendance Analysis System

A full-stack Python & Flask web application for analyzing attendance logs, identifying day-of-week absenteeism anomalies, computing predictive risk scores, and generating downloadable executive reports.

## Project Structure
```text
smart_attendance_analysis_system/
├── app.py                     # Flask web server & REST API endpoints
├── analytics.py               # Pandas analytics engine & predictive risk scorer
├── generate_sample_data.py    # Synthetic attendance dataset generator
├── requirements.txt           # Python dependencies
├── data/
│   └── attendance_logs.csv    # Pre-generated 60-day attendance dataset
├── prompts/
│   └── master_ai_prompt.md    # Structured AI engineering specification prompt
├── templates/
│   └── index.html             # Interactive Chart.js dashboard UI
└── static/
    └── style.css              # Responsive dashboard styling
```

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```
3. Open `http://127.0.0.1:5000` in your browser.

## CSV Upload Schema
To analyze your own dataset, upload a `.csv` file with the following columns:
`entity_id,name,department,date,status,check_in_time,check_out_time`
- **status** values: `Present`, `Absent`, `Late`, `Excused`
- **date** format: `YYYY-MM-DD`
