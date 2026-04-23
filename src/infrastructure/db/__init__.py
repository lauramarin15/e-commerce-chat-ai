from src.infrastructure.database.config import SessionLocal
from src.infrastructure.db.models import ProductModel

def load_initial_data() -> None:
    """Carga productos iniciales si la base de datos está vacía."""
    db = SessionLocal()
    try:
        if db.query(ProductModel).count() > 0:
            return

        products = [
            ProductModel(
                name="Air Max 90",
                brand="Nike",
                category="Running",
                size="42",
                color="Blanco",
                price=120.00,
                stock=15,
                description="Zapatilla clásica de running con amortiguación Air.",
            ),
            ProductModel(
                name="Ultraboost 22",
                brand="Adidas",
                category="Running",
                size="41",
                color="Negro",
                price=180.00,
                stock=10,
                description="Zapatilla de alto rendimiento con tecnología Boost.",
            ),
            ProductModel(
                name="RS-X",
                brand="Puma",
                category="Casual",
                size="43",
                color="Azul",
                price=95.00,
                stock=20,
                description="Zapatilla casual con diseño retro y suela gruesa.",
            ),
            ProductModel(
                name="Chuck Taylor All Star",
                brand="Converse",
                category="Casual",
                size="40",
                color="Negro",
                price=65.00,
                stock=25,
                description="Icónica zapatilla de lona para uso diario.",
            ),
            ProductModel(
                name="Classic Leather",
                brand="Reebok",
                category="Casual",
                size="42",
                color="Blanco",
                price=75.00,
                stock=18,
                description="Zapatilla de cuero clásica y versátil.",
            ),
            ProductModel(
                name="Air Force 1",
                brand="Nike",
                category="Casual",
                size="44",
                color="Blanco",
                price=110.00,
                stock=12,
                description="Zapatilla icónica de baloncesto adaptada al uso casual.",
            ),
            ProductModel(
                name="Stan Smith",
                brand="Adidas",
                category="Formal",
                size="41",
                color="Blanco",
                price=85.00,
                stock=8,
                description="Zapatilla minimalista ideal para looks formales.",
            ),
            ProductModel(
                name="Suede Classic",
                brand="Puma",
                category="Casual",
                size="43",
                color="Verde",
                price=70.00,
                stock=14,
                description="Zapatilla de gamuza con estilo retro urbano.",
            ),
            ProductModel(
                name="Gel-Kayano 29",
                brand="Asics",
                category="Running",
                size="42",
                color="Gris",
                price=160.00,
                stock=9,
                description="Zapatilla de running con máxima estabilidad y soporte.",
            ),
            ProductModel(
                name="Fresh Foam 1080",
                brand="New Balance",
                category="Running",
                size="43",
                color="Azul",
                price=150.00,
                stock=11,
                description="Zapatilla de running con amortiguación premium Fresh Foam.",
            ),
        ]

        # Insertar todos y confirmar
        db.add_all(products)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()