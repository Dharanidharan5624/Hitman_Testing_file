import os
import sys
import subprocess
import ctypes
import time
import socket
import urllib.request
import configparser
import zipfile
import shutil
import mysql.connector
from mysql.connector import errorcode
import winreg

# Configurationz
config = configparser.ConfigParser()
config.read("C:\\hitman edge\\configure\\config.ini")

if 'database' not in config or 'paths' not in config:
    raise KeyError("Missing [database] or [paths] section in config.ini")

# Database Informationz
db_host = config['database']['HE_HOSTNAME']
db_port = config.getint('database', 'HE_PORT')
db_user = config['database']['HE_DB_USERNAME']
db_pass = config['database']['HE_DB_PASSWORD']
db_names = [
    config['database']['HE_DB_DEV'],
    config['database']['HE_DB_TEST'],
    config['database']['HE_DB_PROD'],
]
dsn_name = config['database']['HE_ODBC_NAME']

# Our File_Pathz
base_folder = config['paths']['HE_ROOT_PATH'].replace("\\", "/")
python_folder = config['paths']['HE_PYTHON_PATH'].replace("HE_Root_Path", base_folder).replace("\\", "/")
pb_folder = config['paths']['HE_POWERBUILDER_Exe'].replace("HE_Root_Path", base_folder).replace("\\", "/")
db_folder = config['paths']['HE_DATABSE'].replace("HE_Root_Path", base_folder).replace("\\", "/")
repo_url = config['paths']['HE_REPO_URL']


os.makedirs(python_folder, exist_ok=True)
os.makedirs(pb_folder, exist_ok=True)
os.makedirs(db_folder, exist_ok=True)

# XAMPP Installation Paths & Urls
xampp_path = "C:\\xampp"
installer_file = "xampp_installer.exe"
xampp_installer_url = (
    "https://downloads.sourceforge.net/project/xampp/XAMPP%20Windows/8.2.12/"
    "xampp-windows-x64-8.2.12-0-VS16-installer.exe"
)

# Admin Check
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    params = ' '.join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit()

# XAMPP Setup
def is_xampp_installed():
    return os.path.exists(os.path.join(xampp_path, "apache", "bin", "httpd.exe"))

def download_xampp_installer():
    print(" Downloading XAMPP installer...")
    if not os.path.exists(installer_file):
        urllib.request.urlretrieve(xampp_installer_url, installer_file)
        print(" XAMPP installer downloaded.")

def install_xampp():
    print(" Installing XAMPP...")
    subprocess.run([installer_file, "--mode", "unattended"], check=True)
    time.sleep(30)
    if not is_xampp_installed():
        print(" XAMPP installation failed.")
        sys.exit(1)
    print(" XAMPP installed successfully.")

# MySQL Services
def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((db_host, port)) == 0

