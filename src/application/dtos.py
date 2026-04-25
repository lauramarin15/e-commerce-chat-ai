"""
Módulo de Data Transfer Objects (DTOs).

Define los objetos de transferencia de datos usados para la
comunicación entre la capa de presentación y la capa de aplicación.
Pydantic valida automáticamente los tipos y restricciones.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class ProductDTO(BaseModel):
    """
    DTO para transferir datos de productos.
    Pydantic valida automáticamente los tipos.

    Atributos:
        id (Optional[int]): Identificador único. None para productos nuevos.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoría del producto.
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio en dólares, debe ser mayor a 0.
        stock (int): Cantidad disponible, no puede ser negativa.
        description (str): Descripción detallada del producto.

    Ejemplo:
        >>> dto = ProductDTO(name="Air Max", brand="Nike", price=120, stock=10, ...)
    """

    id: Optional[int] = None
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    description: str

    @validator("price")
    def price_must_be_positive(cls, v):
        """Valida que el precio sea mayor a 0
        Args:
            v (float): Valor del precio a validar.

        Raises:
            ValueError: Si el precio es menor o igual a 0.
        """
        if v <= 0:
            raise ValueError("Price must be greater than 0.")
        return v

    @validator("stock")
    def stock_must_be_non_negative(cls, v):
        """Valida que el stock no sea negativo
        Args:
            v (int): Valor del stock a validar.

        Raises:
            ValueError: Si el stock es negativo.
        """
        if v < 0:
            raise ValueError("Stock cannot be negative.")
        return v

    class Config:
        from_attributes = True  # Permite crear desde objetos ORM


class ChatMessageRequestDTO(BaseModel):
    """DTO para recibir mensajes del usuario
    Valida que el mensaje y el session_id no estén vacíos
    ni contengan solo espacios en blanco.

    Atributos:
        session_id (str): Identificador único de la sesión de chat.
        message (str): Contenido del mensaje del usuario.

    Ejemplo:
        >>> dto = ChatMessageRequestDTO(session_id="abc123", message="Hola")
    """

    session_id: str = Field(min_length=1)
    message: str = Field(min_length=1)

    @validator("message")
    def message_not_empty(cls, v):
        """Valida que el mensaje no esté vacío

        verificamos que el campo no sea solo espacios
        Args:
            v (str): Valor del mensaje a validar.

        Raises:
            ValueError: Si el mensaje contiene solo espacios.
        """
        if not v.strip():
            raise ValueError("Field cannot contain only spaces.")
        return v

    @validator("session_id")
    def session_id_not_empty(cls, v):
        """Valida que session_id no esté vacío"""

        """verificamos que el campo no sea solo espacios
        Args:
            v (str): Valor del session_id a validar 
        Raises:
            ValueError: Si el session_id contiene solo espacios."""

        if not v.strip():
            raise ValueError("Field cannot contain only spaces.")
        return v


class ChatMessageResponseDTO(BaseModel):
    """DTO para enviar respuestas del chat
    Atributos:
        session_id (str): Identificador de la sesión de chat.
        user_message (str): Mensaje original del usuario.
        assistant_message (str): Respuesta generada por la IA.
        timestamp (datetime): Fecha y hora de la respuesta.
    """

    session_id: str
    user_message: str
    assistant_message: str
    timestamp: datetime


class ChatHistoryDTO(BaseModel):
    """DTO para mostrar historial de chat
    Usado en el endpoint GET /chat/history/{session_id} para
    retornar cada mensaje del historial.

    Attributes:
        id (int): Identificador único del mensaje.
        role (str): Rol del emisor, 'user' o 'assistant'.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje.
    """

    id: int
    role: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True
