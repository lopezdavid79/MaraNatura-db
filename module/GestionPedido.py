import json
import os
import sys

from module.Pedido import Pedido  # Importa la clase Pedido

class GestionPedido:
    def __init__(self, nombre_archivo='pedidos.json'):
        self.nombre_archivo = nombre_archivo
        self.pedidos = self.cargar_datos()
        if not isinstance(self.pedidos, list):
            self.pedidos = []

    def _obtener_ruta_completa(self):
        """Obtiene la ruta completa al archivo JSON."""
        if getattr(sys, 'frozen', False):
            ruta_base = sys._MEIPASS
        else:
            ruta_base = os.path.abspath('.')
        return os.path.join(ruta_base, 'data', self.nombre_archivo)

    def cargar_datos(self):
        """Carga los pedidos desde el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa()
        if os.path.exists(ruta_completa):
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                try:
                    pedidos_lista = json.load(archivo)
                    return pedidos_lista
                except json.JSONDecodeError:
                    print("❌ Error al leer JSON, inicializando una lista vacía.")
                    return []
        else:
            return []

    def guardar_datos(self):
        """Guarda la lista de pedidos en el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa()
        with open(ruta_completa, 'w', encoding='utf-8') as archivo:
            json.dump(self.pedidos, archivo, indent=4, ensure_ascii=False)

    def registrar_pedido(self, fecha, cliente, detalle, estado):
        """Registra un nuevo pedido y lo guarda en la base de datos."""
        nuevo_id = len(self.pedidos) + 1
        nuevo_pedido = Pedido(nuevo_id, fecha, cliente, detalle, estado)
        pedido_dict = nuevo_pedido.a_diccionario()  # Usamos el método a_diccionario
        self.pedidos.append(pedido_dict)
        self.guardar_datos()
        print(f"Pedido registrado: {pedido_dict}")
        return nuevo_pedido

    def editar_pedido(self, id_pedido, fecha=None, cliente=None, detalle=None, estado=None):
        """Edita un pedido existente."""
        try:
            id_pedido = int(id_pedido)
        except ValueError:
            print(f"❌ Error: ID {id_pedido} no es un número válido")
            return

        pedido = next((p for p in self.pedidos if p["id"] == id_pedido), None)

        if not pedido:
            print(f"❌ Error: Pedido con ID {id_pedido} no encontrado")
            return

        if fecha:
            pedido["fecha"] = fecha
        if cliente:
            pedido["cliente"] = cliente
        if detalle:
            pedido["detalle"] = detalle
        if estado:
            pedido["estado"] = estado

        self.guardar_datos()
        print(f"✅ Pedido {id_pedido} actualizado: {pedido}")

    def obtener_todos(self):
        """Devuelve todos los pedidos como un diccionario indexado."""
        return {str(pedido["id"]): pedido for pedido in self.pedidos}

    def buscar_pedido(self, id_pedido):
        """Busca un pedido por su ID y devuelve su información."""
        for pedido in self.pedidos:
            if pedido["id"] == id_pedido:
                return pedido
        return None

    def eliminar_pedido(self, id_pedido):
        """Elimina un pedido por su ID."""
        try:
            id_pedido = int(id_pedido)
        except ValueError:
            print(f"❌ Error: ID {id_pedido} no es un número válido")
            return False

        pedido = next((p for p in self.pedidos if p["id"] == id_pedido), None)

        if pedido:
            self.pedidos.remove(pedido)
            self.guardar_datos()
            print(f"Pedido con ID {id_pedido} eliminado.")
            return True

        print(f"Pedido con ID {id_pedido} no encontrado.")
        return False