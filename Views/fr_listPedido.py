import re
import sys
import wx
import wx.lib.mixins.listctrl as listmix
from module.ReproductorSonido import ReproductorSonido
from module.GestionPedido import GestionPedido

gestion_pedido = GestionPedido()

class ListPedido(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=None, title="Gestión de Pedidos", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        panel = wx.Panel(self)

        # Lista de pedidos
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(600, 250))  # Aumentamos el tamaño
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'Fecha', width=100)
        self.list_ctrl.InsertColumn(2, 'Cliente', width=150)
        self.list_ctrl.InsertColumn(3, 'Detalle', width=200)
        self.list_ctrl.InsertColumn(4, 'Estado', width=100)
        self.cargar_pedidos()
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mostrar_detalle_pedido)

        # Botones
        btn_nuevo = wx.Button(panel, label="Nuevo Pedido", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        btn_actualizar = wx.Button(panel, label="Actualizar", pos=(175, 300))
        btn_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_lista)

        self.Show()

    def actualizar_lista(self, event):
        self.cargar_pedidos()
        print("Lista actualizada en la interfaz")
        sys.stdout.flush()
        ReproductorSonido.reproducir("refresh.wav")

    def cargar_pedidos(self):
        self.list_ctrl.DeleteAllItems()
        pedidos = gestion_pedido.obtener_todos()
        for id_pedido, datos in pedidos.items():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(id_pedido))
            self.list_ctrl.SetItem(index, 1, datos["fecha"])
            self.list_ctrl.SetItem(index, 2, datos["cliente"])
            self.list_ctrl.SetItem(index, 3, datos["detalle"])
            self.list_ctrl.SetItem(index, 4, datos["estado"])

    def mostrar_detalle_pedido(self, event):
        index = event.GetIndex()
        id_pedido = self.list_ctrl.GetItemText(index)

        # Obtener los detalles del pedido
        pedidos = gestion_pedido.obtener_todos()
        if id_pedido in pedidos:
            datos = pedidos[id_pedido]
            dialogo = DetallePedidoDialog(self, id_pedido, datos)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_pedidos()  # Actualizar la lista después de la edición

    def abrir_dialogo_nuevo(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        dialogo = AgregarPedidoDialog(self)
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_pedidos()  # Actualiza la lista después de agregar un pedido
        dialogo.Destroy()

    def cerrar_ventana(self, event):
        ReproductorSonido.reproducir("screenCurtainOff.wav")
        self.Close()

class DetallePedidoDialog(wx.Dialog):
    def __init__(self, parent, id_pedido, datos):
        super().__init__(parent, title="Detalle del Pedido", size=(300, 250))
        self.id_pedido = id_pedido

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Mostrar detalles
        vbox.Add(wx.StaticText(panel, label=f"ID: {id_pedido}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Fecha: {datos['fecha']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Cliente: {datos['cliente']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Detalle: {datos['detalle']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Estado: {datos['estado']}"), flag=wx.LEFT | wx.TOP, border=10)

        # Botón para editar
        btn_editar = wx.Button(panel, label="Editar")
        btn_editar.Bind(wx.EVT_BUTTON, self.editar_pedido)
        # eliminar pedido
        btn_delete = wx.Button(panel, label="Eliminar")
        btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_pedido)
        # Botón para cerrar
        btn_cerrar = wx.Button(panel, wx.ID_CANCEL, "Cerrar")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_editar, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cerrar)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def editar_pedido(self, event):
        dialogo = EditarPedidoDialog(self, self.id_pedido)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)  # Cierra el diálogo y recarga la lista
        dialogo.Destroy()

    def eliminar_pedido(self, event):
        dialogo = EliminarPedidoDialog(self, self.id_pedido, gestion_pedido)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)  # Cierra el diálogo y recarga la lista
        dialogo.Destroy()
import wx
from module.GestionPedido import GestionPedido

gestion_pedido = GestionPedido()

