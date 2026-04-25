"""
Módulo de interfaces de repositorios del dominio.

Define los contratos que deben cumplir las implementaciones
concretas de los repositorios. Estas interfaces son independientes
de cualquier base de datos o framework de persistencia.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.entities import Product, ChatMessage


class IProductRepository(ABC):
    """
    Interface que define el contrato para acceder a productos.
    Las implementaciones concretas estarán en la capa de infraestructura.

    Ejemplo:
        >>> class SQLProductRepository(IProductRepository):
        ...     def get_all(self):
        ...         return db.query(ProductModel).all()
    """

    @abstractmethod
    def get_all(self) -> List[Product]:
        """
        Define el método para obtener todos los productos
        Retorna:
            list[Product]: Lista de todas las entidades Product.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        """
        Define el método para obtener un producto por ID
        Retorna None si no existe

        Args:
            product_id (int): ID del producto a buscar.

        Retorna:
            Optional[Product]: La entidad Product si existe, None si no.

        """
        pass

    @abstractmethod
    def get_by_brand(self, brand: str) -> List[Product]:
        """Obtiene productos de una marca específica
        Args:
            brand (str): Nombre de la marca a filtrar.

        Retorna:
            list[Product]: Lista de productos de esa marca.
        """
        pass

    @abstractmethod
    def get_by_category(self, category: str) -> List[Product]:
        """Obtiene productos de una categoría específica
        Args:
            category (str): Nombre de la categoría a filtrar.

        Retorna:
            list[Product]: Lista de productos de esa categoría.
        """
        pass

    @abstractmethod
    def save(self, product: Product) -> Product:
        """
        Guarda o actualiza un producto
        Si tiene ID, actualiza. Si no tiene ID, crea uno nuevo
        Retorna el producto guardado (con ID asignado si es nuevo)
        Args:
            product (Product): Entidad a persistir.

        Retorna:
            Product: La entidad persistida con su ID asignado.
        """
        pass

    @abstractmethod
    def delete(self, product_id: int) -> bool:
        """
        Elimina un producto por ID
         Retorna True si se eliminó, False si no existía
          Args:
             product_id (int): ID del producto a eliminar.

         Retorna:
             bool: True si fue eliminado, False si no existía.
        """
        pass


class IChatRepository(ABC):
    """
    Interface para gestionar el historial de conversaciones.
    """

    @abstractmethod
    def save_message(self, message: ChatMessage) -> ChatMessage:
        """
        Guarda un mensaje en el historial
        Retorna el mensaje guardado con su ID
        Args:
            message (ChatMessage): Entidad a guardar.

        Retorna:
            ChatMessage: La entidad guardada con su ID asignado.
        """
        pass

    @abstractmethod
    def get_session_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Obtiene el historial completo de una sesión
        Si limit está definido, retorna solo los últimos N mensajes
        Los mensajes deben estar en orden cronológico (más antiguos primero)

        Args:
            session_id (str): ID de la sesión a consultar.
            limit (int | None): Límite de mensajes. Sin límite si es None.

        Retorna:
            list[ChatMessage]: Lista de mensajes en orden cronológico.
        """
        pass

    @abstractmethod
    def delete_session_history(self, session_id: str) -> int:
        """
         Elimina todo el historial de una sesión
        Retorna la cantidad de mensajes eliminados

        Args:
            session_id (str): ID de la sesión a limpiar.

        Retorna:
            int: Número de mensajes eliminados.
        """
        pass

    @abstractmethod
    def get_recent_messages(self, session_id: str, count: int) -> List[ChatMessage]:
        """
        TObtiene los últimos N mensajes de una sesión
        Crucial para mantener el contexto conversacional
        Retorna en orden cronológico

        Args:
            session_id (str): ID de la sesión a consultar.
            count (int): Número de mensajes a retornar.

        Retorna:
            list[ChatMessage]: Últimos N mensajes en orden cronológico.
        """
        pass
