from datetime import datetime
import pytest
from src.domain.entities import Product, ChatMessage, ChatContext


class TestProduct:

    def test_create_valid_product(self):
        """llamamos la clase Product para crear un objeto"""
        product = Product(
            id=1,
            name="Air Max 90",
            brand="Nike",
            category="Running",
            size="42",
            color="White",
            price=150.0,
            stock=10,
            description="...",
        )

        assert product.name == "Air Max 90"
        assert product.price == 150.0

    def test_price_must_be_greater_than_zero(self):
        """llamamos la clase Product con price=0
        esperamos que __post_init__ lance ValueError"""
        with pytest.raises(ValueError, match="Price must be bigger than 0."):
            Product(
                id=1,
                name="Air Max",
                brand="Nike",
                category="Running",
                size="42",
                color="White",
                price=0,
                stock=10,
                description="...",
            )

    def test_stock_cannot_be_negative(self):
        """llamamos la clase Product con stock=-1
        esperamos que __post_init__ lance ValueError"""
        with pytest.raises(ValueError, match="Stock cannot be negative."):
            Product(
                id=1,
                name="Air Max",
                brand="Nike",
                category="Running",
                size="42",
                color="White",
                price=150.0,
                stock=-1,
                description="...",
            )

    def test_name_cannot_be_empty(self):
        """llamamos la clase Product con name=""
        esperamos que __post_init__ lance ValueError"""
        with pytest.raises(ValueError, match="Product name cannot be empty."):
            Product(
                id=1,
                name="",
                brand="Nike",
                category="Running",
                size="42",
                color="White",
                price=150.0,
                stock=10,
                description="...",
            )

    def test_is_available_with_stock(self):
        """llamamos la clase Product con stock=5"""
        product = Product(
            id=1,
            name="Air Max",
            brand="Nike",
            category="Running",
            size="42",
            color="White",
            price=150.0,
            stock=5,
            description="...",
        )

        """stock=5 > 0 entonces debe retornar True"""

        assert product.is_available() is True

    def test_is_not_available_without_stock(self):
        """llamamos la clase Product con stock=0"""
        product = Product(
            id=1,
            name="Air Max",
            brand="Nike",
            category="Running",
            size="42",
            color="White",
            price=150.0,
            stock=0,
            description="...",
        )

        """stock=0 entonces debe retornar False"""

        assert product.is_available() is False

    def test_reduce_stock(self):
        """llamamos la clase Product con stock=10"""
        product = Product(
            id=1,
            name="Air Max",
            brand="Nike",
            category="Running",
            size="42",
            color="White",
            price=150.0,
            stock=10,
            description="...",
        )
        """stock debe pasar de 10 a 7"""
        product.reduce_stock(3)

        """verificamos que el atributo stock cambió correctamente"""
        assert product.stock == 7

    def test_reduce_stock_insufficient(self):
        """llamamos la clase Product con stock=2"""
        product = Product(
            id=1,
            name="Air Max",
            brand="Nike",
            category="Running",
            size="42",
            color="White",
            price=150.0,
            stock=2,
            description="...",
        )
        """solo hay stock=2, esperamos ValueError"""

        with pytest.raises(ValueError, match="Insufficient stock"):
            product.reduce_stock(5)

    def test_increase_stock(self):
        """llamamos la clase Product con stock=10"""
        product = Product(
            id=1,
            name="Air Max",
            brand="Nike",
            category="Running",
            size="42",
            color="White",
            price=150.0,
            stock=10,
            description="...",
        )
        """stock debe pasar de 10 a 15"""
        product.increase_stock(5)

        """verificamos que el atributo stock cambió correctamente"""
        assert product.stock == 15


class TestChatMessage:

    def test_create_valid_user_message(self):
        """llamamos la clase ChatMessage con role='user'"""
        msg = ChatMessage(
            id=1,
            session_id="abc123",
            role="user",
            message="Hello",
            timestamp=datetime.now(),
        )
        """role='user' entonces debe retornar True"""
        assert msg.is_from_user() is True

        """role='user' entonces debe retornar False"""
        assert msg.is_from_assistant() is False

    def test_create_valid_assistant_message(self):
        """llamamos la clase ChatMessage con role='assistant'"""
        msg = ChatMessage(
            id=2,
            session_id="abc123",
            role="assistant",
            message="Hi!",
            timestamp=datetime.now(),
        )
        """role='assistant' entonces debe retornar True"""
        assert msg.is_from_assistant() is True

        """role='assistant' entonces debe retornar False"""
        assert msg.is_from_user() is False

    def test_invalid_role(self):
        """llamamos la clase ChatMessage con role='admin'
        ese rol no es válido, esperamos ValueError"""
        with pytest.raises(ValueError, match="Rol must be"):
            ChatMessage(
                id=1,
                session_id="abc123",
                role="admin",
                message="Hello",
                timestamp=datetime.now(),
            )

    def test_empty_message(self):
        """llamamos la clase ChatMessage con message=''
        esperamos que __post_init__ lance ValueError"""
        with pytest.raises(ValueError, match="Message cannot be empty"):
            ChatMessage(
                id=1,
                session_id="abc123",
                role="user",
                message="",
                timestamp=datetime.now(),
            )

    def test_empty_session_id(self):
        """llamamos la clase ChatMessage con session_id=''
        esperamos que __post_init__ lance ValueError"""
        with pytest.raises(ValueError, match="Session id cannot be empty"):
            ChatMessage(
                id=1,
                session_id="",
                role="user",
                message="Hello",
                timestamp=datetime.now(),
            )


class TestChatContext:

    def _make_message(self, role, text):
        """método helper que llama la clase ChatMessage
        para crear mensajes de prueba sin repetir código"""
        return ChatMessage(
            id=1, session_id="abc123", role=role, message=text, timestamp=datetime.now()
        )

    def test_get_recent_messages_respects_limit(self):
        """llamamos _make_message 10 veces para crear 10 mensajes
        _make_message internamente llama la clase ChatMessage"""
        messages = [self._make_message("user", f"msg {i}") for i in range(10)]

        """llamamos la clase ChatContext con max_messages=6"""
        context = ChatContext(messages=messages, max_messages=6)

        """llamamos el método get_recent_messages() de ChatContext
        debe retornar solo 6 mensajes aunque haya 10"""
        assert len(context.get_recent_messages()) == 6

    def test_get_recent_messages_returns_last(self):
        """llamamos _make_message 10 veces, crea mensajes del msg 0 al msg 9"""
        messages = [self._make_message("user", f"msg {i}") for i in range(10)]

        """llamamos la clase ChatContext"""
        context = ChatContext(messages=messages)

        """llamamos el método get_recent_messages() de ChatContext
        el último mensaje debe ser el más reciente: msg 9"""
        assert context.get_recent_messages()[-1].message == "msg 9"

    def test_format_for_prompt(self):
        """llamamos _make_message 2 veces para crear la conversación
        _make_message internamente llama la clase ChatMessage"""
        messages = [
            self._make_message("user", "Do you have Nike size 42?"),
            self._make_message("assistant", "Yes, we have several options."),
        ]
        """llamamos la clase ChatContext"""
        context = ChatContext(messages=messages)

        """llamamos el método format_for_prompt() de ChatContext
        debe construir el string con el historial de conversación"""
        result = context.format_for_prompt()

        """verificamos que el string tiene el formato correcto"""
        assert (
            result
            == "User: Do you have Nike size 42?\nAssistant: Yes, we have several options."
        )
