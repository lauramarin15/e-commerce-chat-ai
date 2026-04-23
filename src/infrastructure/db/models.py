from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime
from src.infrastructure.db.database.py import Base




class ProductModel(Base):
    """Representa la tabla products en la base de datos."""

    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)       
    brand = Column(String(100))                                 # marca    
    category = Column(String(100), index=True)                  # indexado para búsquedas por categoría
    size = Column(String(20))                                   # talla
    color = Column(String(50))                                  # color 
    price = Column(Float)                                       # precio    
    stock = Column(Integer)                                     # cantidad disponible
    description = Column(Text)                                  # descripcion 

    
class ChatMemoryModel(base):
    """Representa la tabla chat_memory en la base de datos."""

    __tablename__ = "chat_memory"
    
    id = Column(Integer, primary_key=true, autoincrement=True)      
    session_id = Column(String(100), index=True)                #indexado para busquedas por categoria
    role = Column(String(20))                                   # 'user' o 'assistant'
    message = Column(Text)                                      # contenido del mensaje
    timestamp = Column(DateTime, default = datetime.utcnow)     # fecha y hora automática
    