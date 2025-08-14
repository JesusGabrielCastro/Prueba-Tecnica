from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter
from ...models.schemas import PrestamoCrear, PrestamoRespuesta
from ...database.models import Libro,Miembro,Prestamo
from ...repositories.biblioteca_repository import GestorBiblioteca
from ...database.db import get_db  
from datetime import datetime

router = APIRouter(prefix="/prestamos", tags=["Prestamos"])

@router.post("/", response_model=PrestamoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_prestamo(prestamo: PrestamoCrear, sesion: Session = Depends(get_db)):
    return GestorBiblioteca.procesar_prestamo(sesion, prestamo)

@router.get("/miembros/{numero_miembro}/prestamos", response_model=List[PrestamoRespuesta])
def listar_prestamos_miembro(numero_miembro: int, sesion: Session = Depends(get_db)):
    return sesion.query(Prestamo).filter(Prestamo.numero_miembro == numero_miembro).all()

@router.get("/bibliotecas/{codigo_biblioteca}/prestamos-activos")
def prestamos_activos_biblioteca(codigo_biblioteca: int, sesion: Session = Depends(get_db)):
    prestamos = sesion.query(Prestamo).join(Miembro).filter(
        Miembro.codigo_biblioteca == codigo_biblioteca,
        Prestamo.estado_prestamo == "Activo"
    ).all()
    return prestamos

@router.put("/{id_prestamo}/devolver")
def devolver_libro(id_prestamo: int, sesion: Session = Depends(get_db)):
    prestamo = sesion.query(Prestamo).filter(Prestamo.id_prestamo == id_prestamo).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
    if prestamo.estado_prestamo != "Activo":
        raise HTTPException(status_code=400, detail="El préstamo no está activo")
    
    # Actualizar préstamo
    prestamo.fecha_devolucion = datetime.now()
    prestamo.estado_prestamo = "Devuelto"
    
    # Calcular multa si hay retraso
    if datetime.now() > prestamo.fecha_limite:
        dias_retraso = (datetime.now() - prestamo.fecha_limite).days
        prestamo.multa_aplicada = dias_retraso * 1000  # $1000 por día de retraso
    
    # Incrementar disponibilidad del libro
    libro = sesion.query(Libro).filter(Libro.codigo_libro == prestamo.codigo_libro).first()
    if libro:
        libro.cantidad_disponible += 1
    
    sesion.commit()
    return {"mensaje": "Libro devuelto exitosamente", "multa": prestamo.multa_aplicada}

@router.delete("/{id_prestamo}")
def eliminar_prestamo(id_prestamo: int, sesion: Session = Depends(get_db)):
    prestamo = sesion.query(Prestamo).filter(Prestamo.id_prestamo == id_prestamo).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
    # Si el préstamo está activo, devolver la disponibilidad al libro
    if prestamo.estado_prestamo == "Activo":
        libro = sesion.query(Libro).filter(Libro.codigo_libro == prestamo.codigo_libro).first()
        if libro:
            libro.cantidad_disponible += 1
    
    # Eliminar el préstamo
    sesion.delete(prestamo)
    sesion.commit()
    
    return {"mensaje": "Préstamo eliminado exitosamente"}