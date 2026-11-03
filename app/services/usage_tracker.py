import os
import sqlite3
from datetime import UTC, datetime

from app.config import get_settings
from app.schemas import ModelUsageSummary, UsageRecord, UsageResponse


class UsageTracker:
    def __init__(self, db_path: str | None = None):
        settings = get_settings()
        self.db_path = db_path or settings.usage_db_path
        self._shared_conn: sqlite3.Connection | None = None

        if self.db_path == ":memory:":
            self._shared_conn = sqlite3.connect(":memory:", check_same_thread=False)
            self._shared_conn.row_factory = sqlite3.Row
        else:
            os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)

        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        if self._shared_conn is not None:
            return self._shared_conn
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        conn = self._get_connection()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                model TEXT NOT NULL,
                prompt_tokens INTEGER NOT NULL,
                completion_tokens INTEGER NOT NULL,
                total_tokens INTEGER NOT NULL,
                cost_usd REAL NOT NULL,
                latency_ms REAL NOT NULL,
                status TEXT NOT NULL
            )
            """
        )
        conn.commit()
        if self._shared_conn is None:
            conn.close()

    def log(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost_usd: float,
        latency_ms: float,
        status: str = "success",
    ) -> UsageRecord:
        now = datetime.now(UTC).isoformat()
        total_tokens = prompt_tokens + completion_tokens
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO usage_logs (
                    timestamp, model, prompt_tokens, completion_tokens,
                    total_tokens, cost_usd, latency_ms, status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now,
                    model,
                    prompt_tokens,
                    completion_tokens,
                    total_tokens,
                    cost_usd,
                    latency_ms,
                    status,
                ),
            )
            record_id = cursor.lastrowid or 0
            conn.commit()
        finally:
            if self._shared_conn is None:
                conn.close()

        return UsageRecord(
            id=record_id,
            timestamp=now,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=round(cost_usd, 6),
            latency_ms=round(latency_ms, 2),
            status=status,
        )

    def get_summary(self) -> UsageResponse:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()

            # Overall aggregates
            cursor.execute(
                """
                SELECT 
                    COUNT(*) as count,
                    COALESCE(SUM(prompt_tokens), 0) as total_prompt,
                    COALESCE(SUM(completion_tokens), 0) as total_comp,
                    COALESCE(SUM(total_tokens), 0) as total_tok,
                    COALESCE(SUM(cost_usd), 0.0) as total_cost
                FROM usage_logs
                """
            )
            agg = cursor.fetchone()
            total_requests = agg["count"] if agg else 0
            total_prompt = agg["total_prompt"] if agg else 0
            total_comp = agg["total_comp"] if agg else 0
            total_tok = agg["total_tok"] if agg else 0
            total_cost = agg["total_cost"] if agg else 0.0

            # Aggregates by model
            cursor.execute(
                """
                SELECT 
                    model,
                    COUNT(*) as calls,
                    COALESCE(SUM(prompt_tokens), 0) as prompt_tokens,
                    COALESCE(SUM(completion_tokens), 0) as completion_tokens,
                    COALESCE(SUM(total_tokens), 0) as total_tokens,
                    COALESCE(SUM(cost_usd), 0.0) as total_cost_usd
                FROM usage_logs
                GROUP BY model
                """
            )
            by_model: dict[str, ModelUsageSummary] = {}
            for row in cursor.fetchall():
                by_model[row["model"]] = ModelUsageSummary(
                    calls=row["calls"],
                    prompt_tokens=row["prompt_tokens"],
                    completion_tokens=row["completion_tokens"],
                    total_tokens=row["total_tokens"],
                    total_cost_usd=round(row["total_cost_usd"], 6),
                )

            # Recent 20 calls
            cursor.execute(
                """
                SELECT 
                    id, timestamp, model, prompt_tokens, completion_tokens,
                    total_tokens, cost_usd, latency_ms, status
                FROM usage_logs
                ORDER BY id DESC
                LIMIT 20
                """
            )
            recent_calls = [
                UsageRecord(
                    id=row["id"],
                    timestamp=row["timestamp"],
                    model=row["model"],
                    prompt_tokens=row["prompt_tokens"],
                    completion_tokens=row["completion_tokens"],
                    total_tokens=row["total_tokens"],
                    cost_usd=round(row["cost_usd"], 6),
                    latency_ms=round(row["latency_ms"], 2),
                    status=row["status"],
                )
                for row in cursor.fetchall()
            ]
        finally:
            if self._shared_conn is None:
                conn.close()

        return UsageResponse(
            total_requests=total_requests,
            total_prompt_tokens=total_prompt,
            total_completion_tokens=total_comp,
            total_tokens=total_tok,
            total_cost_usd=round(total_cost, 6),
            by_model=by_model,
            recent_calls=recent_calls,
        )

    def reset(self) -> None:
        conn = self._get_connection()
        try:
            conn.execute("DELETE FROM usage_logs")
            conn.commit()
        finally:
            if self._shared_conn is None:
                conn.close()


_default_tracker: UsageTracker | None = None


def get_usage_tracker() -> UsageTracker:
    global _default_tracker
    if _default_tracker is None:
        _default_tracker = UsageTracker()
    return _default_tracker
