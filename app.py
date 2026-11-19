import os
import io
from flask import Flask, render_template, request, jsonify, send_file
from analytics import AttendanceAnalyzer
from generate_sample_data import generate_dataset

app = Flask(__name__)
DATA_FILE = os.path.join("data", "attendance_logs.csv")

if not os.path.exists(DATA_FILE):
    generate_dataset(output_path=DATA_FILE)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/analytics", methods=["GET"])
def get_analytics():
    try:
        analyzer = AttendanceAnalyzer(DATA_FILE)
        return jsonify({"status": "success", "data": analyzer.get_dashboard_summary()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/api/upload", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"status": "error", "message": "No file part in request"}), 400
    file = request.files["file"]
    if file.filename == "" or not file.filename.endswith(".csv"):
        return jsonify({"status": "error", "message": "Please upload a valid .csv file"}), 400

    try:
        temp_path = os.path.join("data", "uploaded_temp.csv")
        file.save(temp_path)
        analyzer = AttendanceAnalyzer(temp_path)
        os.replace(temp_path, DATA_FILE)
        return jsonify({"status": "success", "message": "Dataset updated successfully", "data": analyzer.get_dashboard_summary()})
    except Exception as e:
        if os.path.exists(os.path.join("data", "uploaded_temp.csv")):
            os.remove(os.path.join("data", "uploaded_temp.csv"))
        return jsonify({"status": "error", "message": f"Invalid dataset format: {str(e)}"}), 400

@app.route("/api/reset-sample", methods=["POST"])
def reset_sample():
    generate_dataset(output_path=DATA_FILE)
    analyzer = AttendanceAnalyzer(DATA_FILE)
    return jsonify({"status": "success", "data": analyzer.get_dashboard_summary()})

@app.route("/api/export-report", methods=["GET"])
def export_report():
    analyzer = AttendanceAnalyzer(DATA_FILE)
    entity_df = analyzer.compute_entity_metrics()
    buf = io.BytesIO()
    entity_df.to_csv(buf, index=False)
    buf.seek(0)
    return send_file(
        buf,
        mimetype="text/csv",
        as_attachment=True,
        download_name="smart_attendance_risk_report.csv"
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
