from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.infrastructure.db.database import get_db, init_db
from src.infrastructure.db.__init__ import load_initial_data
from src.infrastructure.repositories.product_repository import SQLProductRepository
from src.infrastructure.repositories.chat_repository import SQLChatRepository
from src.infrastructure.llm_providers.gemini_service import GeminiService
from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.application.dtos import ChatMessageRequestDTO, ChatMessageResponseDTO
from src.domain.exceptions import ProductNotFoundError, ChatServiceError


app = FastAPI(
    title="E-Commerce Chat AI",
    description="API de e-commerce con asistente de IA para ventas de zapatos.",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    """Inicializa la base de datos y carga datos iniciales."""
    init_db()
    load_initial_data()



@app.get("/")
def root():
    """Información básica de la API."""
    return {
        "name": "E-Commerce Chat AI",
        "version": "1.0.0",
        "description": "Asistente de IA para ventas de zapatos.",
        "endpoints": [
            "GET  /products",
            "GET  /products/{product_id}",
            "POST /chat",
            "GET  /chat/history/{session_id}",
            "DELETE /chat/history/{session_id}",
            "GET  /health",
        ],
    }


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    """Lista todos los productos disponibles."""
    repo = SQLProductRepository(db)
    service = ProductService(repo)
    return service.get_all_products()


@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Obtiene un producto por su ID."""
    try:
        repo = SQLProductRepository(db)
        service = ProductService(repo)
        return service.get_product_by_id(product_id)
    except ProductNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/chat", response_model=ChatMessageResponseDTO)
async def chat(request: ChatMessageRequestDTO, db: Session = Depends(get_db)):
    """Procesa un mensaje del usuario y retorna la respuesta de la IA."""
    try:
        product_repo = SQLProductRepository(db)
        chat_repo = SQLChatRepository(db)
        ai_service = GeminiService()
        service = ChatService(product_repo, chat_repo, ai_service)
        return await service.process_message(request)
    except ChatServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history/{session_id}")
def get_chat_history(
    session_id: str,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """Obtiene el historial de mensajes de una sesión."""
    chat_repo = SQLChatRepository(db)
    service = ChatService(chat_repo, chat_repo, None)
    return service.get_session_history(session_id, limit)


@app.delete("/chat/history/{session_id}")
def delete_chat_history(session_id: str, db: Session = Depends(get_db)):
    """Elimina el historial de mensajes de una sesión."""
    chat_repo = SQLChatRepository(db)
    service = ChatService(chat_repo, chat_repo, None)
    deleted = service.clear_session_history(session_id)
    return {"session_id": session_id, "deleted_messages": deleted}


@app.get("/health")
def health():
    """Health check de la API."""
    return {"status": "ok", "timestamp": datetime.utcnow()}