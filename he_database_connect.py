# database_connect.py

import mysql.connector
import configparser

# Load config
config = configparser.ConfigParser()
config.read("D:\hitman edge\configure\config.ini")

if 'database' not in config:
    raise KeyError("Missing [database] section in config.ini")

# Database credentials from config
db_host = config['database']['HE_HOSTNAME']
db_port = config.getint('database', 'HE_PORT')
db_user = config['database']['HE_DB_USERNAME']
db_pass = config['database']['HE_DB_PASSWORD']

def get_connection(database=None, root=False):
    """Returns a MySQL connection. Use root=True to connect as root."""
    user = "root" if root else db_user
    password = "" if root else db_pass  # Modify if root password is used

    connection_config = {
        "host": db_host,
        "port": db_port,
        "user": user,
        "password": password,
    }

    if database:
        connection_config["database"] = database

    try:
        return mysql.connector.connect(**connection_config)
    except mysql.connector.Error as err:
        print(f"[ERROR] MySQL connection failed: {err}")
        return None

# C:\ 
#     └── hitman edge\
#         ├── configure\           
#         │   └── config.ini         
#         ├── database\            
#         │   ├── schema.sql
#         │   ├── data.sql
#         │   └── ... (other .sql files)
#         ├── Powerbuilder\        
#         │   └── app.pbl          
#         └── script\                
#             ├── He_Portfolio.py
#             ├── database_connect.py
#             └── ... (other .py files)



# D:\ 
#     └── hitman edge\
#         ├── configure\           
#         │   └── config.ini                   
#         └── script\                
#             ├── database_connect.py 
#             ├── He_Portfolio.py
#             └──  (other He__.py files)