import wx
import re
from module.GestionCliente import GestionCliente
from module.GestionProducto import GestionProducto
from module.GestionVenta import GestionVenta
from module.ReproductorSonido import ReproductorSonido

gestion_cliente = GestionCliente()
gestion_producto = GestionProducto()



class ConfirmacionVentaDialog(wx.Dialog):
    def __init__(self, parent, cliente, productos, total_venta):
        super().__init__(parent, title="Confirmar Venta", size=(400, 300))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Cliente
        vbox.Add(wx.StaticText(panel, label=f"Cliente: {cliente}"), flag=wx.LEFT | wx.TOP, border=10)

        # Productos
        vbox.Add(wx.StaticText(panel, label="Productos:"), flag=wx.LEFT | wx.TOP, border=10)
        for producto in productos:
            vbox.Add(wx.StaticText(panel, label=f"- {producto['descripcion']} (Cantidad: {producto['cantidad']})"), flag=wx.LEFT, border=20)

        # Total
        vbox.Add(wx.StaticText(panel, label=f"Total: ${total_venta:.2f}"), flag=wx.LEFT | wx.TOP, border=10)

        # Botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_confirmar = wx.Button(panel, wx.ID_YES, "Confirmar")
        btn_cancelar = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        hbox.Add(btn_confirmar, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancelar)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)
        self.Center()

        # Enlazar eventos de los botones
        self.Bind(wx.EVT_BUTTON, self.on_confirmar, btn_confirmar)
        self.Bind(wx.EVT_BUTTON, self.on_cancelar, btn_cancelar)

    def on_confirmar(self, event):
        self.EndModal(wx.ID_YES)

    def on_cancelar(self, event):
        self.EndModal(wx.ID_CANCEL)

    @staticmethod
    def mostrar_confirmacion(parent, cliente, productos, total_venta):
        dialog = ConfirmacionVentaDialog(parent, cliente, productos, total_venta)
        resultado = dialog.ShowModal()
        dialog.Destroy()
        return resultado == wx.ID_YES