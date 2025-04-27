import os
import helpers
import database as db

def iniciar():
    while True:
        helpers.limpiar_pantalla()
        print("========================")
        print("  BIENVENIDO AL Manager ")
        print("========================")
        print("[1] Listar clientes")
        print("[2] Buscar cliente")
        print("[3] Añadir cliente")
        print("[4] Modificar cliente")
        print("[5] Borrar cliente")
        print("[6] Cerrar el Manager")
        print("========================")
        
        opcion = input('> ')
        helpers.limpiar_pantalla()

        if opcion == '1':
            print("Listando los clientes...\n")
            for cliente in db.Clientes.lista:
                print(cliente)
        
        elif opcion == '2':
            print("Buscando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 dígitos y 1 letra): ").upper()
            cliente = db.Clientes.buscar(dni)
            print(cliente if cliente else "Cliente no encontrado.")
        
        elif opcion == '3':
            print("Añadiendo un cliente...\n")
            while True:
                dni = helpers.leer_texto(3, 3, "DNI (2 dígitos y 1 letra): ").upper()
                if helpers.dni_valido(dni, db.Clientes.lista):
                    break
            nombre = helpers.leer_texto(2, 30, "Nombre (2 a 30 caracteres): ").capitalize()
            apellido = helpers.leer_texto(2, 30, "Apellido (2 a 30 caracteres): ").capitalize()
            db.Clientes.crear(dni, nombre, apellido)
            print("Cliente añadido correctamente.")
        
        elif opcion == '4':
            print("Modificando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 dígitos y 1 letra): ").upper()
            cliente = db.Clientes.buscar(dni)
            if cliente:
                nombre = helpers.leer_texto(2, 30, f"Nombre (2 a 30 caracteres) [{cliente.nombre}]: ").capitalize()
                apellido = helpers.leer_texto(2, 30, f"Apellido (2 a 30 caracteres) [{cliente.apellido}]: ").capitalize()
                db.Clientes.modificar(dni, nombre, apellido)
                print("Cliente modificado correctamente.")
            else:
                print("Cliente no encontrado.")
        
        elif opcion == '5':
            print("Borrando un cliente...\n")
            dni = helpers.leer_texto(3, 3, "DNI (2 dígitos y 1 letra): ").upper()
            if db.Clientes.borrar(dni):
                print("Cliente borrado correctamente.")
            else:
                print("Cliente no encontrado.")
        
        elif opcion == '6':
            print("Saliendo...\n")
            break
        
        else:
            print("Opción no válida.")
        
        input("\nPresiona ENTER para continuar...")