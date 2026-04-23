from sqlalchemy.orm import Session
from src.domain.repositories import IChatRepository
from src.domain.entities import ChatMessage
from src.infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """Implementación concreta de IChatRepository usando SQLAlchemy."""

    def __init__(self, db: Session):
        """Recibe la sesión de base de datos inyectada."""
        self.db = db


    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """Convierte un modelo ORM a entidad del dominio."""
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        """Convierte una entidad del dominio a modelo ORM."""
        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp,
        )

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje y retorna la entidad con ID asignado."""
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(
        self, session_id: str, limit: int | None = None
    ) -> list[ChatMessage]:
        """Obtiene el historial completo de una sesión en orden cronológico."""
        query = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).order_by(ChatMemoryModel.timestamp)

        if limit:
            query = query.limit(limit)

        return [self._model_to_entity(m) for m in query.all()]

    def delete_session_history(self, session_id: str) -> int:
        """Elimina todos los mensajes de una sesión. Retorna cuántos eliminó."""
        deleted = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).delete()
        self.db.commit()
        return deleted

    def get_recent_messages(self, session_id: str, count: int) -> list[ChatMessage]:
        """Obtiene los últimos N mensajes en orden cronológico."""
        models = self.db.query(ChatMemoryModel).filter(
            ChatMemoryModel.session_id == session_id
        ).order_by(ChatMemoryModel.timestamp.desc()).limit(count).all()


        models.reverse()
        return [self._model_to_entity(m) for m in models]