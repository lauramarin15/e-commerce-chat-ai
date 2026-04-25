"""
Módulo del servicio de IA usando Google Gemini.

Implementa la integración con la API de Google Gemini para generar
respuestas contextuales basadas en el catálogo de productos y el
historial de conversación del usuario.
"""

import os
import google.generativeai as genai
from src.domain.entities import Product, ChatContext
from src.domain.exceptions import ChatServiceError


class GeminiService:
    """Servicio de IA usando Google Gemini.
    Gestiona la comunicación con la API de Google Gemini para generar
    respuestas inteligentes sobre productos de zapatos, usando el
    catálogo disponible y el historial de conversación como contexto.

    Atributos:
        model (GenerativeModel): Instancia del modelo Gemini configurado.

    Ejemplo:
        >>> service = GeminiService()
        >>> response = await service.generate_response(
        ...     user_message="Busco zapatillas Nike",
        ...     products=products,
        ...     context=context,
        ... )
    """

    def __init__(self):
        """Carga la API key y configura el modelo.
        Raises:
            ValueError: Si la variable de entorno GEMINI_API_KEY
                        no está definida.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrada en variables de entorno.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    async def generate_response(
        self,
        user_message: str,
        products: list[Product],
        context: ChatContext,
    ) -> str:
        """Genera una respuesta usando Gemini.
        Construye un prompt con el catálogo de productos, el historial
        de conversación y el mensaje actual del usuario, luego llama
        a la API de Gemini para generar una respuesta coherente.

        Args:
            user_message (str): Mensaje actual del usuario.
            products (list[Product]): Lista de productos del catálogo.
            context (ChatContext): Contexto con el historial de conversación.

        Retorna:
            str: Respuesta generada por el modelo de IA.

        Raises:
            ChatServiceError: Si ocurre un error al llamar a la API de Gemini.

        Ejemplo:
            >>> response = await service.generate_response(
            ...     user_message="¿Tienen Nike talla 42?",
            ...     products=products,
            ...     context=context,
            ... )
            >>> print(response)
            "Sí, tenemos Nike Air Max 90 en talla 42..."
        """
        try:
            # 1. Formatear productos y contexto
            products_text = self.format_products_info(products)
            context_text = context.format_for_prompt()

            # 2. Construir prompt completo
            prompt = f"""Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
                        Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

                        PRODUCTOS DISPONIBLES:
                        {products_text}

                        INSTRUCCIONES:
                        - Sé amigable y profesional
                        - Usa el contexto de la conversación anterior
                        - Recomienda productos específicos cuando sea apropiado
                        - Menciona precios, tallas y disponibilidad
                        - Si no tienes información, sé honesto

                        HISTORIAL DE CONVERSACIÓN:
                        {context_text}

                        Usuario: {user_message}

                        Asistente:"""

            # 3. Llamar a Gemini
            response = await self.model.generate_content_async(prompt)

            # 4. Retornar respuesta
            return response.text

        except Exception as e:
            raise ChatServiceError(f"Error al llamar a Gemini: {str(e)}") from e

    def format_products_info(self, products: list[Product]) -> str:
        """Convierte la lista de productos a texto legible para el prompt.

        Args:
            products (list[Product]): Lista de productos a formatear.

        Retorna:
            str: Texto con el catálogo formateado, o mensaje indicando
                 que no hay productos disponibles.

        Ejemplo:
            >>> text = service.format_products_info(products)
            >>> print(text)
            "- Air Max 90 | Nike | $120.00 | Talla: 42 | En stock (stock: 15)"
        """
        if not products:
            return "No hay productos disponibles."

        lines = []
        for p in products:
            availability = "En stock" if p.is_available() else "Agotado"
            lines.append(
                f"- {p.name} | {p.brand} | ${p.price:.2f} | Talla: {p.size} | {availability} (stock: {p.stock})"
            )
        return "\n".join(lines)
