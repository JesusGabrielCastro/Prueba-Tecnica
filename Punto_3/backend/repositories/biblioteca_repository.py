from fastapi import  HTTPException
from sqlalchemy.orm import  Session
from datetime import datetime, timedelta
from ..database.models import  Miembro, Libro, Prestamo
from ..models.schemas import PrestamoCrear


class GestorBiblioteca:
    
    @staticmethod
    def verificar_pertenencia_biblioteca(sesion: Session, numero_miembro: int, codigo_biblioteca: int) -> bool:
        """Verifica si un miembro pertenece a una biblioteca específica"""
        miembro = sesion.query(Miembro).filter(Miembro.numero_miembro == numero_miembro).first()
        return miembro and miembro.codigo_biblioteca == codigo_biblioteca
    
    @staticmethod
    def contar_prestamos_activos(sesion: Session, numero_miembro: int) -> int:
        """Cuenta los préstamos activos de un miembro"""
        return sesion.query(Prestamo).filter(
            Prestamo.numero_miembro == numero_miembro,
            Prestamo.estado_prestamo == "Activo"
        ).count()
    
    @staticmethod
    def verificar_disponibilidad_libro(sesion: Session, codigo_libro: str) -> bool:
        """Verifica si un libro está disponible para préstamo"""
        libro = sesion.query(Libro).filter(Libro.codigo_libro == codigo_libro).first()
        return libro and libro.cantidad_disponible > 0
    
    @staticmethod
    def procesar_prestamo(sesion: Session, datos_prestamo: PrestamoCrear) -> Prestamo:
        """Procesa un nuevo préstamo con todas las validaciones"""
        
        # Verificar que el miembro existe
        miembro = sesion.query(Miembro).filter(Miembro.numero_miembro == datos_prestamo.numero_miembro).first()
        if not miembro:
            raise HTTPException(status_code=404, detail="Miembro no encontrado")
        
        # Verificar que el libro existe
        libro = sesion.query(Libro).filter(Libro.codigo_libro == datos_prestamo.codigo_libro).first()
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        
        # Verificar que el miembro pertenece a la misma biblioteca que el libro
        if miembro.codigo_biblioteca != libro.codigo_biblioteca:
            raise HTTPException(
                status_code=403, 
                detail="El miembro solo puede solicitar libros de su biblioteca de origen"
            )
        
        # Verificar límite de préstamos
        prestamos_activos = GestorBiblioteca.contar_prestamos_activos(sesion, datos_prestamo.numero_miembro)
        if prestamos_activos >= miembro.limite_prestamos:
            raise HTTPException(
                status_code=400, 
                detail=f"Límite de préstamos alcanzado ({miembro.limite_prestamos})"
            )
        
        # Verificar disponibilidad del libro
        if libro.cantidad_disponible <= 0:
            raise HTTPException(status_code=400, detail="Libro no disponible")
        
        # Crear el préstamo
        fecha_limite = datetime.utcnow() + timedelta(days=datos_prestamo.dias_prestamo)
        nuevo_prestamo = Prestamo(
            numero_miembro=datos_prestamo.numero_miembro,
            codigo_libro=datos_prestamo.codigo_libro,
            fecha_limite=fecha_limite,
            observaciones_adicionales=datos_prestamo.observaciones_adicionales
        )
        
        # Reducir disponibilidad del libro
        libro.cantidad_disponible -= 1
        
        sesion.add(nuevo_prestamo)
        sesion.commit()
        sesion.refresh(nuevo_prestamo)
        
        return nuevo_prestamo