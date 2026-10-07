"""Simple but real login: passwords are salted and hashed (PBKDF2), never stored in plain text."""
import hashlib, os, re
from datetime import date
import db

ROLES = ["Farm Owner", "Veterinarian", "Buyer"]

def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 120_000).hex()

def create_user(username, full_name, role, password):
    username = username.strip().lower()
    if not re.fullmatch(r"[a-z0-9_.]{3,20}", username):
        return False, "Username 3 se 20 characters ka ho (sirf a-z, 0-9, _ ya .)."
    if not full_name.strip():
        return False, "Poora naam likhein."
    if role not in ROLES:
        return False, "Role chunein."
    if len(password) < 6:
        return False, "Password kam az kam 6 characters ka ho."
    if db.q("SELECT 1 FROM users WHERE username=?", (username,)):
        return False, "Yeh username pehle se maujood hai."
    salt = os.urandom(16).hex()
    db.run("INSERT INTO users(username,full_name,role,salt,pw_hash,created) VALUES(?,?,?,?,?,?)",
           (username, full_name.strip(), role, salt, _hash(password, salt), str(date.today())))
    return True, "Account ban gaya. Ab login karein."

def login(username, password):
    rows = db.q("SELECT * FROM users WHERE username=?", (username.strip().lower(),))
    if not rows:
        return None
    u = rows[0]
    return u if _hash(password, u["salt"]) == u["pw_hash"] else None

def ensure_demo_users():
    if db.q("SELECT COUNT(*) n FROM users")[0]["n"] == 0:
        create_user("owner", "Demo Farm Owner", "Farm Owner", "owner123")
        create_user("vet", "Dr. Demo Vet", "Veterinarian", "vet123")
        create_user("buyer", "Demo Buyer", "Buyer", "buyer123")
