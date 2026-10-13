import sqlite3

_db = sqlite3.connect("scores.db", check_same_thread=False)
_db.execute("CREATE TABLE IF NOT EXISTS scores (name TEXT, score INTEGER, time INTEGER)")


def add_score(name, score, seconds):
    _db.execute("INSERT INTO scores VALUES (?, ?, ?)", (name[:20], score, seconds))
    _db.commit()


def top_scores(limit=10):
    rows = _db.execute(
        "SELECT name, score, time FROM scores ORDER BY score DESC, time ASC LIMIT ?",
        (limit,),
    ).fetchall()
    return [
        {"name": n, "score": s, "time": f"{t // 60:02d}:{t % 60:02d}"}
        for n, s, t in rows
    ]