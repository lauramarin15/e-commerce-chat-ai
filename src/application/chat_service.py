"""
Módulo del servicio de aplicación para el chat con IA.

Orquesta la interacción entre el repositorio de productos,
el repositorio de chat y el servicio de IA de Gemini para
proporcionar respuestas contextuales a los usuarios.
"""

from datetime import datetime
from typing import List, Optional

from src.application.dtos import ChatMessageRequestDTO, ChatMessageResponseDTO
from src.domain.entities import ChatContext, ChatMessage
from src.domain.exceptions import ChatServiceError
from src.domain.repositories import IChatRepository, IProductRepository
from src.infrastructure.llm_providers.gemini_service import GeminiService


class ChatService:
    """Servicio de Ichat
    Atributos:
        _product_repo (IProductRepository): Repositorio de productos.
        _chat_repo (IChatRepository): Repositorio de mensajes de chat.
        _ai_service (GeminiService): Servicio de IA de Google Gemini.

    Example:
        >>> service = ChatService(product_repo, chat_repo, ai_service)
        >>> response = await service.process_message(request)
    """

    def __init__(
        self,
        product_repository: IProductRepository,
        chat_repository: IChatRepository,
        ai_service: GeminiService,
    ):
        """Recibe el chat por inyección de dependencias.
        Args:
            product_repository (IProductRepository): Repositorio de productos.
            chat_repository (IChatRepository): Repositorio de mensajes.
            ai_service (GeminiService): Servicio de IA de Google Gemini.
        """
        self._chat_repo = chat_repository
        self._product_repo = product_repository
        self._ai_service = ai_service

    async def process_message(
        self, request: ChatMessageRequestDTO
    ) -> ChatMessageResponseDTO:
        """flujo para procesar mensajes
        Este método realiza el flujo completo:
        1. Obtiene productos disponibles del catálogo
        2. Recupera historial reciente de la conversación
        3. Construye el contexto conversacional
        4. Genera respuesta con IA usando el contexto
        5. Guarda mensaje del usuario y respuesta del asistente
        6. Retorna la respuesta

        Args:
            request (ChatMessageRequestDTO): Mensaje del usuario con session_id.

        Retorna:
            ChatMessageResponseDTO: Respuesta generada por la IA con timestamp.

        Raises:
            ChatServiceError: Si hay un error al procesar el mensaje o
                              comunicarse con el servicio de IA.

        Ejemplo:
            >>> request = ChatMessageRequestDTO(
            ...     session_id="user123",
            ...     message="Busco zapatos Nike"
            ... )
            >>> response = await chat_service.process_message(request)
            >>> print(response.assistant_message)
            "Tengo varios modelos Nike disponibles..."
        """
        try:
            products = self._product_repo.get_all()

            history = self._chat_repo.get_recent_messages(
                session_id=request.session_id,
                count=6,
            )

            context = ChatContext(messages=history)

            ai_response = await self._ai_service.generate_response(
                user_message=request.message,
                products=products,
                context=context,
            )

            user_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="user",
                message=request.message,
                timestamp=datetime.utcnow(),
            )
            self._chat_repo.save_message(user_message)

            assistant_message = ChatMessage(
                id=None,
                session_id=request.session_id,
                role="assistant",
                message=ai_response,
                timestamp=datetime.utcnow(),
            )
            self._chat_repo.save_message(assistant_message)

            return ChatMessageResponseDTO(
                session_id=request.session_id,
                user_message=request.message,
                assistant_message=ai_response,
                timestamp=assistant_message.timestamp,
            )

        except Exception as e:
            raise ChatServiceError(f"Error procesando el mensaje: {str(e)}") from e

    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """Obtiene el historial de mensajes de una sesión.
         Args:
            session_id (str): ID de la sesión a consultar.
            limit (Optional[int]): Límite de mensajes. Sin límite si es None.

        Retorna:
            List[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        return self._chat_repo.get_session_history(session_id, limit)

    def clear_session_history(self, session_id: str) -> int:
        """Elimina todos los mensajes de una sesión.
        Args:
            session_id (str): ID de la sesión a limpiar.

        Returns:
            int: Número de mensajes eliminados.
        """
        return self._chat_repo.delete_session_history(session_id)
