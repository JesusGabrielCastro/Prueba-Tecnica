from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter
from ...database.models import Biblioteca, Miembro, Prestamo
from ...models.schemas import MiembroCrear, MiembroRespuesta
from ...database.db import get_db  

router = APIRouter(prefix="/miembros", tags=["Miembros"])

@router.post("/", response_model=MiembroRespuesta, status_code=status.HTTP_201_CREATED)
def crear_miembro(miembro: MiembroCrear, sesion: Session = Depends(get_db)):
    # Verificar que la biblioteca existe
    biblioteca = sesion.query(Biblioteca).filter(Biblioteca.codigo_biblioteca == miembro.codigo_biblioteca).first()
    if not biblioteca:
        raise HTTPException(status_code=404, detail="Biblioteca no encontrada")
    
    nuevo_miembro = Miembro(**miembro.dict())
    sesion.add(nuevo_miembro)
    sesion.commit()
    sesion.refresh(nuevo_miembro)
    return nuevo_miembro

@router.get("/bibliotecas/{codigo_biblioteca}/miembros", response_model=List[MiembroRespuesta])
def listar_miembros_biblioteca(codigo_biblioteca: int, sesion: Session = Depends(get_db)):
    return sesion.query(Miembro).filter(
        Miembro.codigo_biblioteca == codigo_biblioteca,
        Miembro.cuenta_activa == True
    ).all()

@router.put("/{numero_miembro}", response_model=MiembroRespuesta)
def actualizar_miembro(numero_miembro: int, miembro: MiembroCrear, sesion: Session = Depends(get_db)):
    miembro_bd = sesion.query(Miembro).filter(Miembro.numero_miembro == numero_miembro).first()
    if not miembro_bd:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    
    # Verificar que la nueva biblioteca existe si se está cambiando
    if miembro.codigo_biblioteca != miembro_bd.codigo_biblioteca:
        biblioteca = sesion.query(Biblioteca).filter(Biblioteca.codigo_biblioteca == miembro.codigo_biblioteca).first()
        if not biblioteca:
            raise HTTPException(status_code=404, detail="Nueva biblioteca no encontrada")
        
        # Verificar que no tenga préstamos activos antes de cambiar de biblioteca
        prestamos_activos = sesion.query(Prestamo).filter(
            Prestamo.numero_miembro == numero_miembro,
            Prestamo.estado_prestamo == "Activo"
        ).count()
        
        if prestamos_activos > 0:
            raise HTTPException(status_code=400, detail="No se puede cambiar de biblioteca con préstamos activos")
    
    for campo, valor in miembro.dict().items():
        setattr(miembro_bd, campo, valor)
    
    sesion.commit()
    sesion.refresh(miembro_bd)
    return miembro_bd

@router.delete("/{numero_miembro}")
def eliminar_miembro(numero_miembro: int, sesion: Session = Depends(get_db)):
    miembro = sesion.query(Miembro).filter(Miembro.numero_miembro == numero_miembro).first()
    if not miembro:
        raise HTTPException(status_code=404, detail="Miembro no encontrado")
    
    # Verificar que no tenga préstamos activos
    prestamos_activos = sesion.query(Prestamo).filter(
        Prestamo.numero_miembro == numero_miembro,
        Prestamo.estado_prestamo == "Activo"
    ).count()
    
    if prestamos_activos > 0:
        raise HTTPException(status_code=400, detail="No se puede eliminar miembro con préstamos activos")
    
    # Eliminar historial de préstamos del miembro
    prestamos_historial = sesion.query(Prestamo).filter(Prestamo.numero_miembro == numero_miembro).all()
    for prestamo in prestamos_historial:
        sesion.delete(prestamo)
    
    # Eliminar el miembro
    sesion.delete(miembro)
    sesion.commit()
    
    return {"mensaje": "Miembro y su historial eliminados exitosamente"}