import sqlite3
import json
import logging

logging.basicConfig(level=logging.INFO)

def insertar_datos_desde_json(ruta_db, ruta_json):
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    with open(ruta_json, 'r') as archivo_json:
        clientes_json = json.load(archivo_json)

    for cliente in clientes_json:
        id_cliente = cliente.get('id')
        nombre = cliente.get('nombre')
        direccion = cliente.get('dire')  # Usar 'dire' como en el JSON
        telefono = cliente.get('tel')    # Usar 'tel' como en el JSON

        if id_cliente is not None:
            try:
                cursor.execute("INSERT INTO clientes (id, nombre, direccion, telefono) VALUES (?, ?, ?, ?)",
                               (id_cliente, nombre, direccion, telefono))
                logging.info(f"Cliente insertado: ID {id_cliente}, Nombre {nombre}")
            except sqlite3.IntegrityError as e:
                logging.error(f"Error al insertar cliente con ID {id_cliente}: {e}")
                conn.rollback()
        else:
            logging.warning("Cliente sin ID encontrado en el JSON.")

    conn.commit()
    conn.close()
    logging.info(f"Se insertaron los clientes desde '{ruta_json}' a '{ruta_db}'.")

if __name__ == "__main__":
    ruta_db = 'MaraNatura.db'  # Reemplaza si tu base de datos tiene otro nombre
    ruta_json = 'data/clientes.json'  # Reemplaza con la ruta a tu archivo JSON

    insertar_datos_desde_json(ruta_db, ruta_json)