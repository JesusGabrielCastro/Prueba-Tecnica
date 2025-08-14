# Sistema de Gestión de Bibliotecas - Backend

## Descripción

API REST desarrollada con FastAPI para gestionar múltiples bibliotecas, sus miembros, inventario de libros y sistema de préstamos. El sistema permite administrar de manera integral las operaciones de bibliotecas con un diseño modular y escalable.

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para crear APIs
- **SQLAlchemy**: ORM para Python
- **SQLite**: Base de datos (archivo: `sistema_bibliotecas.db`)
- **Pydantic**: Validación de datos y serialización
- **Uvicorn**: Servidor ASGI

## Estructura del Proyecto

```
backend/
├── __init__.py 
├── main.py                     # Punto de entrada de la aplicación
├── requirements.txt            # Dependencias del proyecto
├── sistema_bibliotecas.db      # Base de datos SQLite
├── database/
│   ├── __init__.py
│   ├── db.py                   # Configuración de base de datos
│   └── models.py               # Modelos de datos (SQLAlchemy)
├── models/
│   ├── __init__.py
│   └── schemas.py              # Esquemas Pydantic para validación
├── repositories/
│   ├── __init__.py
│   └── biblioteca_repository.py # Repositorio de bibliotecas
└── services/
    ├── __init__.py
    ├── main.py                 # Router principal
    └── routes/
        ├── __init__.py
        ├── biblioteca_service.py   # Endpoints de bibliotecas
        ├── libro_service.py        # Endpoints de libros
        ├── miembro_service.py      # Endpoints de miembros
        └── prestamo_service.py     # Endpoints de préstamos
```

## Modelos de Datos

### Biblioteca
- Código de biblioteca (ID único)
- Nombre de la institución
- Dirección de sede
- Teléfono de contacto
- Correo del administrador
- Estado activo/inactivo

### Miembro
- Número de miembro (ID único)
- Nombres completos
- Documento de identidad
- Información de contacto
- Límite de préstamos (por defecto: 3)
- Asociación a biblioteca

### Libro
- Código de libro (ID único)
- Título, autor, editorial
- Año de publicación
- Categoría/tema
- Estado de conservación
- Cantidad disponible/total
- Ubicación en estante

### Préstamo
- ID de préstamo
- Relación miembro-libro
- Fechas de solicitud, límite y devolución
- Estado (Activo, Devuelto, Vencido)
- Sistema de multas

## Endpoints de la API

### Bibliotecas (`/bibliotecas`)
- `POST /` - Crear nueva biblioteca
- `GET /` - Listar todas las bibliotecas
- `GET /{codigo_biblioteca}` - Obtener biblioteca específica
- `PUT /{codigo_biblioteca}` - Actualizar biblioteca
- `DELETE /{codigo_biblioteca}` - Eliminar biblioteca

### Libros (`/libros`)
- `POST /` - Agregar nuevo libro
- `GET /bibliotecas/{codigo_biblioteca}/libros` - Listar libros por biblioteca
- `GET /buscar` - Buscar libros por título, autor o categoría
- `PUT /{codigo_libro}` - Actualizar información del libro
- `DELETE /{codigo_libro}` - Eliminar libro

### Miembros (`/miembros`)
- `POST /` - Registrar nuevo miembro
- `GET /bibliotecas/{codigo_biblioteca}/miembros` - Listar miembros por biblioteca
- `PUT /{numero_miembro}` - Actualizar información del miembro
- `DELETE /{numero_miembro}` - Eliminar miembro

### Préstamos (`/prestamos`)
- `POST /` - Crear nuevo préstamo
- `GET /miembros/{numero_miembro}/prestamos` - Historial de préstamos por miembro
- `GET /bibliotecas/{codigo_biblioteca}/prestamos-activos` - Préstamos activos por biblioteca
- `PUT /{id_prestamo}/devolver` - Registrar devolución de libro
- `DELETE /{id_prestamo}` - Eliminar registro de préstamo

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd Punto_3/backend
   ```

2. **Crear entorno virtual (recomendado)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   uvicorn main:app --reload
   ```
   o de otra manera
   ```bash
   fastapi run main.py
   ```

5. **Acceder a la API**
   - API: http://localhost:8000
   - Documentación interactiva: http://localhost:8000/docs
   - Documentación alternativa: http://localhost:8000/redoc

## Funcionalidades Destacadas

### Gestión Integral
- Administración completa de múltiples bibliotecas
- Control de inventario con disponibilidad en tiempo real
- Sistema de membresías con límites personalizables

### Sistema de Préstamos
- Validación automática de disponibilidad
- Control de fechas límite y vencimientos
- Cálculo automático de multas por retraso
- Historial completo de transacciones

### Búsqueda Avanzada
- Búsqueda de libros por múltiples criterios
- Filtros por biblioteca, categoría y estado
- Consultas optimizadas con SQLAlchemy

### Validación de Datos
- Esquemas Pydantic para entrada y salida
- Validación automática de tipos y formatos
- Manejo de errores con códigos HTTP apropiados

## Base de Datos

El sistema utiliza SQLite con las siguientes características:
- Base de datos relacional con integridad referencial
- Relaciones bien definidas entre entidades
- Índices para optimizar consultas frecuentes
- Soporte para transacciones ACID

## CORS y Middleware

La API está configurada con CORS habilitado para permitir acceso desde cualquier origen, facilitando la integración con aplicaciones frontend.

## Documentación de la API

FastAPI genera automáticamente documentación interactiva disponible en:
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

Esta documentación incluye:
- Descripción detallada de todos los endpoints
- Esquemas de request/response
- Posibilidad de probar la API directamente
- Ejemplos de uso

## Desarrollo y Extensión

El código está estructurado siguiendo principios de arquitectura limpia:
- **Separación de responsabilidades**: Modelos, servicios y controladores separados
- **Modularidad**: Cada entidad tiene su propio módulo de servicios
- **Extensibilidad**: Fácil agregar nuevas funcionalidades
- **Mantenibilidad**: Código bien documentado y organizado

## Consideraciones de Producción
Esta app está hecha para desarrollo para cambiar a produccion se debe de considerar cambiar el motor de base de datos y otras configuraciones
