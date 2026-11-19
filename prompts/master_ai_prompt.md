# Master AI Engineering Prompt: Smart Attendance Analysis System

## Role & Objective
Act as a Senior Full-Stack Software Engineer and Data Scientist. Build a complete, production-ready **Smart Attendance Analysis System** using Python, Flask, Pandas, Scikit-Learn, and Chart.js. The system must track attendance, analyze absenteeism patterns, detect at-risk individuals using anomaly detection/predictive heuristics, and generate automated executive reports.

## System Architecture & Requirements
1. **Backend Framework**: Python 3.10+ with Flask (`app.py`).
2. **Data Processing & Analytics Engine** (`analytics.py`):
   - Ingest attendance logs (`CSV` / `SQLite`) containing `entity_id`, `name`, `department`, `date`, `status` (`Present`, `Absent`, `Late`, `Excused`), `check_in_time`, and `check_out_time`.
   - Compute KPIs: Overall Attendance Rate (%), Punctuality Rate (%), Chronic Absenteeism Rate (< 80% threshold), Department-wise Breakdown, and Day-of-Week Absenteeism Trends.
   - **Smart Risk Scoring**: Implement a weighted risk index combining consecutive absences, overall attendance percentage, and late arrival frequency to flag `High Risk`, `Moderate Risk`, and `Low Risk` individuals.
3. **Interactive Web Dashboard** (`templates/index.html` + `static/style.css`):
   - Responsive KPI summary cards.
   - Interactive charts (Attendance Trend Line Chart, Department Comparison Bar Chart, Status Distribution Doughnut Chart).
   - Searchable & filterable At-Risk Student/Employee Table with actionable alert badges.
   - CSV upload endpoint for live dataset analysis and downloadable CSV report export.
4. **Database & Sample Data** (`generate_sample_data.py`):
   - Generate realistic synthetic attendance data across 60 days for 50 entities across 4 departments (`Engineering`, `Design`, `Operations`, `Marketing`) with injected chronic absenteeism and tardiness anomalies for testing.

## Code Quality & Execution Standards
- Modularize code cleanly (`app.py`, `analytics.py`, `generate_sample_data.py`).
- Include complete error handling for malformed CSV uploads.
- Provide `requirements.txt` and `README.md` with clear setup and execution instructions.
