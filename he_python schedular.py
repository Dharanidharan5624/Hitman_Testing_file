from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import subprocess
import sys
import os
import mysql.connector
from win10toast import ToastNotifier
import psutil
import traceback

# === Toast Notification ===
toaster = ToastNotifier()

# === DB Config ===
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123',
    'database': 'hitman_edgev_1'
}

# === Script Folder (absolute path) ===
SCRIPT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')

# === Read CLI or PowerBuilder Arguments ===
if len(sys.argv) != 5:
    print("❌ Error: Expected 4 arguments")
    print("Usage: python scheduler.py <job_name> <start_time> <frequency> <schedule_type>")
    sys.exit(1)

job_name = sys.argv[1]
start_time = sys.argv[2]
schedule_frequency = sys.argv[3].lower()
schedule_type = sys.argv[4].title()

print(f"✅ Job Name: {job_name}")
print(f"✅ Start Time: {start_time}")
print(f"✅ Frequency: {schedule_frequency}")
print(f"✅ Schedule Type: {schedule_type}")
# === Prevent Duplicate Instances ===


# === Notification Helper ===
def show_notification(title, message):
    try:
        print(f"[NOTIFY] {title}: {message}")
        toaster.show_toast(title, message, duration=4)
    except Exception as e:
        print(f"[TOAST ERROR] {e}")

# === Get Next ID ===
def get_next_id(table, column):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"SELECT MAX({column}) FROM {table}")
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return (result or 0) + 1

# === Insert or Update Job Metadata ===
def insert_or_update_job(job_name, schedule_time, schedule_frequency, schedule_type):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT job_number FROM he_job_master WHERE job_name = %s", (job_name,))
    result = cursor.fetchone()

    if result:
        cursor.execute("""
            UPDATE he_job_master
            SET start_time = %s, schedule_frequency = %s, schedule_type = %s
            WHERE job_name = %s
        """, (schedule_time, schedule_frequency, schedule_type, job_name))
    else:
        job_id = get_next_id("he_job_master", "id")
        job_number = str(job_id)
        cursor.execute("""
            INSERT INTO he_job_master (
                id, job_number, job_name, start_time, schedule_frequency, schedule_type
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (job_id, job_number, job_name, schedule_time, schedule_frequency, schedule_type))

    conn.commit()
    cursor.close()
    conn.close()

# === Get Next Run Number ===
def get_next_run_number(job_number):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(job_run_number) FROM he_job_execution WHERE job_number = %s", (job_number,))
    result = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return (result or 0) + 1

# === Log to Job Logs Table ===
def log_job(job_number, run_number, description):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO he_job_logs (job_number, job_run_number, job_log_description)
        VALUES (%s, %s, %s)
    """, (job_number, run_number, description))
    conn.commit()
    cursor.close()
    conn.close()

# === Job Execution Logic ===
def run_scheduled_job(job_name):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT job_number FROM he_job_master WHERE job_name = %s", (job_name,))
    job_number_row = cursor.fetchone()
    if not job_number_row:
        print(f"[ERROR] Job '{job_name}' not found.")
        return

    job_number = job_number_row[0]
    job_run_number = get_next_run_number(job_number)
    start_time = datetime.now()

    try:
        cursor.execute("""
            INSERT INTO he_job_execution (job_number, job_run_number, execution_status, start_datetime, end_datetime)
            VALUES (%s, %s, %s, %s, NULL)
        """, (job_number, job_run_number, "RUNNING", start_time))
        conn.commit()

        log_job(job_number, job_run_number, f"{job_name} started at {start_time}")

        # === Run script ===
        script_path = os.path.join(SCRIPT_FOLDER, f"{job_name}.py")
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Script not found: {script_path}")

        subprocess.run(["python", script_path], check=True)

        end_time = datetime.now()

        # === SUCCESS Update ===
        cursor.execute("""
            UPDATE he_job_execution
            SET execution_status = %s, end_datetime = %s
            WHERE job_number = %s AND job_run_number = %s
        """, ("SUCCESS", end_time, job_number, job_run_number))

        cursor.execute("""
            UPDATE he_job_master
            SET end_time = %s
            WHERE job_number = %s
        """, (end_time, job_number))

        conn.commit()
        log_job(job_number, job_run_number, f"{job_name} completed successfully at {end_time}")
        show_notification("✅ Job Success", f"{job_name} finished at {end_time.strftime('%H:%M:%S')}")

    except subprocess.CalledProcessError as e:
        end_time = datetime.now()

        cursor.execute("""
            UPDATE he_job_execution
            SET execution_status = %s, end_datetime = %s
            WHERE job_number = %s AND job_run_number = %s
        """, ("FAILED", end_time, job_number, job_run_number))

        cursor.execute("""
            UPDATE he_job_master
            SET end_time = %s
            WHERE job_number = %s
        """, (end_time, job_number))

        conn.commit()
        log_job(job_number, job_run_number, f"{job_name} failed: {e}")
        show_notification("❌ Job Failed", f"{job_name} failed at {end_time.strftime('%H:%M:%S')}")

    except Exception as e:
        print("[UNEXPECTED ERROR]")
        traceback.print_exc()

    cursor.close()
    conn.close()

# === Schedule Setup ===
def schedule_job(job_name, schedule_time, schedule_frequency):
    time_obj = datetime.strptime(schedule_time, "%H:%M:%S")
    scheduler = BlockingScheduler()

    if schedule_frequency == 'daily':
        scheduler.add_job(lambda: run_scheduled_job(job_name), 'cron',
                          hour=time_obj.hour, minute=time_obj.minute, second=time_obj.second)
    elif schedule_frequency == 'weekly':
        scheduler.add_job(lambda: run_scheduled_job(job_name), 'cron',
                          day_of_week='mon', hour=time_obj.hour, minute=time_obj.minute, second=time_obj.second)
    elif schedule_frequency == 'monthly':
        scheduler.add_job(lambda: run_scheduled_job(job_name), 'cron',
                          day=1, hour=time_obj.hour, minute=time_obj.minute, second=time_obj.second)
    else:
        print("[ERROR] Invalid frequency")
        return

    show_notification("Scheduler Started", f"{job_name} will run {schedule_frequency} at {schedule_time}")
    print(f"[SCHEDULER] {job_name} scheduled {schedule_frequency} at {schedule_time}")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("[STOPPED] Scheduler stopped.")

# === Main Entry Point ===
def main():
    insert_or_update_job(job_name, start_time, schedule_frequency, schedule_type)
    schedule_job(job_name, start_time, schedule_frequency)

if __name__ == "__main__":
    main()
