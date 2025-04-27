import pytest
from fastapi.testclient import TestClient
from gestor.api import app
import database as db
import config
from pathlib import Path
from typing import Generator

@pytest.fixture
def client() -> TestClient:
    return TestClient(app)

@pytest.fixture
def temp_db(tmp_path: Path) -> Generator[None, None, None]:
    # Configurar un archivo CSV temporal para pruebas
    original_path = config.DATABASE_PATH
    config.DATABASE_PATH = str(tmp_path / "test_clientes.csv")
    
    # Crear datos de prueba
    db.Clientes.lista.clear()
    db.Clientes.crear("15J", "Marta", "Perez")
    db.Clientes.crear("48H", "Manolo", "Lopez")
    db.Clientes.crear("28Z", "Ana", "Garcia")
    db.Clientes.guardar()
    
    yield
    
    # Restaurar configuración original
    config.DATABASE_PATH = original_path
    db.Clientes.cargar()

def test_listar_clientes(client: TestClient, temp_db: None) -> None:
    response = client.get("/clientes/")
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0] == {"dni": "15J", "nombre": "Marta", "apellido": "Perez"}

def test_buscar_cliente_existente(client: TestClient, temp_db: None) -> None:
    response = client.get("/clientes/15J")
    assert response.status_code == 200
    assert response.json() == {"dni": "15J", "nombre": "Marta", "apellido": "Perez"}

def test_buscar_cliente_no_existente(client: TestClient, temp_db: None) -> None:
    response = client.get("/clientes/99X")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado"

def test_crear_cliente_valido(client: TestClient, temp_db: None) -> None:
    nuevo_cliente = {"dni": "99X", "nombre": "Hector", "apellido": "Costa"}
    response = client.post("/clientes/", json=nuevo_cliente)
    assert response.status_code == 201
    assert response.json() == {"dni": "99X", "nombre": "Hector", "apellido": "Costa"}
    cliente = db.Clientes.buscar("99X")
    assert cliente is not None
    assert cliente.nombre == "Hector"

def test_crear_cliente_dni_invalido(client: TestClient, temp_db: None) -> None:
    nuevo_cliente = {"dni": "123X", "nombre": "Hector", "apellido": "Costa"}
    response = client.post("/clientes/", json=nuevo_cliente)
    assert response.status_code == 400
    assert response.json()["detail"] == "DNI inválido o duplicado"

def test_modificar_cliente_existente(client: TestClient, temp_db: None) -> None:
    datos_actualizados = {"nombre": "Mariana", "apellido": "Perez"}
    response = client.put("/clientes/28Z", json=datos_actualizados)
    assert response.status_code == 200
    assert response.json() == {"dni": "28Z", "nombre": "Mariana", "apellido": "Perez"}
    cliente = db.Clientes.buscar("28Z")
    assert cliente.nombre == "Mariana"

def test_modificar_cliente_no_existente(client: TestClient, temp_db: None) -> None:
    datos_actualizados = {"nombre": "Mariana", "apellido": "Perez"}
    response = client.put("/clientes/99X", json=datos_actualizados)
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado"

def test_borrar_cliente_existente(client: TestClient, temp_db: None) -> None:
    response = client.delete("/clientes/48H")
    assert response.status_code == 200
    assert response.json() == {"dni": "48H", "nombre": "Manolo", "apellido": "Lopez"}
    cliente = db.Clientes.buscar("48H")
    assert cliente is None

def test_borrar_cliente_no_existente(client: TestClient, temp_db: None) -> None:
    response = client.delete("/clientes/99X")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado"