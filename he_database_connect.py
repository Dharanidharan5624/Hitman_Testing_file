import os
import sys
import traceback
import configparser
import mysql.connector
from mysql.connector import Error as MySQLError

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Attempt to import custom error logger
try:
    from he_error_logs import log_error_to_db
except ImportError:
    def log_error_to_db(file_name: str, error_description: str, created_by: str = "system", env: str = "dev"):
        print(f"[ERROR LOGGER FAILED] {error_description}")

# Global config cache
_config = None

def load_config() -> configparser.ConfigParser:
    """
    Load and return configuration from config.ini file.
    Caches the config to avoid repeated reads.
    """
    global _config
    if _config:
        return _config

    config_path = os.path.join(r"C:\Hitman Edge", "config.ini")

    if not os.path.exists(config_path):
        msg = f"Config file not found: {config_path}"
        print(f"[ERROR] {msg}")
        log_error_to_db("he_database_connect.py", msg)
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(config_path)

    if 'database' not in config:
        msg = "Missing [database] section in config.ini"
        print(f"[ERROR] {msg}")
        log_error_to_db("he_database_connect.py", msg)
        sys.exit(1)

    _config = config
    return config

def get_connection(env: str = 'dev') -> mysql.connector.connection.MySQLConnection:
    """
    Establish and return a MySQL database connection based on the given environment.

    :param env: The environment key ('dev', 'test', 'prod')
    :return: MySQLConnection object
    """
    config = load_config()
    db = config['database']

    env_mapping = {
        'dev': 'HE_DB_DEV',
        'test': 'HE_DB_TEST',
        'prod': 'HE_DB_PROD'
    }

    if env not in env_mapping or env_mapping[env] not in db:
        msg = f"Invalid or missing environment key in config: {env}"
        print(f"[ERROR] {msg}")
        log_error_to_db("he_database_connect.py", msg, env=env)
        sys.exit(1)

    try:
        conn = mysql.connector.connect(
            host=db.get('HE_HOSTNAME'),
            port=int(db.get('HE_PORT', 3306)),
            user=db.get('HE_DB_USERNAME'),
            password=db.get('HE_DB_PASSWORD'),
            database=db.get(env_mapping[env])
        )
        print(f"[INFO] Successfully connected to {env} database.")
        return conn

    except MySQLError as err:
        error_details = traceback.format_exc()
        print(f"[ERROR] Database connection failed: {err}")
        log_error_to_db("he_database_connect.py", error_details, created_by="DB_CONNECT", env=env)
        sys.exit(1)
