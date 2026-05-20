#!/usr/bin/env python3
"""
Anti-Gravity Lead Monitor Utility
=================================
Parses, aggregates, filters, and formats leads captured in the local SQLite database 
and the Obsidian vault markdown files.

Usage:
    python scripts/monitor_leads.py
    python scripts/monitor_leads.py --grade A
    python scripts/monitor_leads.py --stats
    python scripts/monitor_leads.py --export leads_consolidated.csv
"""

import os
import re
import sys
import sqlite3
import argparse
from datetime import datetime

# Configure base directory paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "tru", "Data", "mortgage_leads.db")
VAULT_LEADS_PATH = os.path.join(BASE_DIR, "tru", "Leads")

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def print_header(title):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}{Colors.RESET}\n")

def parse_markdown_lead(filepath):
    """Parses frontmatter and contact details from a vault lead file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract frontmatter
        fm_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL | re.MULTILINE)
        lead_data = {
            "source": "Vault (.md)",
            "file": os.path.basename(filepath),
            "first_name": "",
            "last_name": "",
            "email": "",
            "phone": "",
            "loan_purpose": "",
            "property_type": "",
            "location_nh": "",
            "est_value": 0.0,
            "down_payment": 0.0,
            "credit_score": "",
            "grade": "U",
            "timestamp": ""
        }
        
        if fm_match:
            fm_text = fm_match.group(1)
            for line in fm_text.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    key = key.strip()
                    val = val.strip()
                    if key == "grade": lead_data["grade"] = val
                    elif key == "loan_purpose": lead_data["loan_purpose"] = val
                    elif key == "property_type": lead_data["property_type"] = val
                    elif key == "location": lead_data["location_nh"] = val
                    elif key == "credit_score": lead_data["credit_score"] = val
                    elif key == "est_value": lead_data["est_value"] = float(val) if val else 0.0
                    elif key == "down_payment": lead_data["down_payment"] = float(val) if val else 0.0
                    elif key == "captured_at": lead_data["timestamp"] = val
        
        # Parse body for contact details and name
        name_match = re.search(r'# Lead Intelligence:\s*([^\n]+)', content)
        if name_match:
            name_parts = name_match.group(1).strip().split(' ', 1)
            lead_data["first_name"] = name_parts[0]
            if len(name_parts) > 1:
                lead_data["last_name"] = name_parts[1]
                
        email_match = re.search(r'-\s*\*\*Email\*\*:\s*([^\n]+)', content)
        if email_match: lead_data["email"] = email_match.group(1).strip()
        
        phone_match = re.search(r'-\s*\*\*Phone\*\*:\s*([^\n]+)', content)
        if phone_match: lead_data["phone"] = phone_match.group(1).strip()
        
        # If NH Location in body but not in frontmatter
        loc_match = re.search(r'-\s*\*\*NH Location\*\*:\s*([^\n]+)', content)
        if loc_match and not lead_data["location_nh"]:
            lead_data["location_nh"] = loc_match.group(1).strip()
            
        return lead_data
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Could not parse {filepath}: {e}")
        return None

def fetch_db_leads():
    """Fetches leads from the local SQLite database."""
    leads = []
    if not os.path.exists(DB_PATH):
        return leads
        
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leads'")
        if not cursor.fetchone():
            conn.close()
            return leads
            
        cursor.execute("SELECT * FROM leads ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        for row in rows:
            leads.append({
                "source": "SQLite (db)",
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "phone": row["phone"],
                "loan_purpose": row["loan_purpose"],
                "property_type": row["property_type"],
                "location_nh": row["location_nh"],
                "est_value": row["est_value"],
                "down_payment": row["down_payment"],
                "credit_score": row["credit_score"],
                "grade": row["status"],  # Database stores grade in status
                "timestamp": row["timestamp"],
                "file": "N/A"
            })
        conn.close()
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Database query failed: {e}")
    return leads

def get_all_leads():
    """Aggregates leads from vault markdown files and SQLite database."""
    all_leads = []
    seen_emails = set()
    
    # 1. Parse from Obsidian vault (.md)
    if os.path.exists(VAULT_LEADS_PATH):
        for filename in os.listdir(VAULT_LEADS_PATH):
            if filename.endswith(".md"):
                filepath = os.path.join(VAULT_LEADS_PATH, filename)
                lead = parse_markdown_lead(filepath)
                if lead:
                    all_leads.append(lead)
                    if lead["email"]:
                        seen_emails.add(lead["email"].lower())
                        
    # 2. Parse from SQLite
    db_leads = fetch_db_leads()
    for lead in db_leads:
        # Avoid duplicating if already fetched from Vault Markdown
        if lead["email"] and lead["email"].lower() in seen_emails:
            continue
        all_leads.append(lead)
        
    # Sort all leads by timestamp
    def parse_time(t_str):
        if not t_str:
            return datetime.min
        t_str = t_str.replace("T", " ").replace("Z", "")
        # Try different formats
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(t_str.split(".")[0], fmt.split(".")[0])
            except ValueError:
                continue
        return datetime.min
        
    all_leads.sort(key=lambda x: parse_time(x["timestamp"]), reverse=True)
    return all_leads

def filter_leads(leads, grade_filter=None):
    """Filters leads by grade."""
    if not grade_filter:
        return leads
    return [l for l in leads if l["grade"].strip().upper() == grade_filter.strip().upper()]

def display_leads_table(leads):
    """Prints a beautifully formatted console table of leads."""
    if not leads:
        print(f"  {Colors.YELLOW}[INFO]{Colors.RESET} No leads match the current filters.")
        return
        
    # Headers
    print(f"{Colors.BOLD}{'Date':<11} | {'Name':<18} | {'Location':<14} | {'Value':<8} | {'Down Pymt':<9} | {'Grade':<5} | {'Source':<12}{Colors.RESET}")
    print("-" * 88)
    
    for lead in leads:
        name = f"{lead['first_name']} {lead['last_name']}"
        date_str = lead['timestamp'][:10] if lead['timestamp'] else "N/A"
        grade = lead['grade'].upper()
        
        # Color code grade
        if grade in ("A", "HOT"):
            grade_colored = f"{Colors.GREEN}{grade:<5}{Colors.RESET}"
        elif grade in ("B", "WARM"):
            grade_colored = f"{Colors.YELLOW}{grade:<5}{Colors.RESET}"
        else:
            grade_colored = f"{Colors.RESET}{grade:<5}"
            
        print(f"{date_str:<11} | {name:<18} | {lead['location_nh']:<14} | ${int(lead['est_value'])/1000:>6.0f}k | ${int(lead['down_payment'])/1000:>7.0f}k | {grade_colored} | {lead['source']:<12}")
    print()

def print_statistics(leads):
    """Calculates and displays lead statistics."""
    print_header("NH MORTGAGE LEADS — STATISTICAL SYNOPSIS")
    if not leads:
        print("No leads recorded to generate statistics.")
        return
        
    total_count = len(leads)
    grades = {}
    locations = {}
    total_val = 0.0
    total_dp = 0.0
    
    for lead in leads:
        g = lead["grade"].upper()
        grades[g] = grades.get(g, 0) + 1
        
        loc = lead["location_nh"] or "Unknown"
        locations[loc] = locations.get(loc, 0) + 1
        
        total_val += lead["est_value"]
        total_dp += lead["down_payment"]
        
    avg_val = total_val / total_count
    avg_dp = total_dp / total_count
    
    print(f"{Colors.BOLD}General Summary:{Colors.RESET}")
    print(f"  Total Captured Leads: {total_count}")
    print(f"  Avg Home Value:       ${avg_val:,.2f}")
    print(f"  Avg Down Payment:     ${avg_dp:,.2f}")
    print(f"  Average LTV Ratio:    {((avg_val - avg_dp) / avg_val * 100):.1f}%")
    print()
    
    print(f"{Colors.BOLD}Quality Distribution:{Colors.RESET}")
    for g, count in sorted(grades.items()):
        color = Colors.RESET
        if g in ("A", "HOT"): color = Colors.GREEN
        elif g in ("B", "WARM"): color = Colors.YELLOW
        print(f"  Grade {color}{g:<4}{Colors.RESET}: {count} ({count/total_count*100:.1f}%)")
    print()
    
    print(f"{Colors.BOLD}Top Markets (by volume):{Colors.RESET}")
    for loc, count in sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {loc:<15}: {count} leads")
    print()

def export_leads_csv(leads, filepath):
    """Exports consolidated leads to a CSV file."""
    import csv
    try:
        # Ensure path exists
        dirname = os.path.dirname(filepath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
            
        keys = ["timestamp", "first_name", "last_name", "email", "phone", "loan_purpose", "property_type", "location_nh", "est_value", "down_payment", "credit_score", "grade", "source"]
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([k.upper() for k in keys])
            for lead in leads:
                writer.writerow([lead[k] for k in keys])
        print(f"{Colors.GREEN}[SUCCESS]{Colors.RESET} Consolidated leads exported to {Colors.BOLD}{filepath}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[ERROR]{Colors.RESET} Failed to export leads to CSV: {e}")

def main():
    parser = argparse.ArgumentParser(description="Monitor and manage captured mortgage leads in the workspace.")
    parser.add_argument("--grade", type=str, help="Filter leads by grade (e.g. A, B, C, HOT, WARM)")
    parser.add_argument("--stats", action="store_true", help="Display advanced statistical summary instead of table")
    parser.add_argument("--export", type=str, help="Export leads to the specified CSV filepath")
    
    args = parser.parse_args()
    
    leads = get_all_leads()
    filtered = filter_leads(leads, args.grade)
    
    if args.stats:
        print_statistics(filtered)
    elif args.export:
        export_leads_csv(filtered, args.export)
    else:
        title = "NH MORTGAGE LEADS DASHBOARD (Sovereign Vault)"
        if args.grade:
            title += f" [FILTER: Grade {args.grade.upper()}]"
        print_header(title)
        display_leads_table(filtered)

if __name__ == "__main__":
    main()
