# Gestor-de-clientes

https://github.com/AlbertoVarelaGamero/Gestor-de-clientes
Gestor de Clientes
Aplicación para gestionar clientes con interfaces de terminal, gráfica (Tkinter), y API REST (FastAPI).
Instalación

Crea un entorno virtual:
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


Instala las dependencias:
pip install -r requirements.txt


En Linux, instala Tkinter:
sudo apt-get install python3-tk



Ejecución

Modo terminal:
python3 run.py -t


Modo gráfico:
python3 run.py


API:
uvicorn gestor.api:app --reload

Accede a http://127.0.0.1:8000/docs para la documentación.

Pruebas unitarias:
pytest -v



Estructura

gestor/: Código fuente (run.py, menu.py, database.py, helpers.py, ui.py, config.py, api.py).
tests/: Pruebas unitarias (test_database.py, test_api.py, clientes_test.csv).
clientes.csv: Datos de clientes.
requirements.txt: Dependencias.

