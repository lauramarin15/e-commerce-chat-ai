from sqlalchemy import create_engine, sessionmake,  declarative_base

URL = sqlite:///./data/ecommerce_chat.db

engine = create_engine(
    URL, connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()

def get_db() -> Generator:
    """Dependency de FastAPI. Crea y cierra la sesión por cada request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Crea todas las tablas al arrancar la aplicación."""
    Base.metadata.create_all(bind=engine)