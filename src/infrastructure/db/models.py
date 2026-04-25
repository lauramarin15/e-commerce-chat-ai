"""
Módulo de modelos ORM de SQLAlchemy.

Define los modelos que mapean las entidades del dominio
a tablas en la base de datos. Cada clase representa una tabla
y cada atributo representa una columna.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from src.infrastructure.db.database import Base


class ProductModel(Base):
    """Representa la tabla products en la base de datos.
    Atributos:
        id (int): Clave primaria autoincremental.
        name (str): Nombre del producto, obligatorio.
        brand (str): Marca del producto.
        category (str): Categoría, indexada para búsquedas rápidas.
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio en dólares.
        stock (int): Unidades disponibles en inventario.
        description (str): Descripción larga del producto.
    """

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    brand = Column(String(100))  # marca
    category = Column(String(100), index=True)  # indexado para búsquedas por categoría
    size = Column(String(20))  # talla
    color = Column(String(50))  # color
    price = Column(Float)  # precio
    stock = Column(Integer)  # cantidad disponible
    description = Column(Text)  # descripcion


class ChatMemoryModel(Base):
    """Representa la tabla chat_memory en la base de datos.
    Almacena el historial de mensajes de todas las sesiones de chat.
    El session_id está indexado para recuperar el historial rápidamente.

    Attributes:
        id (int): Clave primaria autoincremental.
        session_id (str): Identificador de la sesión, indexado.
        role (str): Rol del emisor, 'user' o 'assistant'.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje, por defecto utcnow.
    """

    __tablename__ = "chat_memory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(
        String(100), index=True
    )  # indexado para busquedas por categoria
    role = Column(String(20))  # 'user' o 'assistant'
    message = Column(Text)  # contenido del mensaje
    timestamp = Column(DateTime, default=datetime.utcnow)  # fecha y hora automática
