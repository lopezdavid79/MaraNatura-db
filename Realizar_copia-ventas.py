import sqlite3
import json
import logging

logging.basicConfig(level=logging.INFO)

def insertar_datos_desde_json(ruta_db, ruta_json):
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    with open(ruta_json, 'r') as archivo_json:
        ventas_json = json.load(archivo_json)

    for venta in ventas_json:
        id_venta= venta.get('id')
        nombre = venta.get('nombre')
        direccion = venta.get('dire')  # Usar 'dire' como en el JSON
        telefono = venta.get('tel')    # Usar 'tel' como en el JSON

        if id_ventais not None:
            try:
                cursor.execute("INSERT INTO ventas (id, nombre, direccion, telefono) VALUES (?, ?, ?, ?)",
                               (id_venta, nombre, direccion, telefono))
                logging.info(f"ventainsertado: ID {id_venta}, Nombre {nombre}")
            except sqlite3.IntegrityError as e:
                logging.error(f"Error al insertar ventacon ID {id_venta}: {e}")
                conn.rollback()
        else:
            logging.warning("ventasin ID encontrado en el JSON.")

    conn.commit()
    conn.close()
    logging.info(f"Se insertaron los ventas desde '{ruta_json}' a '{ruta_db}'.")

if __name__ == "__main__":
    ruta_db = 'MaraNatura.db'  # Reemplaza si tu base de datos tiene otro nombre
    ruta_json = 'data/ventas.json'  # Reemplaza con la ruta a tu archivo JSON

    insertar_datos_desde_json(ruta_db, ruta_json)