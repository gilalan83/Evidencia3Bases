
from pymongo import MongoClient

# Conectarse al servidor de MongoDB (por defecto, se conecta a localhost)
client = MongoClient()

# Seleccionar la base de datos
db = client["Evidencia3Bases"]

# Crear colección Videojuegos
videojuegos = db["Videojuegos"]

# Crear colección Ventas
ventas = db["Ventas"]

# Imprimir mensaje de confirmación
print("Base de datos creada correctamente: Evidencia3Bases")
print("Colecciones creadas correctamente: Videojuegos, Ventas")

# Crear documentos para la colección Videojuegos
videojuegos_data = [
    {"nombre": "Super Mario Bros", "plataforma": "NES", "lanzamiento": 1985},
    {"nombre": "The Legend of Zelda", "plataforma": "NES", "lanzamiento": 1986},
    {"nombre": "Minecraft", "plataforma": "Multiplataforma", "lanzamiento": 2011},
    {"nombre": "Grand Theft Auto V", "plataforma": "Multiplataforma", "lanzamiento": 2013},
    {"nombre": "Pokémon Rojo/Azul", "plataforma": "Game Boy", "lanzamiento": 1996},
    {"nombre": "The Witcher 3: Wild Hunt", "plataforma": "Multiplataforma", "lanzamiento": 2015}
]

# Insertar los documentos en la colección Videojuegos
result = videojuegos.insert_many(videojuegos_data)

# Crear documentos para la colección Ventas relacionados con los videojuegos
ventas_data = [
    {"videojuego_id": result.inserted_ids[0], "cantidad": 100, "ingresos": 50000},
    {"videojuego_id": result.inserted_ids[1], "cantidad": 80, "ingresos": 40000},
    {"videojuego_id": result.inserted_ids[2], "cantidad": 200, "ingresos": 100000},
    {"videojuego_id": result.inserted_ids[3], "cantidad": 150, "ingresos": 75000},
    {"videojuego_id": result.inserted_ids[4], "cantidad": 120, "ingresos": 60000},
    {"videojuego_id": result.inserted_ids[5], "cantidad": 180, "ingresos": 90000}
]

# Insertar los documentos en la colección Ventas
ventas.insert_many(ventas_data)

# Imprimir mensaje de confirmación
print("Documentos creados correctamente.")

# Indexar el campo "nombre" en la colección Videojuegos
videojuegos.create_index("nombre")
# Indexar el campo "videojuego_id" en la colección Ventas
ventas.create_index("videojuego_id")

while True:
    print("Menú:")
    print("1. Buscar en la colección Videojuegos")
    print("2. Mostrar ventas de un videojuego por nombre")
    print("3. Actualizar información")
    print("4. Agregar un nuevo documento")
    print("5. Eliminar ventas de un documento")
    print("6. Salir")


    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        filtro_nombre = input("Ingrese el nombre del videojuego a buscar: ")
        resultado = list(videojuegos.find({"nombre": filtro_nombre}))
        for i, juego in enumerate(resultado, 1):
            print(f"{i}. {juego}")
        
        if not resultado:
            print("No se encontraron resultados.")
    elif opcion == "2":
        filtro_nombre = input("Ingrese el nombre del videojuego para mostrar sus ventas: ")
        juego = videojuegos.find_one({"nombre": filtro_nombre})
        if not juego:
            print("No se encontró el videojuego.")
        else:
            resultado_ventas = list(ventas.find({"videojuego_id": juego["_id"]}))
            if not resultado_ventas:
                print("No se encontraron ventas para ese videojuego.")
            else:
                for venta in resultado_ventas:
                    print(venta)
    elif opcion == "3":
        nombre_videojuego = input("Ingrese el nombre del videojuego que desea actualizar: ")
        juego = videojuegos.find_one({"nombre": nombre_videojuego})
        if not juego:
            print("No se encontró el videojuego.")
        else:
            print("Menú de Actualización:")
            print("1. Actualizar nombre")
            print("2. Actualizar plataforma")
            print("3. Actualizar año de lanzamiento")

            opcion_actualizacion = input("Seleccione una opción de actualización: ")

            if opcion_actualizacion == "1":
                nuevo_nombre = input("Ingrese el nuevo nombre: ")
                videojuegos.update_one({"_id": juego["_id"]}, {"$set": {"nombre": nuevo_nombre}})
                print("Nombre actualizado correctamente.")
            elif opcion_actualizacion == "2":
                nueva_plataforma = input("Ingrese la nueva plataforma: ")
                videojuegos.update_one({"_id": juego["_id"]}, {"$set": {"plataforma": nueva_plataforma}})
                print("Plataforma actualizada correctamente.")
            elif opcion_actualizacion == "3":
                nuevo_lanzamiento = input("Ingrese el nuevo año de lanzamiento: ")
                videojuegos.update_one({"_id": juego["_id"]}, {"$set": {"lanzamiento": int(nuevo_lanzamiento)}})
                print("Año de lanzamiento actualizado correctamente.")
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")
    elif opcion == "4":
        print("Menú de Agregar Documento:")
        print("1. Agregar nuevo videojuego")
        print("2. Agregar nueva venta")

        opcion_agregar = input("Seleccione una opción para agregar un nuevo documento: ")

        if opcion_agregar == "1":
            nombre = input("Ingrese el nombre del nuevo videojuego: ")
            plataforma = input("Ingrese la plataforma del nuevo videojuego: ")
            lanzamiento = int(input("Ingrese el año de lanzamiento del nuevo videojuego: "))
            videojuegos.insert_one({"nombre": nombre, "plataforma": plataforma, "lanzamiento": lanzamiento})
            print("Nuevo videojuego agregado correctamente.")
        elif opcion_agregar == "2":
            videojuego_id = input("Ingrese el ID del videojuego al que pertenece la venta: ")
            cantidad = int(input("Ingrese la cantidad de unidades vendidas: "))
            precio_unitario = float(input("Ingrese el precio unitario de la venta: "))
            ventas.insert_one({"videojuego_id": videojuego_id, "cantidad": cantidad, "precio_unitario": precio_unitario})
            print("Nueva venta agregada correctamente.")
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")
    elif opcion == "5":
        nombre_videojuego = input("Ingrese el nombre del videojuego cuyas ventas desea eliminar: ")
        juego = videojuegos.find_one({"nombre": nombre_videojuego})
        if not juego:
            print("No se encontró el videojuego.")
        else:
            ventas.delete_many({"videojuego_id": juego["_id"]})
            print("Ventas eliminadas correctamente.")

    elif opcion == "6":
        break
   