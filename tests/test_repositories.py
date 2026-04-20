import pytest
from src.domain.repositories import IProductRepository, IChatRepository


class TestIProductRepository:

    def test_cannot_instantiate_directly(self):
        """IProductRepository no puede instanciarse directamente"""
        with pytest.raises(TypeError):
            IProductRepository()


class TestIChatRepository:

    def test_cannot_instantiate_directly(self):
        """IChatRepository no puede instanciarse directamente"""
        with pytest.raises(TypeError):
            IChatRepository()