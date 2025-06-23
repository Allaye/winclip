import sqlite3
import json
from datetime import datetime
from winclip.engine.model import Clip

DB_PATH = "clipboard_history.db"

def _connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clips (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            pinned INTEGER DEFAULT 0,
            source_app TEXT,
            type TEXT DEFAULT 'text',
            tags TEXT
        )
        """)
        conn.commit()
        

def insert_clip(clip: Clip):
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO clips (id, content, timestamp, pinned, source_app, type, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            clip.id,
            clip.content,
            clip.timestamp.isoformat(),
            int(clip.pinned),
            clip.source_app,
            clip.type,
            json.dumps(clip.tags or [])
        ))
        conn.commit()


def get_recent_clips(limit=50):
    # Query and convert rows -> List[Clip]
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clips ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        clips = []
        for row in rows:
            clip = Clip(
                id=row[0],
                content=row[1],
                timestamp=datetime.fromisoformat(row[2]),
                pinned=bool(row[3]),
                source_app=row[4],
                type=row[5],
                tags=json.loads(row[6]) if row[6] else []
            )
            clips.append(clip)
        return clips

def pin_unpin_clip(clip: Clip):
    """
    Pin or unpin a clip.
    :param clip: The Clip object to pin or unpin.
    """
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clips SET pinned = ? WHERE id = ?
        """, (int(clip.pinned), clip.id))
        conn.commit()

def delete_clip(clip_id: str):
    """
    Delete a clip by its ID.
    :param clip_id: The ID of the clip to delete.
    """
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clips WHERE id = ?", (clip_id,))
        conn.commit()

def clear_clips():
    """
    Clear all clips from the database, except for pinned clips.
    """
    # Delete all non-pinned clips
    with _connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clips")
        conn.commit()
    pass
