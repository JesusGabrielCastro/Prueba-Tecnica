from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


RUTA_BD = "sqlite:///./sistema_bibliotecas.db"
motor = create_engine(RUTA_BD, connect_args={"check_same_thread": False})
CrearSesion = sessionmaker(autocommit=False, autoflush=False, bind=motor)
ModeloBase = declarative_base()

# sesión de DB
def get_db() -> Session:
    db = CrearSesion()
    try:
        yield db
    finally:
        db.close()