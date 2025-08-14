from pydantic import BaseModel, Field
from typing import  Optional
from datetime import datetime


class BibliotecaBase(BaseModel):
    nombre_institucion: str = Field(..., min_length=1, max_length=200)
    direccion_sede: Optional[str] = None
    telefono_contacto: Optional[str] = None
    correo_administrador: Optional[str] = None

class BibliotecaCrear(BibliotecaBase):
    pass

class BibliotecaRespuesta(BibliotecaBase):
    codigo_biblioteca: int
    fecha_creacion: datetime
    estado_activo: bool
    
    class Config:
        from_attributes = True


class MiembroBase(BaseModel):
    nombres_completos: str = Field(..., min_length=1, max_length=150)
    documento_identidad: str = Field(..., min_length=1, max_length=20)
    telefono_personal: Optional[str] = None
    correo_electronico: Optional[str] = None
    direccion_residencia: Optional[str] = None
    codigo_biblioteca: int

class MiembroCrear(MiembroBase):
    pass

class MiembroRespuesta(MiembroBase):
    numero_miembro: int
    fecha_registro: datetime
    cuenta_activa: bool
    limite_prestamos: int
    
    class Config:
        from_attributes = True


class LibroBase(BaseModel):
    codigo_libro: str = Field(..., min_length=1, max_length=20)
    titulo_obra: str = Field(..., min_length=1, max_length=250)
    autor_principal: Optional[str] = None
    editorial_publicacion: Optional[str] = None
    ano_publicacion: Optional[int] = None
    categoria_tema: Optional[str] = None
    descripcion_contenido: Optional[str] = None
    numero_paginas: Optional[int] = None
    codigo_biblioteca: int
    cantidad_total: int = Field(default=1, ge=1)
    ubicacion_estante: Optional[str] = None
    estado_conservacion: str = Field(default="Bueno")

class LibroCrear(LibroBase):
    pass

class LibroRespuesta(LibroBase):
    cantidad_disponible: int
    fecha_ingreso: datetime
    
    class Config:
        from_attributes = True


class PrestamoBase(BaseModel):
    numero_miembro: int
    codigo_libro: str
    dias_prestamo: int = Field(default=14, ge=1, le=30)
    observaciones_adicionales: Optional[str] = None

class PrestamoCrear(PrestamoBase):
    pass

class PrestamoRespuesta(BaseModel):
    id_prestamo: int
    numero_miembro: int
    codigo_libro: str
    fecha_solicitud: datetime
    fecha_limite: datetime
    fecha_devolucion: Optional[datetime]
    estado_prestamo: str
    observaciones_adicionales: Optional[str]
    multa_aplicada: int
    
    class Config:
        from_attributes = True