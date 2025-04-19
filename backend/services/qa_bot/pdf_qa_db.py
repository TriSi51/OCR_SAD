import sqlite3
from typing import Dict
import os
DB_NAME = "pdf_qa.db"
def delete_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
        print(f"Deleted existing {DB_NAME}.")
    else:
        print(f"{DB_NAME} does not exist.")


def get_connection():
    return sqlite3.connect(DB_NAME)

def save_pdf_binary(file_name:str,  binary_data:bytes):
    conn= sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdf_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT,
            content BLOB,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
                   
    ''')

    cursor.execute(
        "INSERT INTO pdf_files (file_name,content) VALUES (?,?)",
        (file_name,binary_data)
    )
    pdf_id= cursor.lastrowid
    conn.commit()
    conn.close()
    return pdf_id

def get_pdf_by_id(pdf_id: int)-> Dict:
    conn= get_connection()
    conn.row_factory= sqlite3.Row
    cursor= conn.cursor()

    cursor.execute("SELECT * FROM pdf_files WHERE id= ?", (pdf_id,))

    row= cursor.fetchone()

    conn.close()

    if row:
        return dict(row)
    return None