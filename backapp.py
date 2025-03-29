import wx
import os
import shutil
import zipfile
import datetime

class BackupFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(600, 450))  # Aumenta el tamaño para el botón de salir

        self.panel = wx.Panel(self)

        # Controles para seleccionar archivos
        wx.StaticText(self.panel, label="Archivos a respaldar:", pos=(10, 10))
        self.archivos_listbox = wx.ListBox(self.panel, pos=(10, 30), size=(300, 100), style=wx.LB_MULTIPLE)
        self.seleccionar_archivos_btn = wx.Button(self.panel, label="Seleccionar archivos", pos=(320, 30))
        self.seleccionar_archivos_btn.Bind(wx.EVT_BUTTON, self.on_seleccionar_archivos)

        # Control para seleccionar carpeta de destino
        wx.StaticText(self.panel, label="Carpeta de destino:", pos=(10, 140))
        self.carpeta_destino_text = wx.TextCtrl(self.panel, pos=(10, 160), size=(300, 25), style=wx.TE_READONLY)
        self.seleccionar_carpeta_btn = wx.Button(self.panel, label="Seleccionar carpeta", pos=(320, 160))
        self.seleccionar_carpeta_btn.Bind(wx.EVT_BUTTON, self.on_seleccionar_carpeta)

        # Botón para iniciar la copia de seguridad
        self.iniciar_backup_btn = wx.Button(self.panel, label="Iniciar copia de seguridad", pos=(10, 200))
        self.iniciar_backup_btn.Bind(wx.EVT_BUTTON, self.on_iniciar_backup)

        # Botón para salir
        self.salir_btn = wx.Button(self.panel, label="Salir", pos=(10, 240))  # Agregado el botón de salir
        self.salir_btn.Bind(wx.EVT_BUTTON, self.on_salir)

        # Barra de estado
        self.statusbar = self.CreateStatusBar()

    def on_seleccionar_archivos(self, event):
        """Abre un diálogo para seleccionar múltiples archivos."""
        with wx.FileDialog(self, "Seleccionar archivos", wildcard="Todos los archivos (*.*)|*.*", style=wx.FD_OPEN | wx.FD_MULTIPLE) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                rutas_archivos = dialog.GetPaths()
                self.archivos_listbox.Set(rutas_archivos)

    def on_seleccionar_carpeta(self, event):
        """Abre un diálogo para seleccionar una carpeta."""
        with wx.DirDialog(self, "Seleccionar carpeta de destino") as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                ruta_carpeta = dialog.GetPath()
                self.carpeta_destino_text.SetValue(ruta_carpeta)

    def on_iniciar_backup(self, event):
        """Inicia el proceso de copia de seguridad."""
        rutas_archivos = self.archivos_listbox.GetStrings()
        ruta_carpeta_destino = self.carpeta_destino_text.GetValue()

        if not rutas_archivos or not ruta_carpeta_destino:
            wx.MessageBox("Por favor, seleccione archivos y una carpeta de destino.", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            self.statusbar.SetStatusText("Creando copia de seguridad...", 0)
            self.crear_copia_seguridad(rutas_archivos, ruta_carpeta_destino)
            self.statusbar.SetStatusText("Copia de seguridad creada con éxito.", 0)
            wx.MessageBox("Copia de seguridad creada con éxito.", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            self.statusbar.SetStatusText("Error al crear la copia de seguridad.", 0)
            wx.MessageBox(f"Error al crear la copia de seguridad:\n{e}", "Error", wx.OK | wx.ICON_ERROR)

    def crear_copia_seguridad(self, rutas_archivos, ruta_carpeta_destino):
        """Crea una copia de seguridad comprimida de los archivos."""
        nombre_archivo_zip = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        ruta_archivo_zip = os.path.join(ruta_carpeta_destino, nombre_archivo_zip)

        with zipfile.ZipFile(ruta_archivo_zip, 'w', zipfile.ZIP_DEFLATED) as archivo_zip:
            for ruta_archivo in rutas_archivos:
                archivo_zip.write(ruta_archivo, os.path.basename(ruta_archivo))

    def on_salir(self, event):
        """Cierra la aplicación."""
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    frame = BackupFrame(None, "Copia de Seguridad")
    frame.Show()
    app.MainLoop()