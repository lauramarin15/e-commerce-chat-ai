from sqlalchemy.orm import Session
from src.domain.repositories import IProductRepository
from src.domain.entities import Product
from src.infrastructure.db.models import ProductModel


class SQLProductRepository(IProductRepository):
    """Implementación concreta de IProductRepository usando SQLAlchemy."""

    def __init__(self, db: Session):
        """Recibe la sesión de base de datos inyectada."""
        self.db = db
        
    def _model_to_entity(self, model: ProductModel) -> Product:
        """Convierte un modelo ORM a entidad del dominio."""
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description,
        )

    def _entity_to_model(self, entity: Product) -> ProductModel:
        """Convierte una entidad del dominio a modelo ORM."""
        return ProductModel(
            id=entity.id,
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description,
        )

    def get_all(self) -> list[Product]:
        """Retorna todos los productos."""
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_id(self, product_id: int) -> Product | None:
        """Busca un producto por ID."""
        model = self.db.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str) -> list[Product]:
        """Filtra productos por marca."""
        models = self.db.query(ProductModel).filter(
            ProductModel.brand == brand
        ).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_category(self, category: str) -> list[Product]:
        """Filtra productos por categoría."""
        models = self.db.query(ProductModel).filter(
            ProductModel.category == category
        ).all()
        return [self._model_to_entity(m) for m in models]

    def save(self, product: Product) -> Product:
        """Crea o actualiza un producto según tenga ID o no."""
        if product.id:
            model = self.db.query(ProductModel).filter(
                ProductModel.id == product.id
            ).first()
            model.name = product.name
            model.brand = product.brand
            model.category = product.category
            model.size = product.size
            model.color = product.color
            model.price = product.price
            model.stock = product.stock
            model.description = product.description
        else:
            model = self._entity_to_model(product)
            self.db.add(model)

        self.db.commit()
        self.db.refresh(model)
        return self._model_to_entity(model)

    def delete(self, product_id: int) -> bool:
        """Elimina un producto por ID."""
        model = self.db.query(ProductModel).filter(
            ProductModel.id == product_id
        ).first()
        if not model:
            return False
        self.db.delete(model)
        self.db.commit()
        return True