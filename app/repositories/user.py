from app.database.connection import get_connection


class UserRepository:
    """Repository for accessing authentication users."""

    def create_user(
        self,
        user_id: str,
        email: str,
        password_hash: str,
        role: str,
    ) -> dict:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (
                id,
                email,
                password_hash,
                role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                email,
                password_hash,
                role,
            ),
        )

        connection.commit()
        connection.close()

        return {
            "id": user_id,
            "email": email,
            "password_hash": password_hash,
            "role": role,
        }

    def get_user_by_email(self, email: str) -> dict | None:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, email, password_hash, role
            FROM users
            WHERE email = ?
            """,
            (email,),
        )

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return {
            "id": row[0],
            "email": row[1],
            "password_hash": row[2],
            "role": row[3],
        }