import pandas as pd
import numpy as np

REQUIRED_COLUMNS = {"entity_id", "name", "department", "date", "status"}

class AttendanceAnalyzer:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self._validate_and_clean()

    def _validate_and_clean(self):
        missing = REQUIRED_COLUMNS - set(self.df.columns)
        if missing:
            raise ValueError(f"Missing required CSV columns: {', '.join(missing)}")
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df["status"] = self.df["status"].str.strip().str.title()
        self.df["day_of_week"] = self.df["date"].dt.day_name()
        self.df["is_present_or_late"] = self.df["status"].isin(["Present", "Late"]).astype(int)
        self.df["is_present"] = (self.df["status"] == "Present").astype(int)
        self.df["is_late"] = (self.df["status"] == "Late").astype(int)
        self.df["is_absent"] = (self.df["status"] == "Absent").astype(int)

    def _max_consecutive_absences(self, group):
        sorted_grp = group.sort_values("date")
        max_streak = 0
        current_streak = 0
        for status in sorted_grp["status"]:
            if status == "Absent":
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        return max_streak

    def compute_entity_metrics(self):
        records = []
        for (entity_id, name, dept), grp in self.df.groupby(["entity_id", "name", "department"]):
            total_days = len(grp)
            present_days = grp["is_present"].sum()
            late_days = grp["is_late"].sum()
            absent_days = grp["is_absent"].sum()
            excused_days = (grp["status"] == "Excused").sum()

            attendance_rate = round(((present_days + late_days) / total_days) * 100, 1) if total_days else 0.0
            punctuality_rate = round((present_days / (present_days + late_days)) * 100, 1) if (present_days + late_days) else 0.0
            max_consec_abs = self._max_consecutive_absences(grp)

            # Smart Risk Score (0 to 100, higher = higher risk)
            absence_penalty = max(0, (100 - attendance_rate) * 2.2)
            tardiness_penalty = (late_days / total_days) * 40 if total_days else 0
            streak_penalty = max_consec_abs * 8
            risk_score = min(100.0, round(absence_penalty + tardiness_penalty + streak_penalty, 1))

            if attendance_rate < 80.0 or max_consec_abs >= 3 or risk_score >= 55:
                risk_level = "High Risk"
            elif attendance_rate < 90.0 or (late_days / total_days) > 0.20 or risk_score >= 30:
                risk_level = "Moderate Risk"
            else:
                risk_level = "Low Risk"

            records.append({
                "entity_id": entity_id,
                "name": name,
                "department": dept,
                "total_days": int(total_days),
                "present_days": int(present_days),
                "late_days": int(late_days),
                "absent_days": int(absent_days),
                "excused_days": int(excused_days),
                "attendance_rate": attendance_rate,
                "punctuality_rate": punctuality_rate,
                "max_consecutive_absences": int(max_consec_abs),
                "risk_score": risk_score,
                "risk_level": risk_level
            })

        entity_df = pd.DataFrame(records).sort_values(by=["risk_score", "attendance_rate"], ascending=[False, True])
        return entity_df

    def get_dashboard_summary(self):
        entity_df = self.compute_entity_metrics()
        total_records = len(self.df)
        overall_attendance = round((self.df["is_present_or_late"].sum() / total_records) * 100, 1) if total_records else 0.0
        total_attended = self.df["is_present_or_late"].sum()
        overall_punctuality = round((self.df["is_present"].sum() / total_attended) * 100, 1) if total_attended else 0.0

        high_risk_count = int((entity_df["risk_level"] == "High Risk").sum())
        moderate_risk_count = int((entity_df["risk_level"] == "Moderate Risk").sum())

        # Status breakdown
        status_counts = self.df["status"].value_counts().to_dict()

        # Department stats
        dept_stats = (
            self.df.groupby("department")
            .agg(
                attendance_rate=("is_present_or_late", lambda x: round(x.mean() * 100, 1)),
                punctuality_rate=("is_present", lambda x: round(x.mean() * 100, 1)),
                absent_count=("is_absent", "sum")
            )
            .reset_index()
            .to_dict(orient="records")
        )

        # Daily trend (last 20 active dates)
        daily_trend = (
            self.df.groupby(self.df["date"].dt.strftime("%Y-%m-%d"))
            .agg(attendance_rate=("is_present_or_late", lambda x: round(x.mean() * 100, 1)))
            .reset_index()
            .tail(20)
            .to_dict(orient="records")
        )

        # Day of week absenteeism
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        dow_stats = (
            self.df.groupby("day_of_week")["is_absent"]
            .mean()
            .mul(100)
            .round(1)
            .reindex(days_order)
            .fillna(0)
            .to_dict()
        )

        return {
            "kpis": {
                "total_entities": int(len(entity_df)),
                "total_records": int(total_records),
                "overall_attendance": overall_attendance,
                "overall_punctuality": overall_punctuality,
                "high_risk_count": high_risk_count,
                "moderate_risk_count": moderate_risk_count
            },
            "status_counts": status_counts,
            "dept_stats": dept_stats,
            "daily_trend": daily_trend,
            "dow_absenteeism": dow_stats,
            "entities": entity_df.to_dict(orient="records")
        }
