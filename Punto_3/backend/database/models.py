from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .db import ModeloBase

class Biblioteca(ModeloBase):
    __tablename__ = "bibliotecas"
    
    codigo_biblioteca = Column(Integer, primary_key=True, index=True)
    nombre_institucion = Column(String(200), nullable=False)
    direccion_sede = Column(String(300))
    telefono_contacto = Column(String(15))
    correo_administrador = Column(String(100))
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    estado_activo = Column(Boolean, default=True)
    
    # relacion
    miembros_asociados = relationship("Miembro", back_populates="biblioteca_origen")
    inventario_libros = relationship("Libro", back_populates="biblioteca_propietaria")


class Miembro(ModeloBase):
    __tablename__ = "miembros"
    
    numero_miembro = Column(Integer, primary_key=True, index=True)
    nombres_completos = Column(String(150), nullable=False)
    documento_identidad = Column(String(20), unique=True, nullable=False)
    telefono_personal = Column(String(15))
    correo_electronico = Column(String(100))
    direccion_residencia = Column(String(200))
    fecha_registro = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    codigo_biblioteca = Column(Integer, ForeignKey("bibliotecas.codigo_biblioteca"), nullable=False)
    cuenta_activa = Column(Boolean, default=True)
    limite_prestamos = Column(Integer, default=3)
    
    # relacion
    biblioteca_origen = relationship("Biblioteca", back_populates="miembros_asociados")
    historial_prestamos = relationship("Prestamo", back_populates="miembro_solicitante")


class Libro(ModeloBase):
    __tablename__ = "libros"
    
    codigo_libro = Column(String(20), primary_key=True, index=True)  # En lugar de ISBN
    titulo_obra = Column(String(250), nullable=False)
    autor_principal = Column(String(150))
    editorial_publicacion = Column(String(100))
    ano_publicacion = Column(Integer)
    categoria_tema = Column(String(50))
    descripcion_contenido = Column(Text)
    numero_paginas = Column(Integer)
    codigo_biblioteca = Column(Integer, ForeignKey("bibliotecas.codigo_biblioteca"), nullable=False)
    cantidad_disponible = Column(Integer, default=1)
    cantidad_total = Column(Integer, default=1)
    ubicacion_estante = Column(String(20))
    ESTADO_CONSERVACION_ENUM = ("Bueno", "Regular", "Malo")

    estado_conservacion = Column(
        Enum(*ESTADO_CONSERVACION_ENUM, name="estado_conservacion_enum"),
        default="Bueno",
        nullable=False
    )
    fecha_ingreso = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # relacion
    biblioteca_propietaria = relationship("Biblioteca", back_populates="inventario_libros")
    registros_prestamo = relationship("Prestamo", back_populates="libro_prestado")


class Prestamo(ModeloBase):
    __tablename__ = "prestamos"
    
    id_prestamo = Column(Integer, primary_key=True, index=True)  
    numero_miembro = Column(Integer, ForeignKey("miembros.numero_miembro"), nullable=False)
    codigo_libro = Column(String(20), ForeignKey("libros.codigo_libro"), nullable=False)
    fecha_solicitud = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    fecha_limite = Column(DateTime, nullable=False)
    fecha_devolucion = Column(DateTime, nullable=True)
    ESTADO_PRESTAMO_ENUM = ("Activo", "Devuelto", "Vencido")
    estado_prestamo = Column(
        Enum(*ESTADO_PRESTAMO_ENUM, name="estado_prestamo_enum"),
        default="Activo",
        nullable=False
    )
    observaciones_adicionales = Column(Text)
    multa_aplicada = Column(Integer, default=0)
    
    # relacion
    miembro_solicitante = relationship("Miembro", back_populates="historial_prestamos")
    libro_prestado = relationship("Libro", back_populates="registros_prestamo")
