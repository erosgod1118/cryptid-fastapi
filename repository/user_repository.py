from model.user import User 
from .init import sqlite3Cursor, IntegrityError
from errors.data_errors import DataDuplicationError, DataMissingError

sqlite3Cursor.execute("""create table if not exists
                            user(
                                name text primary key,
                                hash text
                            )
                      """)
def row_to_model(pRow: tuple) -> User:
    name, hash = pRow 
    return User(name = name, hash = hash)

def get_all() -> list[User]:
    query = "select * from user"
    sqlite3Cursor.execute(query)

    return [row_to_model(row) for row in sqlite3Cursor.fetchall()]

def get_one_by_name(pName: str) -> User:
    query = "select * from user where name=:username"
    params = {"username": pName}

    sqlite3Cursor.execute(query, params)

    row = sqlite3Cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise DataMissingError(msg=f"User {pName} not found")
