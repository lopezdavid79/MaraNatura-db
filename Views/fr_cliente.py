import wx
import re
from module.ReproductorSonido import ReproductorSonido
from module.GestionCliente  import GestionCliente

# Inicialización
gestion_cliente= GestionCliente()

class VentanaCliente(wx.Frame):
    def __init__(self, parent, id=None, title="Nuevo Cliente", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        self.id = id  # Guarda el ID (puede ser None si es un nuevo cliente)
        self.SetTitle(title)  # Usa el título proporcionado
        
        # Panel principal
        panel = wx.Panel(self)

        # Etiquetas y campos de entrada
        #wx.StaticText(panel, label="ID:", pos=(10, 10))
        #self.txt_id = wx.TextCtrl(panel, pos=(100, 10))

        wx.StaticText(panel, label="Nombre:", pos=(10, 40))
        self.txt_nombre = wx.TextCtrl(panel, pos=(100, 40))

        wx.StaticText(panel, label="Dirección:", pos=(10, 70))
        self.txt_direccion = wx.TextCtrl(panel, pos=(100, 70))

        wx.StaticText(panel, label="Teléfono:", pos=(10, 100))
        self.txt_telefono = wx.TextCtrl(panel, pos=(100, 100))

        # Botón de guardar
        btn_guardar = wx.Button(panel, label="Guardar", pos=(150, 150))
        btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_cliente)

        # Botón de cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(250, 150))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)

        # Área de mensajes
        self.lbl_mensaje = wx.StaticText(panel, label="", pos=(10, 200))
        # Capturar eventos de teclado
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
        self.Show()

        """Captura teclas y ejecuta acciones según la combinación."""
    def on_key_down(self, event):

        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("G"):  # Ctrl + G
            self.guardar_cliente(None)
        elif control_presionado and key_code == ord("C"):  # Ctrl + C -> Cerrar ventana
            self.cerrar_ventana(None)
        event.Skip()  # Permitir que otros eventos se procesen

    def guardar_cliente(self, event):
        #id_cliente = self.txt_id.GetValue()
        id_cliente = max([c["id"] for c in gestion_cliente.clientes], default=0) + 1
        nombre = self.txt_nombre.GetValue()
        direccion = self.txt_direccion.GetValue()
        telefono = self.txt_telefono.GetValue()

        # Validación de campos obligatorios
        if not id_cliente or not nombre or not direccion or not telefono:
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.")
            return
        # Validación del nombre (solo letras, espacios y acentos)
        if not re.match("^[A-Za-zÁÉÍÓÚáéíóúñÑ ]+$", nombre):
            self.mostrar_mensaje("Error: El nombre solo puede contener letras, acentos y espacios.")
            return
        if not telefono.isdigit() or len(telefono) != 10:
            self.mostrar_mensaje("Error: El teléfono debe contener solo números y tener exactamente 10 dígitos.")
            return

        try:
            id_cliente = int(id_cliente)  # Convertir ID a entero
        except ValueError:
            self.mostrar_mensaje("Error: El ID debe ser un número.")
            return

        # Validación del ID
        if id_cliente <= 0:
            self.mostrar_mensaje("Error: El ID debe ser un número positivo.")
            return

        # Validación del teléfono (solo números y longitud adecuada)
        if not telefono.isdigit() or not (7 <= len(telefono) <= 15):
            self.mostrar_mensaje("Error: El teléfono debe contener solo números y tener entre 7 y 15 dígitos.")
            return

        # Verificar si el ID ya existe
        if gestion_cliente.buscar_cliente(id_cliente):
            self.mostrar_mensaje("Error: Ya existe un cliente con ese ID.")
            return

        # Registrar el cliente
        gestion_cliente.registrar_cliente(nombre, direccion, telefono)

        print(f"Cliente guardado: ID={id_cliente}, Nombre={nombre}, Dirección={direccion}, Teléfono={telefono}")
        ReproductorSonido.reproducir("Sounds/Ok.wav")
        self.mostrar_mensaje("Cliente guardado con éxito.", wx.ICON_INFORMATION)

        # Limpiar campos
        self.txt_id.SetValue("")
        self.txt_nombre.SetValue("")
        self.txt_direccion.SetValue("")
        self.txt_telefono.SetValue("")

    def mostrar_mensaje(self, mensaje, tipo=wx.ICON_ERROR):
        """Muestra un mensaje emergente en la ventana."""
        wx.MessageBox(mensaje, "Información", style=tipo)

    def cerrar_ventana(self, event):
        """Cierra la ventana actual."""
        self.Close()
