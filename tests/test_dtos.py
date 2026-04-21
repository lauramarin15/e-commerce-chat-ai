import pytest
from pydantic import ValidationError
from src.application.dtos import ProductDTO, ChatMessageRequestDTO


class TestProductDTO:
    
    def test_price_greater_than_zer(self):
        """price=0 debe lanzar ValidationError
        pydantic lo checa automáticamente"""
        with pytest.raises(ValidationError):
            ProductDTO(
                id=1, 
                name="Air Max", 
                brand="Nike", 
                category="Running",
                size="42", 
                color="White",
                price=0, 
                stock=10, 
                description="..."
            )
            
    def test_stock_cannot_be_negative(self):
        """stock=-1 debe lanzar ValidationError
        pydantic lo checa automáticamente"""
        with pytest.raises(ValidationError):
            ProductDTO(
                id=1, 
                name="Air Max", 
                brand="Nike",
                category="Running",
                size="42", 
                color="White",
                price=150.0, 
                stock=-1, 
                description="..."
            )
            
class TestChatMessageRequestDTO:
    
    def test_message_cannot_be_empty(self):
        """messege no puede estar vacio
        debe lanzar validation error"""
        with pytest.raises(ValidationError):
            ChatMessageRequestDTO(
             
                session_id="abc123",
              
                message="",
                
            )
            
    def test_session_ID_cannot_be_empty(self):
        """messege no puede estar vacio
        debe lanzar validation error"""
        with pytest.raises(ValidationError):
            ChatMessageRequestDTO(
               
                session_id="",
                
                message="abc123",
                
            )
    
    