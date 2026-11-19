import os
import random
import pandas as pd
from datetime import datetime, timedelta

def generate_dataset(output_path="data/attendance_logs.csv", num_entities=50, num_days=60):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    random.seed(42)

    departments = ["Engineering", "Product & Design", "Operations", "Marketing"]
    first_names = ["Aarav", "Priya", "Rohan", "Ananya", "Vikram", "Neha", "Kabir", "Meera", "Arjun", "Diya",
                   "Siddharth", "Kavya", "Aditya", "Riya", "Dev", "Sneha", "Karan", "Pooja", "Nikhil", "Tara"]
    last_names = ["Sharma", "Verma", "Patel", "Gupta", "Singh", "Kumar", "Nair", "Reddy", "Joshi", "Mehta"]

    entities = []
    for i in range(1, num_entities + 1):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        dept = random.choice(departments)
        # Assign behavioral archetypes: regular (75%), chronically_late (15%), high_absenteeism (10%)
        rand_val = random.random()
        if rand_val < 0.75:
            archetype = "regular"
        elif rand_val < 0.90:
            archetype = "late_prone"
        else:
            archetype = "at_risk"
        entities.append({"id": f"ID-{1000 + i}", "name": name, "department": dept, "archetype": archetype})

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=num_days)

    records = []
    current_date = start_date
    while current_date <= end_date:
        # Skip weekends
        if current_date.weekday() < 5:
            is_monday_or_friday = current_date.weekday() in [0, 4]
            for ent in entities:
                arch = ent["archetype"]
                r = random.random()

                if arch == "regular":
                    absent_prob = 0.04 if is_monday_or_friday else 0.02
                    late_prob = 0.06
                elif arch == "late_prone":
                    absent_prob = 0.06
                    late_prob = 0.35
                else:  # at_risk
                    absent_prob = 0.28 if is_monday_or_friday else 0.20
                    late_prob = 0.20

                if r < absent_prob:
                    status = "Absent"
                    check_in = ""
                    check_out = ""
                elif r < absent_prob + 0.02:
                    status = "Excused"
                    check_in = ""
                    check_out = ""
                elif r < absent_prob + 0.02 + late_prob:
                    status = "Late"
                    late_mins = random.randint(16, 75)
                    in_dt = datetime.combine(current_date, datetime.strptime("09:00", "%H:%M").time()) + timedelta(minutes=late_mins)
                    out_dt = in_dt + timedelta(hours=8, minutes=random.randint(0, 30))
                    check_in = in_dt.strftime("%H:%M")
                    check_out = out_dt.strftime("%H:%M")
                else:
                    status = "Present"
                    early_or_on_time = random.randint(-15, 10)
                    in_dt = datetime.combine(current_date, datetime.strptime("09:00", "%H:%M").time()) + timedelta(minutes=early_or_on_time)
                    out_dt = in_dt + timedelta(hours=8, minutes=random.randint(15, 45))
                    check_in = in_dt.strftime("%H:%M")
                    check_out = out_dt.strftime("%H:%M")

                records.append({
                    "entity_id": ent["id"],
                    "name": ent["name"],
                    "department": ent["department"],
                    "date": current_date.strftime("%Y-%m-%d"),
                    "status": status,
                    "check_in_time": check_in,
                    "check_out_time": check_out
                })
        current_date += timedelta(days=1)

    df = pd.DataFrame(records)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} attendance records at {output_path}")

if __name__ == "__main__":
    generate_dataset()
