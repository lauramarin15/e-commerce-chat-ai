import os
import google.generativeai as genai
from src.domain.entities import Product, ChatContext
from src.domain.exceptions import ChatServiceError


class GeminiService:
    """Servicio de IA usando Google Gemini."""

    def __init__(self):
        """Carga la API key y configura el modelo."""
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
        """Genera una respuesta usando Gemini."""
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
        """Convierte la lista de productos a texto legible para el prompt."""
        if not products:
            return "No hay productos disponibles."

        lines = []
        for p in products:
            availability = "En stock" if p.is_available() else "Agotado"
            lines.append(
                f"- {p.name} | {p.brand} | ${p.price:.2f} | Talla: {p.size} | {availability} (stock: {p.stock})"
            )
        return "\n".join(lines)