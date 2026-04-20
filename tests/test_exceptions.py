import pytest
from src.domain.exceptions import ProductNotFoundError, InvalidProductDataError, ChatServiceError

class TestProductNotFoundError:
    
    def test_notfound(self):
        """creamos el error sin pasar product_id
        debe usar el mensaje por defecto"""
        error = ProductNotFoundError()
        """verificamos que el mensaje por defecto es correcto"""
        assert error.message == "Product not found"
        
    def test_message_id_notfound(self):
        """creamos el error pasando product_id=42
        debe construir un mensaje con el ID"""
        error = ProductNotFoundError(product_id=42)
        """verificamos que el mensaje contiene el ID"""
        assert error.message == "Product with ID 42 not found" 

class TestInvalidProductDataError:

    def test_default_message(self):
        """creamos el error sin pasar mensaje
        debe usar el mensaje por defecto"""
        error = InvalidProductDataError()
        """verificamos que el mensaje por defecto es correcto"""
        assert error.message == "Invalid product data"

    def test_custom_message(self):
        """creamos el error pasando un mensaje personalizado
        debe reemplazar el mensaje por defecto"""
        error = InvalidProductDataError("Price cannot be negative")
        """verificamos que el mensaje personalizado se guardó correctamente"""
        assert error.message == "Price cannot be negative"


class TestChatServiceError:

    def test_default_message(self):
        """creamos el error sin pasar mensaje
        debe usar el mensaje por defecto"""
        error = ChatServiceError()
        """verificamos que el mensaje por defecto es correcto"""
        assert error.message == "Chat service error"

    def test_custom_message(self):
        """creamos el error pasando un mensaje personalizado
        debe reemplazar el mensaje por defecto"""
        error = ChatServiceError("Could not connect to AI")
        """verificamos que el mensaje personalizado se guardó correctamente"""
        assert error.message == "Could not connect to AI"