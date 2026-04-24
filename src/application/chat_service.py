from src.domain.repositories import IProductRepository, IChatRepository 
from src.infrastructure.llm_providers.gemini_service import GeminiService
from src .application.dtos import ChatMessageRequestDTO, ChatMessageResponseDTO
from typing import Optional, List
from src.domain.entities import ChatMessage, ChatContext
from src.domain.exceptions import ChatServiceError
from datetime import datetime

class ChatService:
    """Servicio de Ichat"""
    
    def __init__(self,product_repository: IProductRepository, chat_repository: IChatRepository ,ai_service: GeminiService):
        """Recibe el chat por inyección de dependencias."""
        self._chat_repo = chat_repository
        self._product_repo = product_repository
        self._ai_service = ai_service  
        
    async def process_message(self, request: ChatMessageRequestDTO) -> ChatMessageResponseDTO:
        """flujo para procesar mensajes"""
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
                context=context,)
                
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
        
    def get_session_history(self, session_id: str, limit: Optional[int] = None) -> List[ChatMessage]:
        """Obtiene el historial de mensajes de una sesión."""
        return self._chat_repo.get_session_history(session_id, limit)

    def clear_session_history(self, session_id: str) -> int:
        """Elimina todos los mensajes de una sesión."""
        return self._chat_repo.delete_session_history(session_id)