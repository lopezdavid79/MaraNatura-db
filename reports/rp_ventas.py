import wx
import wx.grid as gridlib
import wx.adv
import pandas as pd
from datetime import datetime
from module.GestionVenta import GestionVenta  # Importa tu clase GestionVenta
gestion_venta=GestionVenta()
class ReporteVentasFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(800, 600))
        #self.gestion_venta = GestionVenta(nombre_base_datos) # Crea una instancia de GestionVenta

        self.panel = wx.Panel(self)

        # Controles para el rango de fechas
        self.lbl_fecha_inicio = wx.StaticText(self.panel, label="Fecha Inicio:")
        self.date_picker_inicio = wx.adv.DatePickerCtrl(self.panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.lbl_fecha_fin = wx.StaticText(self.panel, label="Fecha Fin:")
        self.date_picker_fin = wx.adv.DatePickerCtrl(self.panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        self.btn_filtrar = wx.Button(self.panel, label="Filtrar Ventas")
        self.btn_filtrar.Bind(wx.EVT_BUTTON, self.on_filtrar_ventas)

        # Cuadrícula para mostrar los resultados
        self.grid = gridlib.Grid(self.panel)

        # Sizer para organizar los controles
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(self.lbl_fecha_inicio, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        top_sizer.Add(self.date_picker_inicio, 0, wx.ALL, 5)
        top_sizer.Add(self.lbl_fecha_fin, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        top_sizer.Add(self.date_picker_fin, 0, wx.ALL, 5)
        top_sizer.Add(self.btn_filtrar, 0, wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(top_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(self.grid, 1, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(main_sizer)

        self.cargar_ventas() # Cargar todas las ventas al inicio

        self.Centre()
        self.Show(True)

    def cargar_ventas(self, fecha_inicio=None, fecha_fin=None):
        try:
            df = gestion_venta.obtener_ventas_rango_pandas(fecha_inicio, fecha_fin)
            self.mostrar_dataframe_en_grid(df)
        except Exception as e:
            wx.MessageBox(f"Error al cargar ventas: {e}", "Error", wx.OK | wx.ICON_ERROR)

    def mostrar_dataframe_en_grid(self, df):
        self.grid.ClearGrid()
        if not df.empty:
            self.grid.CreateGrid(len(df), len(df.columns))
            for col_num, col_name in enumerate(df.columns):
                self.grid.SetColLabelValue(col_num, col_name)
                for row_num, value in enumerate(df[col_name]):
                    self.grid.SetCellValue(row_num, col_num, str(value))
            self.grid.AutoSizeColumns()
        else:
            self.grid.CreateGrid(1, 1)
            self.grid.SetCellValue(0, 0, "No se encontraron ventas en el rango seleccionado.")
            self.grid.AutoSize()

    def on_filtrar_ventas(self, event):
        fecha_inicio = self.date_picker_inicio.GetValue().FormatISODate()
        fecha_fin = self.date_picker_fin.GetValue().FormatISODate()
        self.cargar_ventas(fecha_inicio, fecha_fin)
