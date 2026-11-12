import sqlite3
from datetime import datetime
from pathlib import Path

from .models import Alert


class AlertStore:
    def __init__(self, database_path: str):
        self.database_path = database_path
        if database_path != ":memory:":
            Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS alerts (
                alert_id TEXT PRIMARY KEY, event_id TEXT UNIQUE NOT NULL,
                asset_id TEXT NOT NULL, site_id TEXT NOT NULL, severity TEXT NOT NULL,
                message TEXT NOT NULL, created_at TEXT NOT NULL)""")

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def add(self, alert: Alert) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT OR IGNORE INTO alerts VALUES (?, ?, ?, ?, ?, ?, ?)",
                (alert.alert_id, alert.event_id, alert.asset_id, alert.site_id,
                 alert.severity, alert.message, alert.created_at.isoformat()),
            )
            return cur.rowcount == 1

    def list(self, limit: int = 100) -> list[Alert]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT alert_id,event_id,asset_id,site_id,severity,message,created_at "
                "FROM alerts ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [Alert(alert_id=r[0], event_id=r[1], asset_id=r[2], site_id=r[3],
                      severity=r[4], message=r[5], created_at=datetime.fromisoformat(r[6]))
                for r in rows]
