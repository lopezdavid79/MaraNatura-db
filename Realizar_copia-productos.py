import sqlite3
import json
import logging

def insertar_productos_desde_json(ruta_db, archivo_json):
    """Inserta productos en la base de datos desde un archivo JSON."""
    try:
        conexion = sqlite3.connect(ruta_db)
        cursor = conexion.cursor()

        with open(archivo_json, 'r', encoding='utf-8') as archivo:
            productos_json = json.load(archivo)

        for id_producto, producto_info in productos_json.items():
            cursor.execute(
                "INSERT INTO productos (id, nombre, detalle, stock, precio) VALUES (?, ?, ?, ?, ?)",
                (
                    producto_info["id"],
                    producto_info["nombre"],
                    producto_info["detalle"],
                    producto_info["stock"],
                    producto_info["precio"],
                ),
            )
        conexion.commit()  # Guarda los cambios en la base de datos
        print("Productos insertados correctamente.")
        conexion.close()  # Cierra la conexión a la base de datos

    except FileNotFoundError:
        logging.error(f"Error: El archivo {archivo_json} no fue encontrado.")
    except json.JSONDecodeError:
        logging.error(f"Error: El archivo {archivo_json} no contiene JSON válido.")
    except sqlite3.Error as e:
        logging.error(f"Error al insertar productos: {e}")

# Ejemplo de uso:
ruta_db = "MaraNatura.db"  # Reemplaza con la ruta a tu base de datos
ruta_json = "data/productos.json"  # Reemplaza con la ruta a tu archivo JSON

insertar_productos_desde_json(ruta_db, ruta_json)