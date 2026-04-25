# E-Commerce Chat AI

API REST de e-commerce de zapatos con asistente de IA integrado, construido con Clean Architecture.

---

## Descripción

Plataforma de e-commerce especializada en zapatos que combina una API REST completa con un chat inteligente powered by Google Gemini AI. El asistente ayuda a los clientes a encontrar el producto perfecto basándose en sus necesidades, presupuesto y preferencias.

---

## Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.11 | Lenguaje principal |
| FastAPI | 0.104.1 | Framework web |
| SQLAlchemy | 2.0.23 | ORM |
| SQLite | — | Base de datos |
| Google Gemini AI | 0.3.1 | IA generativa |
| Docker | — | Containerización |
| Pytest | 7.4.3 | Testing |

---

## Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE (Frontend)                       │
│                  (Navegador, Postman, etc.)                 │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Requests
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              INFRASTRUCTURE LAYER                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI (main.py)                                   │  │
│  │  - Endpoints HTTP                                    │  │
│  │  - Validación de requests                            │  │
│  │  - Serialización de responses                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Repositories (SQLAlchemy)                           │  │
│  │  - product_repository.py                             │  │
│  │  - chat_repository.py                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  External Services                                   │  │
│  │  - gemini_service.py (Google Gemini AI)              │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              APPLICATION LAYER                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Services (Casos de Uso)                             │  │
│  │  - product_service.py                                │  │
│  │  - chat_service.py                                   │  │
│  │  Orquesta: Repositorios + Servicios Externos         │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  DTOs (Data Transfer Objects)                        │  │
│  │  - Validación con Pydantic                           │  │
│  │  - Transformación de datos                           │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────────┐
│              DOMAIN LAYER                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Entities (Lógica de Negocio)                        │  │
│  │  - Product                                           │  │
│  │  - ChatMessage                                       │  │
│  │  - ChatContext                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Repositories (Interfaces)                           │  │
│  │  - IProductRepository                                │  │
│  │  - IChatRepository                                   │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Exceptions (Excepciones del Dominio)                │  │
│  │  - ProductNotFoundError                              │  │
│  │  - InvalidProductDataError                           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

##  Instalación

### Requisitos previos
- Python 3.10+
- Docker y Docker Compose
- API Key de Google Gemini — obtén una gratis en [aistudio.google.com](https://aistudio.google.com)

### Pasos

**1. Clonar repositorio**
```bash
git clone <tu-repo>
cd e-commerce-chat-ai
```

**2. Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

**3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**4. Configurar variables de entorno**
```bash
cp .env.example .env
```

Edita el archivo `.env`:
```env
GEMINI_API_KEY=tu_api_key_aqui
DATABASE_URL=sqlite:///./data/ecommerce_chat.db
```

**5. Ejecutar con Docker**
```bash
docker-compose up --build
```

---

## Uso

| Recurso | URL |
|---|---|
| API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |

---

## Endpoints

### Productos
```bash
# Listar todos los productos
GET /products

# Obtener producto por ID
GET /products/{id}
```

### Chat
```bash
# Enviar mensaje al asistente
POST /chat
Body: {
    "session_id": "abc123",
    "message": "Busco zapatillas Nike talla 42"
}

# Obtener historial de sesión
GET /chat/history/{session_id}

# Eliminar historial
DELETE /chat/history/{session_id}
```


---

## Tests

```bash
# Correr todos los tests
pytest tests/ -v

# Con reporte de coverage
pytest tests/ -v --cov=src
```

---

## Docker

```bash
# Construir y correr
docker-compose up --build

# Correr en background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## Estructura del proyecto

```
e-commerce-chat-ai/
│
├── src/
│   ├── __init__.py
│   ├── config.py                      # Configuración global
│   │
│   ├── domain/                        # 🔷 CAPA DE DOMINIO
│   │   ├── __init__.py
│   │   ├── entities.py                # Product, ChatMessage, ChatContext
│   │   ├── repositories.py            # IProductRepository, IChatRepository
│   │   └── exceptions.py              # Excepciones del dominio
│   │
│   ├── application/                   # 🔶 CAPA DE APLICACIÓN
│   │   ├── __init__.py
│   │   ├── dtos.py                    # DTOs con Pydantic
│   │   ├── product_service.py         # Servicio de productos
│   │   └── chat_service.py            # Servicio de chat
│   │
│   └── infrastructure/                # 🔸 CAPA DE INFRAESTRUCTURA
│       ├── __init__.py
│       │
│       ├── api/                       # FastAPI
│       │   ├── __init__.py
│       │   └── main.py                # Aplicación FastAPI
│       │
│       ├── db/                        # Base de Datos
│       │   ├── __init__.py
│       │   ├── database.py            # Configuración SQLAlchemy
│       │   ├── models.py              # Modelos ORM
│       │   └── init_data.py           # Datos iniciales
│       │
│       ├── repositories/              # Implementaciones
│       │   ├── __init__.py
│       │   ├── product_repository.py
│       │   └── chat_repository.py
│       │
│       └── llm_providers/             # Proveedores de IA
│           ├── __init__.py
│           └── gemini_service.py
│
├── tests/                             # Tests
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
│
├── data/                              # Base de datos (se crea automáticamente)
│   └── ecommerce_chat.db
│
├── .env                               # Variables de entorno (NO versionar)
├── .env.example                       # Ejemplo de variables
├── .gitignore
├── .dockerignore
│
├── Dockerfile                         # Imagen Docker
├── docker-compose.yml                 # Orquestación
│
├── requirements.txt                   # Dependencias Python
├── pyproject.toml                     # Configuración pytest
│
└── README.md                          # Documentación
```

## Autor
Laura Marin - Universidad EAFIT