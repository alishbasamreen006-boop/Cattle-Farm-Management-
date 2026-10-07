"""Business logic: save to database AND anchor the fingerprint on the blockchain."""
import db
from blockchain import record_hash

def add_record(chain, tag, rec_type, rec_date, details, by_user, next_due=""):
    r = {"tag": tag, "rec_type": rec_type, "rec_date": str(rec_date), "details": details,
         "next_due": str(next_due or ""), "by_user": by_user}
    h = record_hash(db.record_payload(r))
    tx = chain.add_event(tag, rec_type, h)
    rid = db.run("INSERT INTO records(tag,rec_type,rec_date,details,next_due,by_user,chain_hash,tx_hash) VALUES(?,?,?,?,?,?,?,?)",
                 (tag, rec_type, r["rec_date"], details, r["next_due"], by_user, h, tx))
    return rid, h, tx

def verify(chain, tag):
    """Compare every database record against the blockchain."""
    on_chain = chain.get_events(tag)
    chain_hashes = [e["hash"] for e in on_chain]
    rows = db.q("SELECT * FROM records WHERE tag=? ORDER BY id", (tag,))
    results, seen = [], set()
    for r in rows:
        current = record_hash(db.record_payload(r))
        ok = current in chain_hashes
        if ok: seen.add(current)
        results.append({"id": r["id"], "type": r["rec_type"], "date": r["rec_date"], "details": r["details"],
                        "by": r["by_user"], "status": "VERIFIED" if ok else "TAMPERED", "tx": r["tx_hash"]})
    missing = [e for e in on_chain if e["hash"] not in seen]
    all_ok = all(x["status"] == "VERIFIED" for x in results) and not missing and len(results) > 0
    return results, missing, all_ok

def resync(chain):
    """Local test chain forgets everything when the app restarts. Re-anchor the ORIGINAL stored hashes."""
    if chain.live:
        return
    for r in db.q("SELECT * FROM records ORDER BY id"):
        chain.add_event(r["tag"], r["rec_type"], r["chain_hash"])
