"""
import csv
import config

class Cliente:
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f"({self.dni}) {self.nombre} {self.apellido}"

class Clientes:
    lista = []

    @staticmethod
    def cargar():
        Clientes.lista.clear()
        try:
            with open(config.DATABASE_PATH, newline='\n') as fichero:
                reader = csv.reader(fichero, delimiter=';')
                for dni, nombre, apellido in reader:
                    cliente = Cliente(dni, nombre, apellido)
                    Clientes.lista.append(cliente)
        except FileNotFoundError:
            pass  # El archivo se creará al guardar

    @staticmethod
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente
        return None

    @staticmethod
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar()
        return cliente

    @staticmethod
    def modificar(dni, nombre, apellido):
        for i, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                Clientes.lista[i].nombre = nombre
                Clientes.lista[i].apellido = apellido
                Clientes.guardar()
                return Clientes.lista[i]
        return None

    @staticmethod
    def borrar(dni):
        for i, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                cliente = Clientes.lista.pop(i)
                Clientes.guardar()
                return cliente
        return None

    @staticmethod
    def guardar():
        with open(config.DATABASE_PATH, 'w', newline='\n') as fichero:
            writer = csv.writer(fichero, delimiter=';')
            for cliente in Clientes.lista:
                writer.writerow([cliente.dni, cliente.nombre, cliente.apellido])

# Cargar clientes al iniciar
Clientes.cargar()
"""
import csv
import config
import shutil
import os
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    filename='gestor_clientes.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Cliente:
    def __init__(self, dni, nombre, apellido):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __str__(self):
        return f"({self.dni}) {self.nombre} {self.apellido}"

class Clientes:
    lista = []

    @staticmethod
    def cargar():
        Clientes.lista.clear()
        try:
            with open(config.DATABASE_PATH, newline='\n') as fichero:
                reader = csv.reader(fichero, delimiter=';')
                for dni, nombre, apellido in reader:
                    cliente = Cliente(dni, nombre, apellido)
                    Clientes.lista.append(cliente)
            logging.info("Base de datos cargada correctamente")
        except FileNotFoundError:
            logging.warning("Archivo CSV no encontrado, se creará uno nuevo")
        except Exception as e:
            logging.error(f"Error al cargar la base de datos: {str(e)}")
            raise

    @staticmethod
    def buscar(dni):
        for cliente in Clientes.lista:
            if cliente.dni == dni:
                return cliente
        return None

    @staticmethod
    def crear(dni, nombre, apellido):
        cliente = Cliente(dni, nombre, apellido)
        Clientes.lista.append(cliente)
        Clientes.guardar()
        logging.info(f"Cliente creado: {dni} - {nombre} {apellido}")
        return cliente

    @staticmethod
    def modificar(dni, nombre, apellido):
        for i, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                Clientes.lista[i].nombre = nombre
                Clientes.lista[i].apellido = apellido
                Clientes.guardar()
                logging.info(f"Cliente modificado: {dni} - {nombre} {apellido}")
                return Clientes.lista[i]
        return None

    @staticmethod
    def borrar(dni):
        for i, cliente in enumerate(Clientes.lista):
            if cliente.dni == dni:
                cliente = Clientes.lista.pop(i)
                Clientes.guardar()
                logging.info(f"Cliente borrado: {dni} - {cliente.nombre} {cliente.apellido}")
                return cliente
        return None

    @staticmethod
    def guardar():
        try:
            # Crear respaldo antes de guardar
            if os.path.exists(config.DATABASE_PATH):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"{config.DATABASE_PATH}.{timestamp}.bak"
                shutil.copy(config.DATABASE_PATH, backup_path)
                logging.info(f"Respaldo creado: {backup_path}")
            
            with open(config.DATABASE_PATH, 'w', newline='\n') as fichero:
                writer = csv.writer(fichero, delimiter=';')
                for cliente in Clientes.lista:
                    writer.writerow([cliente.dni, cliente.nombre, cliente.apellido])
            logging.info("Base de datos guardada correctamente")
        except Exception as e:
            logging.error(f"Error al guardar en el archivo CSV: {str(e)}")
            raise
# Cargar clientes al iniciar
Clientes.cargar()