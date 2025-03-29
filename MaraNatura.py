import wx
import os
import sys
from module.ReproductorSonido import ReproductorSonido 
from Views.fr_menu import Principal  # Asegúrate de que la ruta sea correcta

class MyApp(wx.App):
    def OnInit(self):
        self.frame = Principal(None, title="My App")
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

    def Reiniciar(self):
        self.frame.Close()  # Cierra la ventana principal
        python = sys.executable
        os.execl(python, python, *sys.argv)  # Reemplaza el proceso actual

class Principal(Principal): # Aseguramos que Principal herede de Principal de fr_menu.py
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        # Asegúrate de tener un botón o un evento que llame a self.OnReiniciar()
        # Ejemplo:
        #boton_reiniciar = wx.Button(self, label="Reiniciar", pos=(10, 10))
        #boton_reiniciar.Bind(wx.EVT_BUTTON, self.OnReiniciar)

    def OnReiniciar(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        app = wx.GetApp()
        app.Reiniciar()

if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()