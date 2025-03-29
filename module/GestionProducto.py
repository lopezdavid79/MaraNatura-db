import sqlite3
import logging
import pdb
# Configuración de logging para errores
logging.basicConfig(filename='errores.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class GestionProducto:
    def __init__(self, db_nombre="MaraNatura.db"):
        self.db_nombre = db_nombre
        try:
            self.conexion = sqlite3.connect(self.db_nombre)
            self.cursor = self.conexion.cursor()
            self.cursor.execute("PRAGMA foreign_keys = 1")
            self.cursor.execute("PRAGMA journal_mode = WAL;")
            self.conexion.commit()
            self.crear_tabla()
            logging.info("Conexión a la base de datos establecida.")
        except sqlite3.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            self.conexion = None

    def crear_tabla(self):
        """Crea la tabla productos si no existe."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                detalle TEXT,
                stock INTEGER,
                precio REAL
            )
        """)
        self.conexion.commit()
        logging.info("Tabla productos creada o ya existente.")

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos."""
        if self.conexion:
            self.conexion.close()
            logging.info("Conexión a la base de datos cerrada.")

    def agregar_producto(self, id, nombre, detalle, stock, precio):
        """Agrega un nuevo producto a la base de datos."""
        try:
            self.cursor.execute("INSERT INTO productos (id, nombre, detalle, stock, precio) VALUES (?, ?, ?, ?, ?)",
                                (id, nombre, detalle, stock, precio))
            self.conexion.commit()
            logging.info(f"Producto {nombre} agregado.")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error al agregar producto: {e}")
            return False

    def editar_producto(self, id, nombre=None, detalle=None, stock=None, precio=None):
        """Actualiza los datos de un producto existente."""
        try:
            updates = []
            values = []
            if nombre:
                updates.append("nombre = ?")
                values.append(nombre)
            if detalle:
                updates.append("detalle = ?")
                values.append(detalle)
            if stock is not None:
                updates.append("stock = ?")
                values.append(stock)
            if precio is not None:
                updates.append("precio = ?")
                values.append(precio)

            if updates:
                query = f"UPDATE productos SET {', '.join(updates)} WHERE id = ?"
                values.append(id)
                self.cursor.execute(query, values)
                self.conexion.commit()
                logging.info(f"Producto {id} actualizado.")
                return True
            else:
                logging.warning("No se proporcionaron datos para actualizar.")
                return False
        except sqlite3.Error as e:
            logging.error(f"Error al editar producto: {e}")
            return False

    def eliminar_producto(self, id):
        """Elimina un producto por su ID."""
        try:
            self.cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
            self.conexion.commit()
            logging.info(f"Producto {id} eliminado.")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar producto: {e}")
            return False



    def obtener_todos(self):
        """Recupera todos los productos de la base de datos."""
        try:
            self.cursor.execute("SELECT id, nombre, detalle, stock, precio FROM productos")
            productos = {str(row[0]): {"nombre": row[1], "detalle": row[2], "stock": row[3], "precio": row[4]}
                        for row in self.cursor.fetchall()}

            # Imprime los productos para depuración
            #print("Productos recuperados de la base de datos:")
            #for id_producto, datos_producto in productos.items():
                #print(f"  ID: {id_producto}, Nombre: {datos_producto['nombre']}, Detalle: {datos_producto['detalle']}, Stock: {datos_producto['stock']}, Precio: {datos_producto['precio']}")

            return productos
        except sqlite3.Error as e:
            logging.error(f"Error al obtener productos: {e}")
            return {}
    

    def obtener_productos(self):
        """Recupera todos los productos de la base de datos."""
        try:
            self.cursor.execute("SELECT id, nombre, detalle, stock, precio FROM productos")
            productos = {str(row[0]): {"nombre": row[1], "detalle": row[2], "stock": row[3], "precio": row[4]}
            for row in self.cursor.fetchall()}
            pdb.set_trace
            return productos
        except sqlite3.Error as e:
            logging.error(f"Error al obtener productos: {e}")
            return {}

    def existe_producto(self, id):
        """Verifica si un producto con el ID dado existe en la base de datos."""
        try:
            self.cursor.execute("SELECT 1 FROM productos WHERE id = ?", (id,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            logging.error(f"Error al verificar la existencia del producto: {e}")
            return False
        


    def obtener_productos_por_nombre(self, nombre_producto):
        """Recupera productos de la base de datos filtrando por nombre."""
        try:
            self.cursor.execute("SELECT id, nombre, detalle, stock, precio FROM productos WHERE nombre = ?", (nombre_producto,))
            productos = {str(row[0]): {"nombre": row[1], "detalle": row[2], "stock": row[3], "precio": row[4]}
                        for row in self.cursor.fetchall()}
            #pdb.set_trace()
            return productos
        except sqlite3.Error as e:
            logging.error(f"Error al obtener productos por nombre: {e}")
            return {}
        

#def guardar_productos(self,productos_vendidos):
        



    def buscar_producto(self, id_producto):
        """Recupera un producto específico de la base de datos por su ID."""
        try:
            self.cursor.execute("SELECT id, nombre, detalle, stock, precio FROM productos WHERE id = ?", (id_producto,))
            producto = self.cursor.fetchone() # Obtener un solo producto

            if producto:
                # Crear un diccionario con los datos del producto
                producto_dict = {
                    "id": producto[0],
                    "nombre": producto[1],
                    "detalle": producto[2],
                    "stock": producto[3],
                    "precio": producto[4]
                }
                return producto_dict
            else:
                return None  # Retornar None si no se encuentra el producto

        except sqlite3.Error as e:
            logging.error(f"Error al obtener el producto con ID {id_producto}: {e}")
            return None  # Retornar None en caso de error
        


    def actualizar_stock_producto(self, id_producto, cantidad):
        """Actualiza el stock de un producto en la base de datos."""
        try:
            # Validar la cantidad
            if not isinstance(cantidad, (int, float)) or cantidad <= 0:
                logging.error("La cantidad debe ser un número positivo.")
                return False

            # Obtener el stock actual del producto
            self.cursor.execute("SELECT stock FROM productos WHERE id = ?", (id_producto,))
            resultado = self.cursor.fetchone()

            if resultado:
                stock_actual = resultado[0]
                if cantidad > stock_actual:
                    logging.error(f"Cantidad {cantidad} excede el stock actual {stock_actual} del producto {id_producto}.")
                    return False
                nuevo_stock = stock_actual - cantidad

                # Actualizar el stock en la base de datos
                self.cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (nuevo_stock, id_producto))
                self.conexion.commit()
                logging.info(f"Stock del producto {id_producto} actualizado a {nuevo_stock}.")
                return True
            else:
                logging.warning(f"Producto con ID {id_producto} no encontrado en la base de datos.")
                return False

        except sqlite3.Error as e:
            logging.error(f"Error de base de datos al actualizar el stock del producto {id_producto}: {e}")
            return False
        except Exception as e:
            logging.error(f"Error inesperado al actualizar el stock del producto {id_producto}: {e}")
            return False
