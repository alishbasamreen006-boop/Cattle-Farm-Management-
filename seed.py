"""DUMMY demo data. Replace with real data from your Mianwali farm interviews later."""
import random
from datetime import date, timedelta
import db, service
from blockchain import Chain

def seed(chain=None):
    db.init()
    if db.q("SELECT COUNT(*) n FROM animals")[0]["n"] > 0:
        return
    chain = chain or Chain()
    random.seed(7)
    today = date.today()
    animals = [("MW-001","Lali","Buffalo","Nili-Ravi",54,610),("MW-002","Moti","Buffalo","Nili-Ravi",48,590),
               ("MW-003","Chitti","Cow","Sahiwal",40,420),("MW-004","Gulabo","Cow","Cholistani",36,390),
               ("MW-005","Kali","Buffalo","Kundi",60,640),("MW-006","Rani","Cow","Sahiwal",30,380),
               ("MW-007","Sohni","Buffalo","Nili-Ravi",44,580),("MW-008","Bholi","Cow","Cross-bred",28,360)]
    for tag, name, sp, br, age, w in animals:
        db.run("INSERT INTO animals(tag,name,species,breed,age_months,weight_kg,owner,created) VALUES(?,?,?,?,?,?,?,?)",
               (tag, name, sp, br, age, w, "Demo Farm Owner", str(today - timedelta(days=200))))
        service.add_record(chain, tag, "REGISTRATION", today - timedelta(days=200), f"{sp} {br}, {age} months, {w} kg", "Demo Farm Owner")
        service.add_record(chain, tag, "VACCINATION", today - timedelta(days=60), "FMD vaccine, batch FMD-2026-A", "Dr. Demo Vet",
                           next_due=today + timedelta(days=random.randint(-5, 120)))
    service.add_record(chain, "MW-003", "TREATMENT", today - timedelta(days=20), "Mastitis, antibiotic course 5 days", "Dr. Demo Vet")
    for d in range(30):
        day = str(today - timedelta(days=d))
        for tag, _, sp, *_ in animals:
            base = 9 if sp == "Buffalo" else 11
            db.run("INSERT INTO milk(tag,day,liters) VALUES(?,?,?)", (tag, day, round(base + random.uniform(-2, 2.5), 1)))
        db.run("INSERT INTO expenses(day,category,amount,tag,note) VALUES(?,?,?,?,?)", (day, "Feed", random.randint(7000, 9000), None, "daily chara/khal"))
        db.run("INSERT INTO income(day,source,amount,tag) VALUES(?,?,?,?)", (day, "Milk sale", random.randint(15000, 18000), None))
    db.run("INSERT INTO expenses(day,category,amount,tag,note) VALUES(?,?,?,?,?)", (str(today - timedelta(days=20)), "Medicine", 3500, "MW-003", "mastitis treatment"))
    db.run("INSERT INTO expenses(day,category,amount,tag,note) VALUES(?,?,?,?,?)", (str(today - timedelta(days=10)), "Labour", 30000, None, "monthly wages"))