def start_services():
    print(" Starting Apache and MySQL...")
    apache_exe = os.path.join(xampp_path, "apache", "bin", "httpd.exe")
    mysql_exe = os.path.join(xampp_path, "mysql", "bin", "mysqld.exe")
    mysql_ini = os.path.join(xampp_path, "mysql", "bin", "my.ini")

    if not is_port_open(80):
        subprocess.Popen([apache_exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(" Apache started.")
    else:
        print(" Apache already running.")

    if not is_port_open(db_port):
        subprocess.Popen([mysql_exe, f"--defaults-file={mysql_ini}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(" MySQL started.")
    else:
        print(" MySQL already running.")

    for _ in range(10):
        if is_port_open(db_port):
            return
        time.sleep(2)
    print(" MySQL failed to start.")
    sys.exit(1)

# MySQL User + DBs
def create_user_and_dbs():
    print(" Creating user and databases...")
    try:
        conn = mysql.connector.connect(host=db_host, user="root", password="")
        cursor = conn.cursor()

        try:
            cursor.execute(f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_pass}';")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_CANNOT_USER:
                print(" User already exists.")
            else:
                raise

        cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO '{db_user}'@'localhost';")
        cursor.execute("FLUSH PRIVILEGES;")

        for db in db_names:
            cursor.execute(f"DROP DATABASE IF EXISTS {db};")
            cursor.execute(f"CREATE DATABASE {db};")
            print(f" Database '{db}' created.")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f" MySQL Error: {err}")
        sys.exit(1)

# GitHub Repo Downloadz
def download_and_extract_repo():
    print("🔽 Downloading repository...")
    zip_url = repo_url.rstrip("/") + "/archive/refs/heads/main.zip"
    zip_path = os.path.join(base_folder, "repo.zip")
    extract_path = os.path.join(base_folder, "temp_repo")

    # Download the ZIP
    urllib.request.urlretrieve(zip_url, zip_path)

    # Extract ZIP
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    subfolder = os.listdir(extract_path)[0]
    extracted_folder = os.path.join(extract_path, subfolder)

    # Ensure destination folders exist
    os.makedirs(python_folder, exist_ok=True)
    os.makedirs(pb_folder, exist_ok=True)
    os.makedirs(db_folder, exist_ok=True)

    sql_file = None

    for root, _, files in os.walk(extracted_folder):
        for file in files:
            full_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            # Destination path
            if ext == ".py":
                dest_path = os.path.join(python_folder, os.path.relpath(full_path, extracted_folder))
            elif ext in [".pbt", ".pbl", ".sru", ".srw", ".srf", ".srp"]:
                dest_path = os.path.join(pb_folder, os.path.relpath(full_path, extracted_folder))
            elif ext == ".sql":
                dest_path = os.path.join(db_folder, os.path.relpath(full_path, extracted_folder))
                sql_file = dest_path
            elif ext == ".ini":
                dest_path = os.path.join(base_folder, os.path.basename(full_path))
            else:
                continue

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(full_path, dest_path)

    os.remove(zip_path)
    shutil.rmtree(extract_path)

    return sql_file


# SQL Importz
def import_sql_to_databases(sql_file_path):
    print(" Importing SQL to databases...")
    for db in db_names:
        cmd = [os.path.join(xampp_path, "mysql", "bin", "mysql.exe"), "-u", "root", db]
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            subprocess.run(cmd, stdin=f, check=True)
        print(f" SQL imported into '{db}'.")

#  MySQL DSN Setup
def create_or_update_dsn():
    print(" Creating ODBC DSNs...")
    driver = "MySQL ODBC 8.0 Unicode Driver"
    for db in db_names:
        try:
            dsn_key = f"Software\\ODBC\\ODBC.INI\\{db}"
            key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, dsn_key)
            winreg.SetValueEx(key, "Database", 0, winreg.REG_SZ, db)
            winreg.SetValueEx(key, "Driver", 0, winreg.REG_SZ, driver)
            winreg.SetValueEx(key, "Server", 0, winreg.REG_SZ, db_host)
            winreg.SetValueEx(key, "Port", 0, winreg.REG_SZ, str(db_port))
            winreg.SetValueEx(key, "UID", 0, winreg.REG_SZ, db_user)
            winreg.SetValueEx(key, "PWD", 0, winreg.REG_SZ, db_pass)
            winreg.CloseKey(key)

            odbc_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, "Software\\ODBC\\ODBC.INI\\ODBC Data Sources")
            winreg.SetValueEx(odbc_key, db, 0, winreg.REG_SZ, driver)
            winreg.CloseKey(odbc_key)

            print(f" DSN '{db}' created.")
        except Exception as e:
            print(f" Failed to create DSN '{db}': {e}")

# Main Setup
def main():
    print(" Starting Hitman Edge Full Setup...")

    if not is_admin():
        run_as_admin()

    if not is_xampp_installed():
        download_xampp_installer()
        install_xampp()
    else:
        print(" XAMPP already installed.")

    start_services()
    create_user_and_dbs()

    sql_file = download_and_extract_repo()
    if sql_file:
        import_sql_to_databases(sql_file)

    create_or_update_dsn()

    print("\n All setup steps completed successfully.")

if __name__ == "__main__":
    main()