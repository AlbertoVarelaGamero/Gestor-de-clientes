from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import re
import database as db

app = FastAPI(
    title="Gestor de Clientes API",
    description="API RESTful para gestionar clientes.",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type"],
)

# Modelos Pydantic
class ClienteCreate(BaseModel):
    dni: str
    nombre: str
    apellido: str

    class Config:
        schema_extra = {
            "example": {
                "dni": "99X",
                "nombre": "Hector",
                "apellido": "Costa"
            }
        }

class ClienteUpdate(BaseModel):
    nombre: str
    apellido: str

    class Config:
        schema_extra = {
            "example": {
                "nombre": "Mariana",
                "apellido": "Perez"
            }
        }

def dni_valido(dni: str) -> bool:
    if not re.match(r'^\d{2}[A-Z]$', dni):
        return False
    for cliente in db.Clientes.lista:
        if cliente.dni == dni:
            return False
    return True

@app.get("/clientes/", response_model=List[Dict[str, str]], summary="Listar todos los clientes")
async def listar_clientes() -> List[Dict[str, str]]:
    return [{"dni": c.dni, "nombre": c.nombre, "apellido": c.apellido} for c in db.Clientes.lista]

@app.get("/clientes/{dni}", response_model=Dict[str, str], summary="Buscar un cliente por DNI")
async def buscar_cliente(dni: str) -> Dict[str, str]:
    cliente = db.Clientes.buscar(dni)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return {"dni": cliente.dni, "nombre": cliente.nombre, "apellido": cliente.apellido}

@app.post("/clientes/", response_model=Dict[str, str], status_code=status.HTTP_201_CREATED, summary="Añadir un nuevo cliente")
async def crear_cliente(cliente: ClienteCreate) -> Dict[str, str]:
    if len(cliente.nombre) < 2 or len(cliente.nombre) > 30 or not cliente.nombre.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nombre inválido")
    if len(cliente.apellido) < 2 or len(cliente.apellido) > 30 or not cliente.apellido.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Apellido inválido")
    if not dni_valido(cliente.dni):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="DNI inválido o duplicado")
    
    nuevo_cliente = db.Clientes.crear(cliente.dni, cliente.nombre.capitalize(), cliente.apellido.capitalize())
    return {"dni": nuevo_cliente.dni, "nombre": nuevo_cliente.nombre, "apellido": nuevo_cliente.apellido}

@app.put("/clientes/{dni}", response_model=Dict[str, str], summary="Modificar un cliente existente")
async def modificar_cliente(dni: str, cliente: ClienteUpdate) -> Dict[str, str]:
    if len(cliente.nombre) < 2 or len(cliente.nombre) > 30 or not cliente.nombre.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nombre inválido")
    if len(cliente.apellido) < 2 or len(cliente.apellido) > 30 or not cliente.apellido.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Apellido inválido")
    
    cliente_modificado = db.Clientes.modificar(dni, cliente.nombre.capitalize(), cliente.apellido.capitalize())
    if not cliente_modificado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return {"dni": cliente_modificado.dni, "nombre": cliente_modificado.nombre, "apellido": cliente_modificado.apellido}

@app.delete("/clientes/{dni}", response_model=Dict[str, str], summary="Borrar un cliente")
async def borrar_cliente(dni: str) -> Dict[str, str]:
    cliente_borrado = db.Clientes.borrar(dni)
    if not cliente_borrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return {"dni": cliente_borrado.dni, "nombre": cliente_borrado.nombre, "apellido": cliente_borrado.apellido}