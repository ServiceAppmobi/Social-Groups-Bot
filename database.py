import sqlite3
from config import DB_PATH


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS leads (
            post_id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            country TEXT DEFAULT 'BR',
            source_channel TEXT NOT NULL,
            title TEXT,
            url TEXT,
            author TEXT,
            content_snippet TEXT,
            lead_type TEXT,
            ai_draft TEXT,
            notified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def is_post_seen(post_id: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM leads WHERE post_id = ?", (post_id,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def save_lead(lead: dict, notified: int = 0):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT OR IGNORE INTO leads
        (post_id, platform, country, source_channel, title, url, author, content_snippet, lead_type, ai_draft, notified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            lead["post_id"],
            lead.get("platform", "social"),
            lead.get("country", "BR"),
            lead.get("source_channel", ""),
            lead.get("title", ""),
            lead.get("url", ""),
            lead.get("author", ""),
            lead.get("content_snippet", ""),
            lead.get("lead_type", ""),
            lead.get("ai_draft", ""),
            notified,
        ),
    )
    conn.commit()
    conn.close()


def mark_notified(post_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE leads SET notified = 1 WHERE post_id = ?", (post_id,))
    conn.commit()
    conn.close()


def get_stats() -> dict:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    stats = {}
    queries = {
        "total": "SELECT COUNT(*) FROM leads",
        "whatsapp": "SELECT COUNT(*) FROM leads WHERE platform = 'whatsapp'",
        "facebook": "SELECT COUNT(*) FROM leads WHERE platform = 'facebook'",
        "tiktok": "SELECT COUNT(*) FROM leads WHERE platform = 'tiktok'",
        "brazil": "SELECT COUNT(*) FROM leads WHERE country = 'BR'",
        "mexico": "SELECT COUNT(*) FROM leads WHERE country = 'MX'",
        "notified": "SELECT COUNT(*) FROM leads WHERE notified = 1",
    }
    for key, sql in queries.items():
        cur.execute(sql)
        stats[key] = cur.fetchone()[0]
    conn.close()
    return stats
