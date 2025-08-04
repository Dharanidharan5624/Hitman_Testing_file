from datetime import datetime
import traceback
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from he_database_connect import get_connection

try:
    from he_database_connect import get_connection
except ImportError as e:
    print(f"[ERROR] Cannot import get_connection: {e}")
    sys.exit(1)

def log_error_to_db(file_name, error_description=None, created_by=None, env="dev"):
    try:
        if error_description is None:
            error_description = traceback.format_exc()
        if not created_by:
            created_by = os.getenv("USERNAME", "system")

        conn = get_connection(env=env)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO he_error_logs (file_name, error_description, created_at, created_by)
            VALUES (%s, %s, %s, %s)
        """, (file_name, error_description, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), created_by))

        conn.commit()
        print(f"[INFO] Error logged from {file_name} by {created_by}")

    except Exception as db_err:
        print(f"[ERROR] Failed to log error: {db_err}")
        print(traceback.format_exc())
    finally:
        try:
            if cursor: cursor.close()
            if conn: conn.close()
        except: pass



# from datetime import datetime
# import traceback
# import os
# import sys

# # Import DB connection
# try:
#     from he_database_connect import get_connection
# except ImportError as import_err:
#     print(f"[ERROR] Unable to import get_connection: {import_err}")
#     sys.exit(1)

# def log_error_to_db(file_name, error_description=None, created_by=None, env="dev"):
#     """
#     Logs error details into the he_error_logs table.

#     Args:
#         file_name (str): Name of the Python file (use os.path.basename(__file__)).
#         error_description (str): Detailed error message or traceback (auto-captured if not passed).
#         created_by (str): Username or system that triggered the error.
#         env (str): Database environment - 'dev', 'test', 'prod'
#     """

#     try:
#         # Auto-detect traceback if not provided
#         if error_description is None:
#             error_description = traceback.format_exc()

#         # Use system username if created_by not passed
#         if not created_by:
#             created_by = os.getenv("USERNAME", "system")

#         # Get DB connection
#         conn = get_connection(env=env)
#         cursor = conn.cursor()

#         insert_query = """
#             INSERT INTO he_error_logs (file_name, error_description, created_at, created_by)
#             VALUES (%s, %s, %s, %s)
#         """
#         values = (
#             file_name,
#             error_description,
#             datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             created_by
#         )

#         cursor.execute(insert_query, values)
#         conn.commit()
#         print(f"[INFO] Error logged from {file_name} by {created_by}")

#     except Exception as db_err:
#         print(f"[ERROR] Failed to log error to DB: {db_err}")
#         print(traceback.format_exc())

#     finally:
#         try:
#             if cursor:
#                 cursor.close()
#             if conn:
#                 conn.close()
#         except Exception:
#             pass



# from datetime import datetime
# import traceback
# import os
# import sys


# try:
#     from he_database_connect import get_connection
# except ImportError:
#     print("[ERROR] Unable to import get_connection from database_connect.py")
#     sys.exit(1)

# def log_error_to_db(file_name, error_description, created_by="system", env="dev"):
#     """Logs an error to the error_logs table using connection from database_connect."""
#     try:
#         conn = get_connection(env=env)
#         cursor = conn.cursor()

#         insert_query = """
#             INSERT INTO he_error_logs (file_name, error_description, created_at, created_by)
#             VALUES (%s, %s, %s, %s)
#         """

#         values = (
#             file_name,
#             error_description,
#             datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             created_by
#         )

#         cursor.execute(insert_query, values)
#         conn.commit()
#         print(f"[INFO] Error logged to DB from {file_name}")

#     except Exception as db_error:
#         print(f"[ERROR] Failed to log error to DB: {db_error}")

#     finally:
#         if 'cursor' in locals():
#             cursor.close()
#         if 'conn' in locals():
#             conn.close()
