import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join("tru", "Data", "mortgage_leads.db")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            loan_purpose TEXT,
            property_type TEXT,
            location_nh TEXT,
            est_value REAL,
            down_payment REAL,
            credit_score TEXT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            status TEXT DEFAULT 'new'
        )
    ''')
    conn.commit()
    conn.close()

class LeadScorer:
    @staticmethod
    def calculate_score(data):
        score = 0
        # High value home
        if data.get('est_value', 0) > 400000: score += 30
        # Solid down payment
        if data.get('down_payment', 0) > 50000: score += 20
        # Good credit
        if "740+" in str(data.get('credit_score')): score += 50
        elif "680" in str(data.get('credit_score')): score += 30
        
        if score >= 80: return "HOT"
        if score >= 50: return "WARM"
        return "COLD"

def save_lead(data):
    score = LeadScorer.calculate_score(data)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leads (
            timestamp, loan_purpose, property_type, location_nh, 
            est_value, down_payment, credit_score, first_name, 
            last_name, email, phone, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data.get('loan_purpose'),
        data.get('property_type'),
        data.get('location_nh'),
        data.get('est_value'),
        data.get('down_payment'),
        data.get('credit_score'),
        data.get('first_name'),
        data.get('last_name'),
        data.get('email'), # In next iteration: encrypt(data.get('email'))
        data.get('phone'), # In next iteration: encrypt(data.get('phone'))
        score
    ))
    conn.commit()
    conn.close()

def export_to_csv():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM leads", conn)
    conn.close()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_path = os.path.join("tru", "Projects", "Mortgage_LeadGen_NH", f"leads_export_{timestamp}.csv")
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    
    df.to_csv(export_path, index=False)
    return export_path

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
