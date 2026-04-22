from typing import List
from src.domain.repositories import IProductRepository
from src.domain.entities import Product
from src.domain.exceptions import ProductNotFoundError
from src.application.dtos.product_dto import ProductRequestDTO


class ProductService:
    """Gestión de productos de la tienda."""

    def __init__(self, product_repository: IProductRepository):
        """Recibe el repositorio por inyección de dependencias."""
        self._product_repo = product_repository

    def get_all_products(self) -> List[Product]:
        """Retorna todos los productos."""
        return self._product_repo.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        """Busca por ID. Lanza ProductNotFoundError si no existe."""
        product = self._product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Producto con id {product_id} no encontrado.")
        return product

    def search_products(self, filters: dict) -> List[Product]:
        """Filtra por brand o color. Sin filtros retorna todos."""
        brand = filters.get("brand")
        category = filters.get("color")

        if brand:
            return self._product_repo.get_by_brand(brand)
        if color:
            return self._product_repo.get_by_color(color)

        return self._product_repo.get_all()

    def create_product(self, product_dto: ProductRequestDTO) -> Product:
        """Convierte el DTO a entidad y la persiste."""
        product = Product(
            id=None,
            name=product_dto.name,
            brand=product_dto.brand,
            category=product_dto.category,
            size=product_dto.size,
            color=product_dto.color,
            price=product_dto.price,
            stock=product_dto.stock,
            description=product_dto.description,
        )
        return self._product_repo.save(product)

    def update_product(self, product_id: int, product_dto: ProductRequestDTO) -> Product:
        """Valida que exista y actualiza con los nuevos datos."""
        existing = self._product_repo.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError(f"Producto con id {product_id} no encontrado.")

        updated_product = Product(
            id=product_id,
            name=product_dto.name,
            brand=product_dto.brand,
            category=product_dto.category,
            size=product_dto.size,
            color=product_dto.color,
            price=product_dto.price,
            stock=product_dto.stock,
            description=product_dto.description,
        )
        return self._product_repo.save(updated_product)

    def delete_product(self, product_id: int) -> bool:
        """Valida que exista y elimina el producto."""
        existing = self._product_repo.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError(f"Producto con id {product_id} no encontrado.")
        return self._product_repo.delete(product_id)

    def get_available_products(self) -> List[Product]:
        """Retorna solo productos con stock disponible."""
        all_products = self._product_repo.get_all()
        return [p for p in all_products if p.is_available()]