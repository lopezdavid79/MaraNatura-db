from module.GestionProducto import GestionProducto
import pdb
import pandas as pd
import sqlite3
import logging
import time
from datetime import datetime

# Configuración de logging para errores
logging.basicConfig(filename='errores.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


gestion_producto=GestionProducto()
class Venta:
    def __init__(self, id, fecha, id_cliente, productos, total):
        self.id = id
        self.fecha = fecha 
        self.id_cliente = id_cliente
        self.productos = productos
        self.total = total

class GestionVenta:
    def __init__(self, db_nombre="MaraNatura.db"):
        self.db_nombre = db_nombre
        try:
            self.conexion = sqlite3.connect(self.db_nombre)
            self.cursor = self.conexion.cursor()
            self.cursor.execute("PRAGMA foreign_keys = 1")
            self.cursor.execute("PRAGMA journal_mode = WAL;")
            self.conexion.commit()
            self.crear_tablas()
            logging.info("Conexión a la base de datos establecida.")
        except sqlite3.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            self.conexion = None

    def crear_tablas(self):
        """Crea las tablas ventas y productos_venta si no existen."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id INTEGER PRIMARY KEY,
                    fecha TEXT NOT NULL,
                    id_cliente INTEGER NOT NULL,
                    total REAL NOT NULL,
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id)
                )
            """)
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos_venta (
                    id_venta INTEGER,
                    id_producto INTEGER,
                    cantidad INTEGER NOT NULL,
                    FOREIGN KEY (id_venta) REFERENCES ventas(id),
                    FOREIGN KEY (id_producto) REFERENCES productos(id)
                )
            """)
            self.conexion.commit()
            logging.info("Tablas ventas y productos_venta creadas o ya existentes.")
        except sqlite3.Error as e:
            logging.error(f"Error al crear tablas: {e}")

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos."""
        if self.conexion:
            self.conexion.close()
            logging.info("Conexión a la base de datos cerrada.")
