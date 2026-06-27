import os
import csv
from datetime import datetime

class AttendanceLogger:
    """
    Manages daily CSV log files (YYYY-MM-DD.csv) directly in project root.
    """
    def __init__(self, logs_dir=".", cutoff_time="09:00:00"):
        self.logs_dir = logs_dir
        try:
            self.cutoff_time = datetime.strptime(cutoff_time, "%H:%M:%S").time()
        except ValueError:
            self.cutoff_time = datetime.strptime("09:00:00", "%H:%M:%S").time()

        self.marked_students = {}  # name -> {"time": time_str, "status": status}
        self.current_file_path = None
        self._init_daily_file()

    def _init_daily_file(self):
        date_str = datetime.now().strftime("%Y-%m-%d")
        self.current_file_path = os.path.join(self.logs_dir, f"{date_str}.csv")
        file_exists = os.path.exists(self.current_file_path)
        
        if file_exists:
            with open(self.current_file_path, "r", newline="") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if len(row) >= 1:
                        name = row[0].strip()
                        t_str = row[1].strip() if len(row) > 1 else ""
                        status = row[3].strip() if len(row) > 3 else "Present"
                        self.marked_students[name] = {"time": t_str, "status": status}
        else:
            with open(self.current_file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Timestamp", "Date", "Status"])

    def mark_attendance(self, student_name):
        student_name = student_name.strip()
        if student_name in self.marked_students:
            return False

        now = datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%Y-%m-%d")
        status = "Late" if now.time() > self.cutoff_time else "On Time"

        with open(self.current_file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([student_name, time_str, date_str, status])

        self.marked_students[student_name] = {"time": time_str, "status": status}
        print(f"[LOGGED] {student_name} marked as '{status}' at {time_str}")
        return True

    def get_today_records(self):
        records = []
        date_str = datetime.now().strftime("%Y-%m-%d")
        for name, details in self.marked_students.items():
            records.append({
                "name": name,
                "time": details["time"],
                "date": date_str,
                "status": details["status"]
            })
        return records

    def get_today_summary(self, total_registered_names=None):
        total_present = len(self.marked_students)
        on_time_count = sum(1 for d in self.marked_students.values() if d["status"] == "On Time")
        late_count = sum(1 for d in self.marked_students.values() if d["status"] == "Late")
        
        absent_students = []
        total_registered = total_present
        if total_registered_names:
            total_registered = len(total_registered_names)
            absent_students = [name for name in total_registered_names if name not in self.marked_students]

        return {
            "total_registered": total_registered,
            "present_count": total_present,
            "on_time_count": on_time_count,
            "late_count": late_count,
            "absent_count": len(absent_students),
            "absent_students": absent_students
        }
