import wx
import wx.adv
import pandas as pd
from module.GestionVenta import GestionVenta

gestion_venta = GestionVenta()

class ReporteVentasFrame(wx.Frame):
    def __init__(self, parent, title="Reporte de Ventas"):
        super().__init__(parent, title=title, size=(800, 600))
        self.panel = wx.Panel(self)

        # Controles para seleccionar rango de fechas
        self.lbl_fecha_inicio = wx.StaticText(self.panel, label="Fecha Inicio:")
        self.date_picker_inicio = wx.adv.DatePickerCtrl(self.panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)

        self.lbl_fecha_fin = wx.StaticText(self.panel, label="Fecha Fin:")
        self.date_picker_fin = wx.adv.DatePickerCtrl(self.panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)

        self.btn_filtrar = wx.Button(self.panel, label="Filtrar Ventas")
        self.btn_filtrar.Bind(wx.EVT_BUTTON, self.on_filtrar_ventas)

        # Lista accesible para mostrar resultados
        self.list_ctrl = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN)

        # Layout
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(self.lbl_fecha_inicio, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        top_sizer.Add(self.date_picker_inicio, 0, wx.ALL, 5)
        top_sizer.Add(self.lbl_fecha_fin, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        top_sizer.Add(self.date_picker_fin, 0, wx.ALL, 5)
        top_sizer.Add(self.btn_filtrar, 0, wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(top_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        self.panel.SetSizer(main_sizer)
        self.Centre()
        self.Show(True)

        # Cargar ventas al inicio
        self.cargar_ventas()

    def cargar_ventas(self, fecha_inicio=None, fecha_fin=None):
        try:
            df = gestion_venta.obtener_ventas_rango_pandas(fecha_inicio, fecha_fin)
            self.mostrar_dataframe_en_lista(df)
        except Exception as e:
            wx.MessageBox(f"Error al cargar ventas: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def mostrar_dataframe_en_lista(self, df):
        self.list_ctrl.ClearAll()

        if df.empty:
            self.list_ctrl.InsertColumn(0, "Información")
            self.list_ctrl.InsertItem(0, "No se encontraron ventas en el rango seleccionado.")
            return

        # Crear columnas
        for col_idx, col in enumerate(df.columns):
            self.list_ctrl.InsertColumn(col_idx, col, width=150)

        # Agregar filas
        for row_idx, row in df.iterrows():
            index = self.list_ctrl.InsertItem(row_idx, str(row[0]))  # Primera columna
            for col_idx in range(1, len(df.columns)):
                self.list_ctrl.SetItem(index, col_idx, str(row[col_idx]))

        # Ajustar ancho
        for i in range(len(df.columns)):
            self.list_ctrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)

    def on_filtrar_ventas(self, event):
        fecha_inicio = self.date_picker_inicio.GetValue().FormatISODate()
        fecha_fin = self.date_picker_fin.GetValue().FormatISODate()
        self.cargar_ventas(fecha_inicio, fecha_fin)
