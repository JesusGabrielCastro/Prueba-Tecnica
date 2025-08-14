from fastapi import APIRouter
from .routes import biblioteca_service, prestamo_service, miembro_service ,libro_service


router = APIRouter()
router.include_router(biblioteca_service.router)
router.include_router(prestamo_service.router)
router.include_router(miembro_service.router)
router.include_router(libro_service.router)
