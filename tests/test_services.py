import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime
from src.domain.entities import Product, ChatMessage
from src.domain.exceptions import ProductNotFoundError
from src.application.product_service import ProductService
from src.application.chat_service import ChatService
from src.application.dtos import ChatMessageRequestDTO

@pytest.fixture
def mock_product_repo():
    return MagicMock()


@pytest.fixture
def mock_chat_repo():
    return MagicMock()


@pytest.fixture
def mock_ai_service():
    service = MagicMock()
    service.generate_response = AsyncMock(return_value="Respuesta de prueba")
    return service


@pytest.fixture
def sample_product():
    return Product(
        id=1,
        name="Air Max 90",
        brand="Nike",
        category="Running",
        size="42",
        color="Blanco",
        price=120.00,
        stock=10,
        description="Zapatilla clásica.",
    )


class TestProductService:

    def test_get_all_products(self, mock_product_repo, sample_product):
        """retorna lista de productos del repositorio"""
        mock_product_repo.get_all.return_value = [sample_product]
        service = ProductService(mock_product_repo)
        result = service.get_all_products()
        assert len(result) == 1
        assert result[0].name == "Air Max 90"

    def test_get_product_by_id(self, mock_product_repo, sample_product):
        """retorna el producto cuando existe"""
        mock_product_repo.get_by_id.return_value = sample_product
        service = ProductService(mock_product_repo)
        result = service.get_product_by_id(1)
        assert result.id == 1

    def test_get_product_by_id_not_found(self, mock_product_repo):
        """lanza ProductNotFoundError cuando no existe"""
        mock_product_repo.get_by_id.return_value = None
        service = ProductService(mock_product_repo)
        with pytest.raises(ProductNotFoundError):
            service.get_product_by_id(99)

    def test_get_available_products(self, mock_product_repo, sample_product):
        """retorna solo productos con stock > 0"""
        out_of_stock = Product(
            id=2, name="Test", brand="Adidas", category="Casual",
            size="41", color="Negro", price=50, stock=0, description="Test"
        )
        mock_product_repo.get_all.return_value = [sample_product, out_of_stock]
        service = ProductService(mock_product_repo)
        result = service.get_available_products()
        assert len(result) == 1
        assert result[0].stock > 0

    def test_delete_product_not_found(self, mock_product_repo):
        """lanza ProductNotFoundError al eliminar uno que no existe"""
        mock_product_repo.get_by_id.return_value = None
        service = ProductService(mock_product_repo)
        with pytest.raises(ProductNotFoundError):
            service.delete_product(99)


class TestChatService:

    @pytest.mark.asyncio
    async def test_process_message_returns_response(
        self, mock_product_repo, mock_chat_repo, mock_ai_service, sample_product
    ):
        """retorna la respuesta generada por la IA"""
        mock_product_repo.get_all.return_value = [sample_product]
        mock_chat_repo.get_recent_messages.return_value = []
        mock_chat_repo.save_message.side_effect = lambda msg: msg

        service = ChatService(mock_product_repo, mock_chat_repo, mock_ai_service)
        request = ChatMessageRequestDTO(session_id="s1", message="Hola")
        response = await service.process_message(request)

        assert response.assistant_message == "Respuesta de prueba"
        assert response.session_id == "s1"

    @pytest.mark.asyncio
    async def test_process_message_saves_two_messages(
        self, mock_product_repo, mock_chat_repo, mock_ai_service, sample_product
    ):
        """guarda el mensaje del usuario y la respuesta del asistente"""
        mock_product_repo.get_all.return_value = [sample_product]
        mock_chat_repo.get_recent_messages.return_value = []
        mock_chat_repo.save_message.side_effect = lambda msg: msg

        service = ChatService(mock_product_repo, mock_chat_repo, mock_ai_service)
        request = ChatMessageRequestDTO(session_id="s1", message="Hola")
        await service.process_message(request)

        assert mock_chat_repo.save_message.call_count == 2

    def test_get_session_history(
        self, mock_product_repo, mock_chat_repo, mock_ai_service
    ):
        """retorna lista del historial de la sesión"""
        mock_chat_repo.get_session_history.return_value = []
        service = ChatService(mock_product_repo, mock_chat_repo, mock_ai_service)
        result = service.get_session_history("s1", 10)
        assert isinstance(result, list)

    def test_clear_session_history(
        self, mock_product_repo, mock_chat_repo, mock_ai_service
    ):
        """retorna el número de mensajes eliminados"""
        mock_chat_repo.delete_session_history.return_value = 5
        service = ChatService(mock_product_repo, mock_chat_repo, mock_ai_service)
        result = service.clear_session_history("s1")
        assert result == 5