import unittest
import copy
import csv
import config
import database as db
import helpers

class TestDatabase(unittest.TestCase):
    def setUp(self):
        db.Clientes.cargar()

    def test_buscar_cliente(self):
        cliente = db.Clientes.buscar('15J')
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente.nombre, 'Marta')
        self.assertEqual(cliente.apellido, 'Perez')
        cliente_no_existe = db.Clientes.buscar('99X')
        self.assertIsNone(cliente_no_existe)

    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('99X', 'Héctor', 'Costa')
        self.assertEqual(nuevo_cliente.dni, '99X')
        self.assertEqual(nuevo_cliente.nombre, 'Héctor')
        self.assertEqual(nuevo_cliente.apellido, 'Costa')

    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('28Z'))
        cliente_modificado = db.Clientes.modificar('28Z', 'Mariana', 'Pérez')
        self.assertEqual(cliente_a_modificar.nombre, 'Ana')
        self.assertEqual(cliente_modificado.nombre, 'Mariana')

    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('48H')
        cliente_rebuscado = db.Clientes.buscar('48H')
        self.assertIsNotNone(cliente_borrado)
        self.assertIsNone(cliente_rebuscado)

    def test_dni_valido(self):
        self.assertTrue(helpers.dni_valido('00A', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('23223X', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('F35', db.Clientes.lista))
        self.assertFalse(helpers.dni_valido('15J', db.Clientes.lista))

    def test_escritura_csv(self):
        db.Clientes.borrar('15J')
        db.Clientes.borrar('48H')
        db.Clientes.modificar('28Z', 'Mariana', 'Pérez')
        with open(config.DATABASE_PATH, newline='\n') as fichero:
            reader = csv.reader(fichero, delimiter=';')
            dni, nombre, apellido = next(reader)
            self.assertEqual(dni, '28Z')
            self.assertEqual(nombre, 'Mariana')
            self.assertEqual(apellido, 'Pérez')

if __name__ == '__main__':
    unittest.main()