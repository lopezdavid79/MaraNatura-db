import datetime
import os
import wx
from module.ReproductorSonido import ReproductorSonido
from module.Productos import Producto
from module.GestionProducto import GestionProducto


# Inicialización
gestion_productos = GestionProducto()

class VentanaProducto(wx.Frame):
    def __init__(self, parent, id=None, title="Nuevo Producto", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        self.id = id  # Guarda el ID (puede ser None si es un nuevo producto)
        self.SetTitle(title)

        # Panel principal
        panel = wx.Panel(self)

        # Etiquetas y campos de entrada
        wx.StaticText(panel, label="ID:", pos=(10, 10))
        self.txt_id = wx.TextCtrl(panel, pos=(100, 10))

        wx.StaticText(panel, label="Producto:", pos=(10, 40))
        self.txt_producto = wx.TextCtrl(panel, pos=(100, 40))

        wx.StaticText(panel, label="Detalle:", pos=(10, 70))  # Corrección de posición
        self.txt_detalle = wx.TextCtrl(panel, pos=(100, 70))  # Corrección de posición

        wx.StaticText(panel, label="Stock:", pos=(10, 100))
        self.txt_stock = wx.TextCtrl(panel, pos=(100, 100))

        wx.StaticText(panel, label="Precio:", pos=(10, 130))
        self.txt_precio = wx.TextCtrl(panel, pos=(100, 130))

        # Botón de guardar
        btn_guardar = wx.Button(panel, label="Guardar", pos=(150, 180))
        btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_producto)

        # Botón de cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(250, 180))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)

        # Área de mensajes
        self.lbl_mensaje = wx.StaticText(panel, label="", pos=(10, 220))

        # Capturar eventos de teclado
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

        self.Show()

    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("G"):  # Ctrl + G
            self.guardar_producto(None)
        elif control_presionado and key_code == ord("C"):  # Ctrl + C -> Cerrar ventana
            self.cerrar_ventana(None)

        event.Skip()  # Permitir que otros eventos se procesen

    def guardar_producto(self, event):
        id_producto = self.txt_id.GetValue()
        nombre = self.txt_producto.GetValue()
        detalle = self.txt_detalle.GetValue()
        stock = self.txt_stock.GetValue()
        precio = self.txt_precio.GetValue()

        # Validación de campos vacíos
        if not all([id_producto, nombre, detalle, stock, precio]):
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.")
            return

        # Validación de tipos de datos
        try:
            id_producto = int(id_producto)
            stock = int(stock)
            precio = float(precio)
        except ValueError:
            self.mostrar_mensaje("Error: ID, Stock y Precio deben ser números.")
            return

        # Validación de ID positivo
        if id_producto <= 0:
            self.mostrar_mensaje("Error: El ID debe ser un número positivo.")
            return

        # Verificar si el ID ya existe
        if gestion_productos.existe_producto(id_producto):
            self.mostrar_mensaje("Error: Ya existe un producto con ese ID.")
            return

        # Agregar el producto
        gestion_productos.agregar_producto(id_producto, nombre, detalle, stock, precio)

        print(f"Producto guardado: ID={id_producto}, Producto={nombre}, Stock={stock}, Precio={precio}")
        ReproductorSonido.reproducir("Ok.wav")

        wx.MessageBox("Producto guardado con éxito.", "Éxito", wx.OK | wx.ICON_INFORMATION)

        # Limpiar campos
        self.txt_id.SetValue("")
        self.txt_producto.SetValue("")
        self.txt_detalle.SetValue("")
        self.txt_stock.SetValue("")
        self.txt_precio.SetValue("")

    def mostrar_mensaje(self, mensaje, tipo=wx.ICON_ERROR):
        wx.MessageBox(mensaje, "Error", style=tipo)

    def cerrar_ventana(self, event):
        self.Close()  # Cierra la ventana
import datetime
import os
import wx
from module.ReproductorSonido import ReproductorSonido
from module.Productos import Producto
from module.GestionProducto import GestionProducto


# Inicialización
gestion_productos = GestionProducto()

class VentanaProducto(wx.Frame):
    def __init__(self, parent, id=None, title="Nuevo Producto", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        self.id = id  # Guarda el ID (puede ser None si es un nuevo producto)
        self.SetTitle(title)

        # Panel principal
        panel = wx.Panel(self)

        # Etiquetas y campos de entrada
        wx.StaticText(panel, label="ID:", pos=(10, 10))
        self.txt_id = wx.TextCtrl(panel, pos=(100, 10))

        wx.StaticText(panel, label="Producto:", pos=(10, 40))
        self.txt_producto = wx.TextCtrl(panel, pos=(100, 40))

        wx.StaticText(panel, label="Detalle:", pos=(10, 70))  # Corrección de posición
        self.txt_detalle = wx.TextCtrl(panel, pos=(100, 70))  # Corrección de posición

        wx.StaticText(panel, label="Stock:", pos=(10, 100))
        self.txt_stock = wx.TextCtrl(panel, pos=(100, 100))

        wx.StaticText(panel, label="Precio:", pos=(10, 130))
        self.txt_precio = wx.TextCtrl(panel, pos=(100, 130))

        # Botón de guardar
        btn_guardar = wx.Button(panel, label="Guardar", pos=(150, 180))
        btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_producto)

        # Botón de cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(250, 180))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)

        # Área de mensajes
        self.lbl_mensaje = wx.StaticText(panel, label="", pos=(10, 220))

        # Capturar eventos de teclado
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

        self.Show()

    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("G"):  # Ctrl + G
            self.guardar_producto(None)
        elif control_presionado and key_code == ord("C"):  # Ctrl + C -> Cerrar ventana
            self.cerrar_ventana(None)

        event.Skip()  # Permitir que otros eventos se procesen

    def guardar_producto(self, event):
        id_producto = self.txt_id.GetValue()
        nombre = self.txt_producto.GetValue()
        detalle = self.txt_detalle.GetValue()
        stock = self.txt_stock.GetValue()
        precio = self.txt_precio.GetValue()

        # Validación de campos vacíos
        if not all([id_producto, nombre, detalle, stock, precio]):
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.")
            return

        # Validación de tipos de datos
        try:
            id_producto = int(id_producto)
            stock = int(stock)
            precio = float(precio)
        except ValueError:
            self.mostrar_mensaje("Error: ID, Stock y Precio deben ser números.")
            return

        # Validación de ID positivo
        if id_producto <= 0:
            self.mostrar_mensaje("Error: El ID debe ser un número positivo.")
            return

        # Verificar si el ID ya existe
        if gestion_productos.existe_producto(id_producto):
            self.mostrar_mensaje("Error: Ya existe un producto con ese ID.")
            return

        # Agregar el producto
        gestion_productos.agregar_producto(id_producto, nombre, detalle, stock, precio)

        print(f"Producto guardado: ID={id_producto}, Producto={nombre}, Stock={stock}, Precio={precio}")
        ReproductorSonido.reproducir("Ok.wav")

        wx.MessageBox("Producto guardado con éxito.", "Éxito", wx.OK | wx.ICON_INFORMATION)

        # Limpiar campos
        self.txt_id.SetValue("")
        self.txt_producto.SetValue("")
        self.txt_detalle.SetValue("")
        self.txt_stock.SetValue("")
        self.txt_precio.SetValue("")

    def mostrar_mensaje(self, mensaje, tipo=wx.ICON_ERROR):
        wx.MessageBox(mensaje, "Error", style=tipo)

    def cerrar_ventana(self, event):
        self.Close()  # Cierra la ventana
