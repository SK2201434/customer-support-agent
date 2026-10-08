from app.repositories.conversation import ConversationRepository


class ConversationService:

    def __init__(
        self,
        repository: ConversationRepository,
    ):
        self.repository = repository

    def create_conversation(
        self,
        user_id: str,
    ) -> dict:
        return self.repository.create_conversation(
            user_id
        )

    def get_conversation(
        self,
        conversation_id: str,
    ) -> dict | None:
        return self.repository.get_conversation(
            conversation_id
        )

    def belongs_to_user(
        self,
        conversation_id: str,
        user_id: str,
    ) -> bool:
        conversation = self.repository.get_conversation(
            conversation_id
        )

        if conversation is None:
            return False

        return conversation["user_id"] == user_id