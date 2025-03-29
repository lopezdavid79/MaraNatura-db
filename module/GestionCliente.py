import pdb  # Importar el módulo pdb
import sqlite3
import logging
# Configuración de logging para errores
logging.basicConfig(filename='errores.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

class GestionCliente:
    def __init__(self, db_nombre="MaraNatura.db"):
        self.db_nombre = db_nombre
        try:
            self.conexion = sqlite3.connect(self.db_nombre)
            self.cursor = self.conexion.cursor()
            self.cursor.execute("PRAGMA foreign_keys = 1")
            self.conexion.commit()
            self.crear_tabla()
            logging.info("Conexión a la base de datos establecida.")
        except sqlite3.Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            self.conexion = None

    def crear_tabla(self):
        """Crea la tabla clientes si no existe."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT
            )
        """)
        self.conexion.commit()
        logging.info("Tabla clientes creada o ya existente.")

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos."""
        if self.conexion:
            self.conexion.close()
            logging.info("Conexión a la base de datos cerrada.")

    def registrar_cliente(self, nombre, direccion, telefono):
        """Registra un nuevo cliente en la base de datos."""
        try:
            self.cursor.execute("INSERT INTO clientes (nombre, direccion, telefono) VALUES (?, ?, ?)",
                                (nombre, direccion, telefono))
            self.conexion.commit()
            logging.info(f"Cliente {nombre} registrado.")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error al registrar cliente: {e}")
            return False

    def editar_cliente(self, id_cliente, nombre=None, direccion=None, telefono=None):
        """Actualiza los datos de un cliente existente."""
        try:
            updates = []
            values = []
            if nombre:
                updates.append("nombre = ?")
                values.append(nombre)
            if direccion:
                updates.append("direccion = ?")
                values.append(direccion)
            if telefono:
                updates.append("telefono = ?")
                values.append(telefono)

            if updates:
                query = f"UPDATE clientes SET {', '.join(updates)} WHERE id = ?"
                values.append(id_cliente)
                self.cursor.execute(query, values)
                self.conexion.commit()
                logging.info(f"Cliente {id_cliente} actualizado.")
                return True
            else:
                logging.warning("No se proporcionaron datos para actualizar.")
                return False
        except sqlite3.Error as e:
            logging.error(f"Error al editar cliente: {e}")
            return False

    def obtener_todos(self):
        """Recupera todos los clientes de la base de datos."""
        try:
            self.cursor.execute("SELECT id, nombre, direccion, telefono FROM clientes")
            #pdb.set_trace()
            clientes = {str(row[0]): {"nombre": row[1], "direccion": row[2], "telefono": row[3]}
                        for row in self.cursor.fetchall()}
            return clientes
        except sqlite3.Error as e:
            logging.error(f"Error al obtener clientes: {e}")
            return {}

    def buscar_cliente(self, id_cliente):
        """Busca un cliente por su ID y devuelve sus datos."""
        try:
            self.cursor.execute("SELECT id, nombre, direccion, telefono FROM clientes WHERE id = ?", (id_cliente,))
            resultado = self.cursor.fetchone()
            if resultado:
                return {"id": resultado[0], "nombre": resultado[1], "direccion": resultado[2], "telefono": resultado[3]}
            else:
                return None
        except sqlite3.Error as e:
            logging.error(f"Error al buscar cliente: {e}")
            return None

    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente por su ID."""
        try:
            self.cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
            self.conexion.commit()
            logging.info(f"Cliente {id_cliente} eliminado.")
            return True
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar cliente: {e}")
            return False
        

    def filtrar_clientes(self, filtro):
        """Busca clientes por nombre o teléfono."""
        try:
            self.cursor.execute("""
                SELECT nombre, telefono
                FROM clientes
                WHERE LOWER(nombre) LIKE ? OR LOWER(telefono) LIKE ?
            """, (f"%{filtro}%", f"%{filtro}%"))
            resultados = [f"{nombre} ({telefono})" for nombre, telefono in self.cursor.fetchall()]
            return resultados
        except sqlite3.Error as e:
            logging.error(f"Error al buscar clientes: {e}")
            return []



    def buscar_cliente_nombre(self, cliente):
        """Busca un cliente por su nombre y devuelve su id."""
        try:
            self.cursor.execute("SELECT id FROM clientes WHERE nombre= ?", (cliente,))
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
        except sqlite3.Error as e:
            logging.error(f"Error al buscar cliente: {e}")
            return None

    