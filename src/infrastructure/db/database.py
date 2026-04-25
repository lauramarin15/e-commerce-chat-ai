"""
Módulo de configuración de la base de datos.

Configura SQLAlchemy con el motor de conexión, la fábrica de sesiones
y la clase base para los modelos ORM. También provee las funciones
necesarias para inicializar la base de datos y gestionar sesiones.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

# URL de conexión a SQLite
URL = "sqlite:///./data/ecommerce_chat.db"

# Motor de conexión a la base de datos
engine = create_engine(
    URL,
    connect_args={"check_same_thread": False},
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Clase base para modelos ORM
Base = declarative_base()


def get_db() -> Generator:
    """Dependency de FastAPI. Crea y cierra la sesión por cada request.
    Crea una sesión por cada request HTTP y la cierra automáticamente
    al finalizar, incluso si ocurre un error.

    Yields:
        Session: Sesión activa de SQLAlchemy lista para usar.

    Ejemplo:
        >>> @app.get("/products")
        ... def get_products(db: Session = Depends(get_db)):
        ...     return db.query(ProductModel).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Crea todas las tablas al arrancar la aplicación.
    Lee todos los modelos registrados que heredan de Base y crea
    sus tablas en la base de datos si no existen todavía.

    Ejemplo
        >>> init_db()
        >>> # Todas las tablas están creadas y listas para usar
    """
    Base.metadata.create_all(bind=engine)
