"""
Módulo de implementación concreta del repositorio de chat.

Implementa IChatRepository usando SQLAlchemy para persistir
y recuperar mensajes de chat de la base de datos SQLite.
"""

from sqlalchemy.orm import Session
from src.domain.repositories import IChatRepository
from src.domain.entities import ChatMessage
from src.infrastructure.db.models import ChatMemoryModel


class SQLChatRepository(IChatRepository):
    """Implementación concreta de IChatRepository usando SQLAlchemy.
     Traduce entre entidades del dominio y modelos ORM, y ejecuta
    las consultas necesarias contra la base de datos.

    Atributos:
        db (Session): Sesión de SQLAlchemy inyectada desde get_db().

    Ejemplo:
        >>> repo = SQLChatRepository(db)
        >>> repo.save_message(message)
    """

    def __init__(self, db: Session):
        """Recibe la sesión de base de datos inyectada."""
        self.db = db

    def _model_to_entity(self, model: ChatMemoryModel) -> ChatMessage:
        """Convierte un modelo ORM a entidad del dominio.

        Args:
            model (ChatMemoryModel): Modelo ORM a convertir.

        Retorna:
            ChatMessage: Entidad del dominio con los datos del modelo."""
        return ChatMessage(
            id=model.id,
            session_id=model.session_id,
            role=model.role,
            message=model.message,
            timestamp=model.timestamp,
        )

    def _entity_to_model(self, entity: ChatMessage) -> ChatMemoryModel:
        """Convierte una entidad del dominio a modelo ORM.
        Args:
            entity (ChatMessage): Entidad del dominio a convertir.

        Retorna:
            ChatMemoryModel: Modelo ORM con los datos de la entidad.
        """
        return ChatMemoryModel(
            id=entity.id,
            session_id=entity.session_id,
            role=entity.role,
            message=entity.message,
            timestamp=entity.timestamp,
        )

    def save_message(self, message: ChatMessage) -> ChatMessage:
        """Guarda un mensaje y retorna la entidad con ID asignado.
         Args:
            message (ChatMessage): Entidad a guardar.

        Retorna:
            ChatMessage: La entidad guardada con su ID asignado.
        """
        model = self._entity_to_model(message)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def get_session_history(
        self, session_id: str, limit: int | None = None
    ) -> list[ChatMessage]:
        """Obtiene el historial completo de una sesión en orden cronológico.
         Args:
            session_id (str): ID de la sesión a consultar.
            limit (int | None): Límite de mensajes. Sin límite si es None.

        Retorna:
            list[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        query = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp)
        )

        if limit:
            query = query.limit(limit)

        return [self._model_to_entity(m) for m in query.all()]

    def delete_session_history(self, session_id: str) -> int:
        """Elimina todos los mensajes de una sesión. Retorna cuántos eliminó.

        Args:
            session_id (str): ID de la sesión a limpiar.

        Returns:
            int: Número de mensajes eliminados."""
        deleted = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .delete()
        )
        self.db.commit()
        return deleted

    def get_recent_messages(self, session_id: str, count: int) -> list[ChatMessage]:
        """Obtiene los últimos N mensajes en orden cronológico.
        Primero ordena descendente para tomar los más recientes,
        luego invierte para retornarlos en orden cronológico correcto.
        Esto es crucial para que la IA entienda el contexto en orden.

        Args:
            session_id (str): ID de la sesión a consultar.
            count (int): Número de mensajes a retornar.

        Retorna:
            list[ChatMessage]: Últimos N mensajes en orden cronológico.
        """
        models = (
            self.db.query(ChatMemoryModel)
            .filter(ChatMemoryModel.session_id == session_id)
            .order_by(ChatMemoryModel.timestamp.desc())
            .limit(count)
            .all()
        )

        models.reverse()
        return [self._model_to_entity(m) for m in models]
