import os 
import sys 
from pathlib import Path 
from sqlite3 import connect, Connection, Cursor, IntegrityError, Error

sqlite3Conn: Connection | None = None 
sqlite3Cursor: Cursor | None = None 

def connect_to_sqlite3(pSqlite3FileName: str | None = None, pResetConnection: bool = False):
    global sqlite3Conn, sqlite3Cursor 
    sqlite3DbFilepath: str | None = None

    if sqlite3Conn:
        if not pResetConnection:
            return 
        sqlite3Conn = None 

    if not pSqlite3FileName:
        pSqlite3FileName = os.getenv('CRYPTID_SQLITE_DB') if os.getenv('CRYPTID_SQLITE_DB') is not None else "cryptid.db"
        sqlite3DbFilepath = str(Path(__file__).resolve().parents[1] / "data" / pSqlite3FileName)
    try:
        sqlite3Conn = connect(sqlite3DbFilepath, check_same_thread=False)
        sqlite3Cursor = sqlite3Conn.cursor()

        print("Connection to SQLite3 database successful")
    except Error as err:
        print(f"An error occured: {err}")
        sys.exit()
    

# Connect to Sqlite3
connect_to_sqlite3()