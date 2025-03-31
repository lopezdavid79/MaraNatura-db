import sqlite3

def borrar_datos_productos(nombre_base_datos):
    """Borra todos los datos de la tabla 'productos' en la base de datos especificada."""
    try:
        conn = sqlite3.connect(nombre_base_datos)
        cursor = conn.cursor()

        # Borrar todos los registros de la tabla productos
        cursor.execute("DELETE FROM ventas ")
        conn.commit()
        print(f"Se borraron todos los datos de la tabla 'productos' en '{nombre_base_datos}'.")

    except sqlite3.Error as e:
        print(f"Error al borrar datos de la tabla 'productos' en '{nombre_base_datos}': {e}")
        if conn:
            conn.rollback()  # Revertir cualquier cambio en caso de error

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    nombre_bd = 'MaraNatura.db'  # Reemplaza con el nombre de tu base de datos
    confirmacion = input(f"¿Estás seguro de que quieres borrar todos los datos de la tabla 'productos' en '{nombre_bd}'? (s/n): ")
    if confirmacion.lower() == 's':
        borrar_datos_productos(nombre_bd)
    else:
        print("Operación de borrado cancelada.")