import uuid
from datetime import datetime, timezone

from app.database.connection import get_connection


class ConversationRepository:

    def create_conversation(
        self,
        user_id: str,
    ) -> dict:
        conversation_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO conversations (
                id,
                user_id,
                created_at
            )
            VALUES (?, ?, ?)
            """,
            (
                conversation_id,
                user_id,
                created_at,
            ),
        )

        connection.commit()
        connection.close()

        return {
            "id": conversation_id,
            "user_id": user_id,
            "created_at": created_at,
        }

    def get_conversation(
        self,
        conversation_id: str,
    ) -> dict | None:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, user_id, created_at
            FROM conversations
            WHERE id = ?
            """,
            (conversation_id,),
        )

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return {
            "id": row[0],
            "user_id": row[1],
            "created_at": row[2],
        }