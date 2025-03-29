import wx.adv
import sys
import os

class ReproductorSonido:
    """Clase para gestionar la reproducción de sonidos en la aplicación."""

    @staticmethod
    def reproducir(archivo):
        """Reproduce un archivo de sonido .wav si es válido."""
        try:
            # Construye la ruta absoluta al archivo de sonido
            ruta_base = getattr(sys, '_MEIPASS', os.path.abspath('.'))
            ruta_sonido = os.path.join(ruta_base, 'Sounds', archivo)

            sonido = wx.adv.Sound(ruta_sonido)
            if sonido.IsOk():
                sonido.Play(wx.adv.SOUND_ASYNC)  # Reproduce sin bloquear la app
            else:
                print(f"Error: No se pudo cargar el archivo de sonido '{ruta_sonido}'.")
        except Exception as e:
            print(f"Error al reproducir sonido: {e}")