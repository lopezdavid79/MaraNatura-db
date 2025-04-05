import wx
import wx.adv
import pandas as pd
from datetime import date

ventas = pd.DataFrame({
    'Fecha': [date(2025, 4, 1), date(2025, 4, 2), date(2025, 4, 3)],
    'Cliente': ['Juan Pérez', 'Ana Torres', 'Luis Gómez'],
    'Producto': ['Zapatillas', 'Remera', 'Pantalón'],
    'Talla': ['42', 'M', 'L']
})

class ReporteAccesible(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(650, 400))

        self.ventas_df = ventas.copy()
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Selector de fecha
        filtro_box = wx.BoxSizer(wx.HORIZONTAL)
        filtro_box.Add(wx.StaticText(panel, label="Filtrar por fecha:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.date_picker = wx.adv.DatePickerCtrl(panel)
        btn_filtrar = wx.Button(panel, label="Filtrar")
        btn_filtrar.Bind(wx.EVT_BUTTON, self.filtrar)
        filtro_box.Add(self.date_picker, 0, wx.RIGHT, 10)
        filtro_box.Add(btn_filtrar)

        vbox.Add(filtro_box, 0, wx.ALL, 10)

        # Lista accesible
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        for col, label in enumerate(['Fecha', 'Cliente', 'Producto', 'Talla']):
            self.list_ctrl.InsertColumn(col, label, width=150)

        vbox.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        # Botón exportar
        btn_exportar = wx.Button(panel, label="Exportar a Excel")
        btn_exportar.Bind(wx.EVT_BUTTON, self.exportar)
        vbox.Add(btn_exportar, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

        self.mostrar_datos(self.ventas_df)

    def mostrar_datos(self, df):
        self.list_ctrl.DeleteAllItems()
        for _, row in df.iterrows():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(row['Fecha']))
            self.list_ctrl.SetItem(index, 1, row['Cliente'])
            self.list_ctrl.SetItem(index, 2, row['Producto'])
            self.list_ctrl.SetItem(index, 3, row['Talla'])

    def filtrar(self, event):
        wx_date = self.date_picker.GetValue()
        fecha_dt = date(wx_date.GetYear(), wx_date.GetMonth() + 1, wx_date.GetDay())
        filtrado = ventas[ventas['Fecha'] == fecha_dt]
        self.ventas_df = filtrado
        self.mostrar_datos(filtrado)

    def exportar(self, event):
        with wx.FileDialog(self, "Guardar Excel", wildcard="Archivos Excel (*.xlsx)|*.xlsx",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            ruta = dlg.GetPath()
            try:
                self.ventas_df.to_excel(ruta, index=False)
                wx.MessageBox("¡Exportado con éxito!", "OK", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error al exportar:\n{e}", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    ReporteAccesible(None, "Reporte de Ventas Accesible")
    app.MainLoop()
