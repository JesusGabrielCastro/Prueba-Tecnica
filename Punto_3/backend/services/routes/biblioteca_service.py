from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter
from ...models.schemas import BibliotecaRespuesta, BibliotecaCrear
from ...database.models import Biblioteca, Prestamo, Miembro, Libro
from ...database.db import get_db  

router = APIRouter(prefix="/biblioteca", tags=["Biblioteca"])

@router.post("/", response_model=BibliotecaRespuesta, status_code=status.HTTP_201_CREATED)
def crear_biblioteca(biblioteca: BibliotecaCrear, sesion: Session = Depends(get_db)):
    nueva_biblioteca = Biblioteca(**biblioteca.dict())
    sesion.add(nueva_biblioteca)
    sesion.commit()
    sesion.refresh(nueva_biblioteca)
    return nueva_biblioteca

@router.get("/", response_model=List[BibliotecaRespuesta])
def listar_bibliotecas(sesion: Session = Depends(get_db)):
    return sesion.query(Biblioteca).filter(Biblioteca.estado_activo == True).all()

@router.get("/{codigo_biblioteca}", response_model=BibliotecaRespuesta)
def obtener_biblioteca(codigo_biblioteca: int, sesion: Session = Depends(get_db)):
    biblioteca = sesion.query(Biblioteca).filter(Biblioteca.codigo_biblioteca == codigo_biblioteca).first()
    if not biblioteca:
        raise HTTPException(status_code=404, detail="Biblioteca no encontrada")
    return biblioteca

@router.put("/{codigo_biblioteca}", response_model=BibliotecaRespuesta)
def actualizar_biblioteca(codigo_biblioteca: int, biblioteca: BibliotecaCrear, sesion: Session = Depends(get_db)):
    biblioteca_bd = sesion.query(Biblioteca).filter(Biblioteca.codigo_biblioteca == codigo_biblioteca).first()
    if not biblioteca_bd:
        raise HTTPException(status_code=404, detail="Biblioteca no encontrada")
    
    for campo, valor in biblioteca.dict().items():
        setattr(biblioteca_bd, campo, valor)
    
    sesion.commit()
    sesion.refresh(biblioteca_bd)
    return biblioteca_bd

@router.delete("/{codigo_biblioteca}")
def eliminar_biblioteca(codigo_biblioteca: int, sesion: Session = Depends(get_db)):
    biblioteca = sesion.query(Biblioteca).filter(Biblioteca.codigo_biblioteca == codigo_biblioteca).first()
    if not biblioteca:
        raise HTTPException(status_code=404, detail="Biblioteca no encontrada")
    
    # Eliminar en cascada: préstamos -> miembros -> libros -> biblioteca
    # Eliminar préstamos de miembros de esta biblioteca
    prestamos = sesion.query(Prestamo).join(Miembro).filter(Miembro.codigo_biblioteca == codigo_biblioteca).all()
    for prestamo in prestamos:
        sesion.delete(prestamo)
    
    # Eliminar miembros de esta biblioteca
    miembros = sesion.query(Miembro).filter(Miembro.codigo_biblioteca == codigo_biblioteca).all()
    for miembro in miembros:
        sesion.delete(miembro)
    
    # Eliminar libros de esta biblioteca
    libros = sesion.query(Libro).filter(Libro.codigo_biblioteca == codigo_biblioteca).all()
    for libro in libros:
        sesion.delete(libro)
    
    # Eliminar la biblioteca
    sesion.delete(biblioteca)
    sesion.commit()
    
    return {"mensaje": "Biblioteca y todos sus datos asociados eliminados exitosamente"}