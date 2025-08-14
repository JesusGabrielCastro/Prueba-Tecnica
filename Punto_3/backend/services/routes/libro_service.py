from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import APIRouter
from ...database.models import Biblioteca,Libro, Prestamo
from ...models.schemas import  LibroCrear, LibroRespuesta
from ...database.db import get_db  

router = APIRouter(prefix="/libros", tags=["Libros"])

@router.post("/", response_model=LibroRespuesta, status_code=status.HTTP_201_CREATED)
def crear_libro(libro: LibroCrear, sesion: Session = Depends(get_db)):
    # Verificar que la biblioteca existe
    biblioteca = sesion.query(Biblioteca).filter(Biblioteca.codigo_biblioteca == libro.codigo_biblioteca).first()
    if not biblioteca:
        raise HTTPException(status_code=404, detail="Biblioteca no encontrada")
    
    # Verificar que el código del libro no existe
    libro_existente = sesion.query(Libro).filter(Libro.codigo_libro == libro.codigo_libro).first()
    if libro_existente:
        raise HTTPException(status_code=400, detail="Código de libro ya existe")
    
    datos_libro = libro.dict()
    datos_libro["cantidad_disponible"] = datos_libro["cantidad_total"]
    nuevo_libro = Libro(**datos_libro)
    sesion.add(nuevo_libro)
    sesion.commit()
    sesion.refresh(nuevo_libro)
    return nuevo_libro

@router.get("/bibliotecas/{codigo_biblioteca}/libros", response_model=List[LibroRespuesta])
def listar_libros_biblioteca(codigo_biblioteca: int, sesion: Session = Depends(get_db)):
    return sesion.query(Libro).filter(Libro.codigo_biblioteca == codigo_biblioteca).all()

@router.get("/buscar")
def buscar_libros(
    titulo: Optional[str] = None,
    autor: Optional[str] = None,
    categoria: Optional[str] = None,
    codigo_biblioteca: Optional[int] = None,
    sesion: Session = Depends(get_db)
):
    consulta = sesion.query(Libro)
    
    if titulo:
        consulta = consulta.filter(Libro.titulo_obra.contains(titulo))
    if autor:
        consulta = consulta.filter(Libro.autor_principal.contains(autor))
    if categoria:
        consulta = consulta.filter(Libro.categoria_tema.contains(categoria))
    if codigo_biblioteca:
        consulta = consulta.filter(Libro.codigo_biblioteca == codigo_biblioteca)
    
    return consulta.all()

@router.put("/{codigo_libro}", response_model=LibroRespuesta)
def actualizar_libro(codigo_libro: str, libro: LibroCrear, sesion: Session = Depends(get_db)):
    libro_bd = sesion.query(Libro).filter(Libro.codigo_libro == codigo_libro).first()
    if not libro_bd:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    # Si se cambia el código del libro, verificar que el nuevo no exista
    if libro.codigo_libro != codigo_libro:
        libro_existente = sesion.query(Libro).filter(Libro.codigo_libro == libro.codigo_libro).first()
        if libro_existente:
            raise HTTPException(status_code=400, detail="El nuevo código de libro ya existe")
    
    # Verificar que la biblioteca existe si se está cambiando
    if libro.codigo_biblioteca != libro_bd.codigo_biblioteca:
        biblioteca = sesion.query(Biblioteca).filter(Biblioteca.codigo_biblioteca == libro.codigo_biblioteca).first()
        if not biblioteca:
            raise HTTPException(status_code=404, detail="Nueva biblioteca no encontrada")
        
        # Verificar que no tenga préstamos activos antes de cambiar de biblioteca
        prestamos_activos = sesion.query(Prestamo).filter(
            Prestamo.codigo_libro == codigo_libro,
            Prestamo.estado_prestamo == "Activo"
        ).count()
        
        if prestamos_activos > 0:
            raise HTTPException(status_code=400, detail="No se puede cambiar libro de biblioteca con préstamos activos")
    
    # Calcular nueva cantidad disponible si cambió la cantidad total
    if libro.cantidad_total != libro_bd.cantidad_total:
        diferencia = libro.cantidad_total - libro_bd.cantidad_total
        nueva_disponible = libro_bd.cantidad_disponible + diferencia
        if nueva_disponible < 0:
            raise HTTPException(status_code=400, detail="La nueva cantidad total no puede ser menor que los libros prestados")
        libro_bd.cantidad_disponible = nueva_disponible
    
    # Actualizar campos
    for campo, valor in libro.dict().items():
        if campo != "cantidad_total":  # Ya se manejó arriba
            setattr(libro_bd, campo, valor)
        else:
            setattr(libro_bd, campo, valor)
    
    sesion.commit()
    sesion.refresh(libro_bd)
    return libro_bd

@router.delete("/{codigo_libro}")
def eliminar_libro(codigo_libro: str, sesion: Session = Depends(get_db)):
    libro = sesion.query(Libro).filter(Libro.codigo_libro == codigo_libro).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    # Verificar que no tenga préstamos activos
    prestamos_activos = sesion.query(Prestamo).filter(
        Prestamo.codigo_libro == codigo_libro,
        Prestamo.estado_prestamo == "Activo"
    ).count()
    
    if prestamos_activos > 0:
        raise HTTPException(status_code=400, detail="No se puede eliminar libro con préstamos activos")
    
    # Eliminar historial de préstamos del libro
    prestamos_historial = sesion.query(Prestamo).filter(Prestamo.codigo_libro == codigo_libro).all()
    for prestamo in prestamos_historial:
        sesion.delete(prestamo)
    
    # Eliminar el libro
    sesion.delete(libro)
    sesion.commit()
    
    return {"mensaje": "Libro y su historial eliminados exitosamente"}