#registrar la venta
    def registrar_venta(self, fecha, id_cliente, productos_vendidos, total_venta, reintentos=3, espera=0.1):
        """Registra una nueva venta y actualiza el stock de forma atómica, con reintentos."""
        for intento in range(reintentos):
            try:
                self.cursor.execute("BEGIN TRANSACTION")

                # Registrar la venta
                self.cursor.execute("INSERT INTO ventas (fecha, id_cliente, total) VALUES (?, ?, ?)",
                                    (fecha, id_cliente, total_venta))
                id_venta = self.cursor.lastrowid

                # Registrar los productos vendidos
                for producto_info in productos_vendidos:
                    self.cursor.execute("INSERT INTO productos_venta (id_venta, id_producto, cantidad) VALUES (?, ?, ?)",
                                        (id_venta, producto_info["id_producto"], producto_info["cantidad"]))

                # Actualizar el stock en lote
                productos_actualizar = [(producto_info["cantidad"], producto_info["id_producto"]) for producto_info in productos_vendidos]
                self.actualizar_stock_productos_lote(productos_actualizar)

                self.conexion.commit()
                logging.info(f"Venta {id_venta} registrada.")
                return Venta(id_venta, fecha, id_cliente, productos_vendidos, total_venta)

            except sqlite3.OperationalError as e:
                self.conexion.rollback()
                if "database is locked" in str(e):
                    logging.warning(f"Base de datos bloqueada, reintentando venta. Intento {intento + 1}")
                    time.sleep(espera)  # Esperar antes de reintentar
                else:
                    logging.error(f"Error al registrar venta: {e}")
                    return None
            except sqlite3.Error as e:
                self.conexion.rollback()
                logging.error(f"Error al registrar venta: {e}")
                return None
        logging.error("No se pudo registrar la venta después de varios reintentos.")
        return None


    def actualizar_stock_productos_lote(self, productos_actualizar):
        """Actualiza el stock de varios productos en lote."""
        try:
            sql = "UPDATE productos SET stock = MAX(0, stock - ?) WHERE id = ?"
            self.cursor.executemany(sql, productos_actualizar)
            self.conexion.commit()
            logging.info(f"Stock de {len(productos_actualizar)} productos actualizado en lote.")
            return True

        except sqlite3.Error as e:
            self.conexion.rollback()
            logging.error(f"Error al actualizar stock de productos en lote: {e}")
            return False

    



    
    def obtener_todos(self):
        """Recupera todas las ventas de la base de datos."""
        try:
            self.cursor.execute("SELECT id, fecha, id_cliente, total FROM ventas")
            ventas = {str(row[0]): {"fecha": row[1], "id_cliente": row[2], "total": row[3]}
                      for row in self.cursor.fetchall()}
            return ventas
        except sqlite3.Error as e:
            logging.error(f"Error al obtener ventas: {e}")
            return {}


    def calcular_total_venta_desde_db(self, productos_seleccionados):
        """
        Calcula el total de la venta desde la base de datos, recibiendo la lista de productos seleccionados.

        Args:
            productos_seleccionados (list): Lista de diccionarios con los productos seleccionados.

        Returns:
            float: El total de la venta, o None si hay un error.
        """
        total_venta = 0.0
        if not productos_seleccionados:
            return total_venta  # No hay productos seleccionados, retorna 0.0

        try:           

            for producto_seleccionado in productos_seleccionados:
                producto_id = producto_seleccionado["id_producto"]
                cantidad_seleccionada = producto_seleccionado["cantidad"]

                self.cursor.execute("SELECT precio FROM productos WHERE id = ?", (producto_id,))
                resultado = self.cursor.fetchone()

                if resultado:
                    precio_producto = resultado[0]
                    total_venta += precio_producto * cantidad_seleccionada
                else:
                    print(f"Advertencia: Producto con ID {producto_id} no encontrado en la base de datos.")

            
            return total_venta

        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
            return None
        

    

    def buscar_venta(self, id_venta):
        """Busca una venta por su ID y devuelve un objeto Venta o None si no se encuentra."""
        try:
            # 1. Obtener la información básica de la venta
            self.cursor.execute("SELECT fecha, id_cliente, total FROM ventas WHERE id = ?", (id_venta,))
            venta_info = self.cursor.fetchone()

            if venta_info:
                fecha, id_cliente, total_venta = venta_info

                # 2. Obtener los productos vendidos en esta venta
                self.cursor.execute("SELECT id_producto, cantidad FROM productos_venta WHERE id_venta = ?", (id_venta,))
                productos_vendidos = []
                productos_venta_rows = self.cursor.fetchall()

                for row in productos_venta_rows:
                    productos_vendidos.append({"id_producto": row[0], "cantidad": row[1]})

                # 3. Crear y devolver el objeto Venta
                return Venta(id_venta, fecha, id_cliente, productos_vendidos, total_venta)
            else:
                return None  # No se encontró la venta

        except sqlite3.Error as e:
            logging.error(f"Error al buscar venta {id_venta}: {e}")
            return None
        
    def obtener_ventas_rango_pandas(self, fecha_inicio=None, fecha_fin=None):
        try:
            query = """
                SELECT v.fecha, c.id AS cliente_id, p.nombre AS producto,
                    pv.cantidad, p.precio, (pv.cantidad * p.precio) AS total_venta
                FROM ventas v
                JOIN clientes c ON v.id_cliente = c.id
                JOIN productos_venta pv ON v.id = pv.id_venta
                JOIN productos p ON pv.id_producto = p.id
            """

            params = ()
            if fecha_inicio and fecha_fin:
                query += """
                    WHERE DATE(SUBSTR(v.fecha, 7, 4) || '-' || SUBSTR(v.fecha, 4, 2) || '-' || SUBSTR(v.fecha, 1, 2))
                    BETWEEN ? AND ?
                """
                params = (fecha_inicio, fecha_fin)

            query += " ORDER BY v.fecha DESC"

            df = pd.read_sql_query(query, self.conexion, params=params)
            return df
        except Exception as e:
            logging.error(f"Error al obtener ventas en rango: {e}")
            return pd.DataFrame()
    
    def editar_venta(self, id_venta, fecha=None, id_cliente=None, total=None):
        """Actualiza los datos de una venta existente."""
        try:
            updates = []
            values = []
            if fecha:
                updates.append("fecha = ?")
                values.append(fecha)
            if id_cliente is not None:
                updates.append("id_cliente = ?")
                values.append(id_cliente)
            if total is not None:
                updates.append("total = ?")
                values.append(total)

            if updates:
                query = f"UPDATE ventas SET {', '.join(updates)} WHERE id = ?"
                values.append(id_venta)
                self.cursor.execute(query, values)
                self.conexion.commit()
                logging.info(f"Venta {id_venta} actualizada.")
                return True
            else:
                logging.warning("No se proporcionaron datos para actualizar la venta.")
                return False
        except sqlite3.Error as e:
            logging.error(f"Error al editar venta: {e}")
            return False
