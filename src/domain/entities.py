from dataclasses import dataclass
from typing import Optional
from datetime import datetime

"""
Módulo de entidades del dominio.

Define las entidades principales del negocio: Product, ChatMessage y ChatContext.
Estas clases contienen la lógica de negocio central y son independientes
de cualquier framework o base de datos.
"""

@dataclass
class Product:
   """
    Entidad que representa un producto en el e-commerce.

    Esta clase encapsula la lógica de negocio relacionada con productos,
    incluyendo validaciones de precio, stock y disponibilidad.

    Atributos:
        id (Optional[int]): Identificador único del producto.
        name (str): Nombre del producto.
        brand (str): Marca del producto.
        category (str): Categoría del producto.
        size (str): Talla del producto.
        color (str): Color del producto.
        price (float): Precio en dólares, debe ser mayor a 0.
        stock (int): Cantidad disponible en inventario.
        description (str): Descripción detallada del producto.
    """
    
    id: Optional[int]
    name: str
    brand: str
    category: str
    size: str
    color: str
    price: float
    stock: int
    description: str

    def __post_init__(self):
        """
        Validaciones que se ejecutan después de crear el objeto.
        - price debe ser mayor a 0
        - stock no puede ser negativo
        - name no puede estar vacío
        Lanza ValueError si alguna validación falla
        """
        if self.price <= 0:
            raise ValueError("Price must be bigger than 0.")

        if self.stock < 0:
            raise ValueError("Stock cannot be negative.")

        if not self.name or not self.name.strip():
            raise ValueError("Product name cannot be empty.")

    def is_available(self) -> bool:
        """
        Retorna True si el producto tiene stock disponible
        
        Retorna:
            bool: True si el stock es mayor a 0, False en caso contrario.

        Ejemplo:
            >>> product = Product(name="Air Max", stock=5, price=100, ...)
            >>> product.is_available()
            True
        """
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce el stock del producto
        - Valida que quantity sea positivo
        - Valida que haya suficiente stock
        - Lanza ValueError si no se puede reducir
        
        Args:
            quantity (int): Cantidad a reducir. Debe ser positiva.

        Raises:
            ValueError: Si quantity es negativo o mayor al stock disponible.

        Ejemplo:
            >>> product.reduce_stock(3)
            >>> print(product.stock)
            7
        """
        if quantity <= 0:
            raise ValueError("Quanttity must be bigger than 0")
        if quantity > self.stock:
            raise ValueError("Insufficient stock")
        self.stock -= quantity

    def increase_stock(self, quantity: int) -> None:
        """
        Aumenta el stock del producto
        - Valida que quantity sea positivo
        
        Args:
            quantity (int): Cantidad a aumentar. Debe ser positiva.

        Raises:
            ValueError: Si quantity es negativo o igual a 0.

        Ejemplo:
            >>> product.increase_stock(5)
            >>> print(product.stock)
            15
        """
        if quantity <= 0:
            raise ValueError("The increase must be positive")
        self.stock += quantity


@dataclass
class ChatMessage:
    """
    Entidad que representa un mensaje en el chat.
    
    Almacena un mensaje individual de la conversación, ya sea del
    usuario o del asistente de IA.

    Atributos:
        id (Optional[int]): Identificador único del mensaje.
        session_id (str): Identificador de la sesión de chat.
        role (str): Rol del emisor, debe ser 'user' o 'assistant'.
        message (str): Contenido del mensaje.
        timestamp (datetime): Fecha y hora del mensaje.
    """

    id: Optional[int]
    session_id: str
    role: str  # 'user' o 'assistant'
    message: str
    timestamp: datetime

    def __post_init__(self):
        """
        Implementar validaciones:
        - role debe ser 'user' o 'assistant'
        - message no puede estar vacío
        - session_id no puede estar vacío
        
         Raises:
            ValueError: Si el rol es inválido, el mensaje está vacío
                        o el session_id está vacío.
        """
        if self.role not in ("user", "assistant"):
            raise ValueError("Rol must be 'user' or 'assistant'")
        if not self.message:
            raise ValueError("Message cannot be empty")
        if not self.session_id:
            raise ValueError("Session id cannot be empty")

    def is_from_user(self) -> bool:
        """
        Retorna True si el mensaje es del usuario
        """
        return self.role == "user"

    def is_from_assistant(self) -> bool:
        """
        Retorna True si el mensaje es del asistente
        """
        return self.role == "assistant"


@dataclass
class ChatContext:
    """
    Value Object que encapsula el contexto de una conversación.
    Mantiene los mensajes recientes para dar coherencia al chat.
    Atributos:
        messages (list): Lista de mensajes de la conversación.
        max_messages (int): Número máximo de mensajes a considerar.
        
    """

    messages: list[ChatMessage]
    max_messages: int = 6

    def get_recent_messages(self) -> list[ChatMessage]:
        """
        Retorna los últimos N mensajes (max_messages)
        """
        return self.messages[-self.max_messages :]

    def format_for_prompt(self) -> str:
        """
        Formatea los mensajes para incluirlos en el prompt de IA
        Formato esperado:
        "Usuario: mensaje del usuario
        Asistente: respuesta del asistente
        Usuario: otro mensaje
        ..."
        
        Construye un string con el historial en formato legible
        que la IA puede usar como contexto.

        Retorna:
            str: Historial formateado con roles y mensajes.

        Ejemplo:
            >>> context.format_for_prompt()
            "User: Busco zapatos\\nAssistant: Tenemos varias opciones."

 
        """
        role_label = {"user": "User", "assistant": "Assistant"}
        lines = [
            f"{role_label[msg.role]}: {msg.message}"
            for msg in self.get_recent_messages()
        ]
        return "\n".join(lines)
