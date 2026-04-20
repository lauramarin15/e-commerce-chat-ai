"""
Excepciones específicas del dominio.
Representan errores de negocio, no errores técnicos.
"""


class ProductNotFoundError(Exception):
    """
    Se lanza cuando se busca un producto que no existe.
    - Debe aceptar un product_id opcional
    - Mensaje por defecto: "Producto no encontrado"
    - Si se pasa product_id: "Producto con ID {product_id} no encontrado"
    """

    def __init__(self, product_id: int = None):
        if product_id:
            self.message = f"Product with ID {product_id} not found"
        else:
            self.message = "Product not found"
        super().__init__(self.message)


class InvalidProductDataError(Exception):
    """
    Se lanza cuando los datos de un producto son inválidos.
    - Debe aceptar un mensaje personalizado
    - Mensaje por defecto: "Datos de producto inválidos"
    """

    def __init__(self, message: str = "Invalid product data"):
        self.message = message

        super().__init__(self.message)


class ChatServiceError(Exception):
    """
    Se lanza cuando hay un error en el servicio de chat.
    Implementa el constructor:
    - Debe aceptar un mensaje personalizado
    - Mensaje por defecto: "Error en el servicio de chat"
    """

    def __init__(self, message: str = "Chat service error"):
        self.message = message

        super().__init__(self.message)
