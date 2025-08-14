from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from backend.database.db import motor, ModeloBase
from backend.services.main import router as service_router

app = FastAPI(
    title="Sistema de Gestión de Bibliotecas",
    description="API para gestionar múltiples bibliotecas, miembros y préstamos",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas
ModeloBase.metadata.create_all(bind=motor)

app.include_router(service_router)