class EditarPedidoDialog(wx.Dialog):
    def __init__(self, parent, id_pedido):
        super().__init__(parent, title="Editar Pedido", size=(300, 250))
        self.id_pedido = id_pedido

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        pedidos = gestion_pedido.obtener_todos()
        datos = pedidos.get(id_pedido, {})

        # Campos editables
        vbox.Add(wx.StaticText(panel, label="Fecha:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_fecha = wx.TextCtrl(panel, value=datos.get("fecha", ""))
        vbox.Add(self.txt_fecha, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Cliente:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_cliente = wx.TextCtrl(panel, value=datos.get("cliente", ""))
        vbox.Add(self.txt_cliente, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Detalle:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_detalle = wx.TextCtrl(panel, value=datos.get("detalle", ""), style=wx.TE_MULTILINE)
        vbox.Add(self.txt_detalle, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Estado:"), flag=wx.LEFT | wx.TOP, border=10)
        self.combo_estado = wx.ComboBox(panel, choices=["Pendiente", "Realizado", "En Proceso", "Cancelado", "Finalizado"], style=wx.CB_READONLY)
        self.combo_estado.SetValue(datos.get("estado", ""))  # Establecer el valor actual
        vbox.Add(self.combo_estado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        panel.SetSizer(vbox)

        # Bind para el botón "Guardar"
        self.Bind(wx.EVT_BUTTON, self.guardar_cambios, btn_ok)

    def guardar_cambios(self, event):
        fecha = self.txt_fecha.GetValue().strip()
        cliente = self.txt_cliente.GetValue().strip()
        detalle = self.txt_detalle.GetValue().strip()
        estado = self.combo_estado.GetValue().strip()

        if not fecha or not cliente or not detalle or not estado:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            gestion_pedido.editar_pedido(self.id_pedido, fecha, cliente, detalle, estado)
            wx.MessageBox("Pedido actualizado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
            



gestion_pedido = GestionPedido()

class EditarPedidoDialog(wx.Dialog):
    def __init__(self, parent, id_pedido):
        super().__init__(parent, title="Editar Pedido", size=(300, 250))
        self.id_pedido = id_pedido

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        pedidos = gestion_pedido.obtener_todos()
        datos = pedidos.get(id_pedido, {})

        # Campos editables
        vbox.Add(wx.StaticText(panel, label="Fecha:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_fecha = wx.TextCtrl(panel, value=datos.get("fecha", ""))
        vbox.Add(self.txt_fecha, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Cliente:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_cliente = wx.TextCtrl(panel, value=datos.get("cliente", ""))
        vbox.Add(self.txt_cliente, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Detalle:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_detalle = wx.TextCtrl(panel, value=datos.get("detalle", ""), style=wx.TE_MULTILINE)
        vbox.Add(self.txt_detalle, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Estado:"), flag=wx.LEFT | wx.TOP, border=10)
        self.combo_estado = wx.ComboBox(panel, choices=["Pendiente", "Realizado", "En Proceso", "Cancelado", "Finalizado"], style=wx.CB_READONLY)
        self.combo_estado.SetValue(datos.get("estado", ""))  # Establecer el valor actual
        vbox.Add(self.combo_estado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        # Botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        panel.SetSizer(vbox)

        # Bind para el botón "Guardar"
        self.Bind(wx.EVT_BUTTON, self.guardar_cambios, btn_ok)

    def guardar_cambios(self, event):
        fecha = self.txt_fecha.GetValue().strip()
        cliente = self.txt_cliente.GetValue().strip()
        detalle = self.txt_detalle.GetValue().strip()
        estado = self.combo_estado.GetValue().strip()

        if not fecha or not cliente or not detalle or not estado:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            gestion_pedido.editar_pedido(self.id_pedido, fecha, cliente, detalle, estado)
            wx.MessageBox("Pedido actualizado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)
class EliminarPedidoDialog(wx.Dialog):
    def __init__(self, parent, id_pedido, gestion_pedido):
        super().__init__(parent, title="Eliminar Pedido", size=(300, 150))
        self.id_pedido = id_pedido
        self.parent = parent  # Guardamos la referencia al padre para actualizar la lista
        self.gestion_pedido = gestion_pedido  # Guardamos la referencia a la gestión de pedidos

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        pedidos = self.gestion_pedido.obtener_todos()
        pedido = pedidos.get(str(id_pedido))  # Convertimos id_pedido a string por seguridad

        if pedido:
            mensaje = f"¿Estás seguro de que deseas eliminar el pedido con ID '{pedido['id']}'?"
            vbox.Add(wx.StaticText(panel, label=mensaje), flag=wx.ALL, border=10)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            btn_ok = wx.Button(panel, wx.ID_OK, "Eliminar")
            btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
            hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
            hbox.Add(btn_cancel)

            vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
            panel.SetSizer(vbox)

            self.Bind(wx.EVT_BUTTON, self.eliminar_pedido, btn_ok)
        else:
            wx.MessageBox(f"No se encontró el pedido con ID {id_pedido}", "Error", wx.OK | wx.ICON_ERROR)
            self.EndModal(wx.ID_CANCEL)

    def eliminar_pedido(self, event):
        try:
            self.gestion_pedido.eliminar_pedido(self.id_pedido)
            wx.MessageBox("Pedido eliminado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
            if hasattr(self.parent, "cargar_pedidos"):
                self.parent.cargar_pedidos()  # Actualizar la lista de pedidos en la ventana principal
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

import wx
from module.GestionPedido import GestionPedido

gestion_pedido = GestionPedido()

class AgregarPedidoDialog(wx.Dialog):
    def __init__(self, parent, id=None, title="Nuevo Pedido"):
        super().__init__(parent, id=wx.ID_ANY, title=title)

        self.id = id
        self.SetTitle(title)

        vbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        grid = wx.GridBagSizer(5, 5)

        # Fecha
        grid.Add(wx.StaticText(panel, label="Fecha:"), pos=(0, 0), flag=wx.ALL, border=5)
        self.txt_fecha = wx.TextCtrl(panel)
        grid.Add(self.txt_fecha, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Cliente
        grid.Add(wx.StaticText(panel, label="Cliente:"), pos=(1, 0), flag=wx.ALL, border=5)
        self.txt_cliente = wx.TextCtrl(panel)
        grid.Add(self.txt_cliente, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Detalle (multilínea)
        grid.Add(wx.StaticText(panel, label="Detalle:"), pos=(2, 0), flag=wx.ALL, border=5)
        self.txt_detalle = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        grid.Add(self.txt_detalle, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Estado (combo box)
        grid.Add(wx.StaticText(panel, label="Estado:"), pos=(3, 0), flag=wx.ALL, border=5)
        self.combo_estado = wx.ComboBox(panel, choices=["Pendiente", "Realizado", "En Proceso", "Cancelado", "Finalizado"], style=wx.CB_READONLY)
        grid.Add(self.combo_estado, pos=(3, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Botones
        btn_ok = wx.Button(panel, label="Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        btn_ok.Bind(wx.EVT_BUTTON, self.guardar_pedido)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)

        vbox.Add(grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
        self.Centre()

    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("G"):
            self.guardar_pedido(None)
        elif control_presionado and key_code == ord("C"):
            self.Close()
        event.Skip()

    def guardar_pedido(self, event):
        fecha = self.txt_fecha.GetValue().strip()
        cliente = self.txt_cliente.GetValue().strip()
        detalle = self.txt_detalle.GetValue().strip()
        estado = self.combo_estado.GetValue().strip()

        if not fecha or not cliente or not detalle or not estado:
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.")
            return

        gestion_pedido.registrar_pedido(fecha, cliente, detalle, estado)
        print(f"Pedido guardado: Fecha={fecha}, Cliente={cliente}, Detalle={detalle}, Estado={estado}")
        self.mostrar_mensaje("Pedido guardado con éxito.", wx.ICON_INFORMATION)

        self.txt_fecha.SetValue("")
        self.txt_cliente.SetValue("")
        self.txt_detalle.SetValue("")
        self.combo_estado.SetSelection(0) # Selecciona el primer elemento (Pendiente)

    def mostrar_mensaje(self, mensaje, tipo=wx.ICON_ERROR):
        wx.MessageBox(mensaje, "Información", style=tipo)