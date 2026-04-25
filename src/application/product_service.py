"""
Módulo del servicio de aplicación para productos.

Orquesta las operaciones de negocio relacionadas con productos,
usando el repositorio inyectado para acceder a los datos.
"""

from typing import List

from src.application.dtos import ProductDTO
from src.domain.entities import Product
from src.domain.exceptions import ProductNotFoundError
from src.domain.repositories import IProductRepository


class ProductService:
    """Gestión de productos de la tienda.
     Atributos:
        _product_repo (IProductRepository): Repositorio de productos inyectado.

    Ejemplo:
        >>> repo = SQLProductRepository(db)
        >>> service = ProductService(repo)
        >>> products = service.get_all_products()
    """

    def __init__(self, product_repository: IProductRepository):
        """Recibe el repositorio por inyección de dependencias.
        Args:
            product_repository (IProductRepository): Implementación
                concreta del repositorio de productos.
        """
        self._product_repo = product_repository

    def get_all_products(self) -> List[Product]:
        """Retorna todos los productos.
        Retorna:
            list[Product]: Lista de entidades Product. Puede ser vacía.
        """
        return self._product_repo.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        """Busca por ID. Lanza ProductNotFoundError si no existe.
        Args:
            product_id (int): ID del producto a buscar.

        Retorna:
            Product: La entidad Product encontrada.

        Raises:
            ProductNotFoundError: Si no existe un producto con ese ID.

        Ejemplo:
            >>> product = service.get_product_by_id(1)
            >>> print(product.name)
            "Air Max 90"
        """
        product = self._product_repo.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(f"Producto con id {product_id} no encontrado.")
        return product

    def search_products(self, filters: dict) -> List[Product]:
        """Filtra por brand o color. Sin filtros retorna todos.
        Args:
            filters (dict): Diccionario con criterios opcionales.
                            Claves soportadas: 'brand', 'category'.

        Retorna:
            list[Product]: Lista de productos que coinciden con los filtros.

        Ejemplo:
            >>> products = service.search_products({"brand": "Nike"})
        """
        brand = filters.get("brand")
        category = filters.get("color")

        if brand:
            return self._product_repo.get_by_brand(brand)
        if color:
            return self._product_repo.get_by_color(color)

        return self._product_repo.get_all()

    def create_product(self, product_dto: ProductDTO) -> Product:
        """Convierte el DTO a entidad y la persiste.
         Args:
            product_dto (ProductDTO): DTO con los datos del nuevo producto.

        Retorna:
            Product: La entidad Product recién creada con su ID asignado.

        Ejemplo:
            >>> dto = ProductDTO(name="Air Max", price=120, ...)
            >>> product = service.create_product(dto)
            >>> print(product.id)
            1
        """
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

    def update_product(self, product_id: int, product_dto: ProductDTO) -> Product:
        """Valida que exista y actualiza con los nuevos datos.
        Args:
            product_id (int): ID del producto a actualizar.
            product_dto (ProductDTO): DTO con los datos actualizados.

        Retorna:
            Product: La entidad Product actualizada.

        Raises:
            ProductNotFoundError: Si no existe un producto con ese ID.
        """
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
        """Valida que exista y elimina el producto.
        Args:
            product_id (int): ID del producto a eliminar.

        Retorna:
            bool: True si fue eliminado correctamente.

        Raises:
            ProductNotFoundError: Si no existe un producto con ese ID.
        """
        existing = self._product_repo.get_by_id(product_id)
        if not existing:
            raise ProductNotFoundError(f"Producto con id {product_id} no encontrado.")
        return self._product_repo.delete(product_id)

    def get_available_products(self) -> List[Product]:
        """Retorna solo productos con stock disponible.
        Retorna:
           list[Product]: Lista de productos donde is_available() es True.
        """
        all_products = self._product_repo.get_all()
        return [p for p in all_products if p.is_available()]
