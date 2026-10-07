import sqlite3, json
from pathlib import Path
from datetime import date

DB_PATH = Path(__file__).parent / "farm.db"

def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init():
    with conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS animals(
            tag TEXT PRIMARY KEY, name TEXT, species TEXT, breed TEXT, age_months INTEGER,
            weight_kg REAL, owner TEXT, status TEXT DEFAULT 'Active', created TEXT);
        CREATE TABLE IF NOT EXISTS records(
            id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT, rec_type TEXT, rec_date TEXT,
            details TEXT, next_due TEXT, by_user TEXT, chain_hash TEXT, tx_hash TEXT);
        CREATE TABLE IF NOT EXISTS milk(
            id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT, day TEXT, liters REAL);
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT, day TEXT, category TEXT, amount REAL, tag TEXT, note TEXT);
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY, full_name TEXT, role TEXT, salt TEXT, pw_hash TEXT, created TEXT);
        CREATE TABLE IF NOT EXISTS income(
            id INTEGER PRIMARY KEY AUTOINCREMENT, day TEXT, source TEXT, amount REAL, tag TEXT);
        """)

def q(sql, args=()):
    with conn() as c:
        return [dict(r) for r in c.execute(sql, args).fetchall()]

def run(sql, args=()):
    with conn() as c:
        cur = c.execute(sql, args)
        return cur.lastrowid

def record_payload(r: dict) -> dict:
    """The exact fields that are fingerprinted. Must match what was hashed at save time."""
    return {"tag": r["tag"], "rec_type": r["rec_type"], "rec_date": r["rec_date"],
            "details": r["details"], "next_due": r["next_due"] or "", "by_user": r["by_user"]}
