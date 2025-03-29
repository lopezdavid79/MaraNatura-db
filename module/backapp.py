import wx
import datetime
import os

def crear_copia_seguridad(ruta_archivo_original, ruta_carpeta_destino):
    """Crea una copia de seguridad comprimida del archivo."""
    try:
        nombre_archivo = os.path.basename(ruta_archivo_original)
        fecha_hora_actual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo_backup = f"{nombre_archivo}_{fecha_hora_actual}.zip"
        ruta_backup = os.path.join(ruta_carpeta_destino, nombre_archivo_backup)

        # Aquí iría tu lógica para crear la copia de seguridad comprimida
        # ...

        # Simulación de la creación de la copia de seguridad
        print(f"Creando copia de seguridad en: {ruta_backup}")  # Reemplaza con tu lógica real

        # Mensaje de éxito con wxPython
        wx.MessageBox(
            f"Copia de seguridad creada con éxito en:\n{ruta_backup}",
            "Copia de seguridad creada",
            wx.OK | wx.ICON_INFORMATION,
        )

    except Exception as e:
        wx.MessageBox(
            f"Error al crear la copia de seguridad:\n{e}",
            "Error",
            wx.OK | wx.ICON_ERROR,
        )

# Ejemplo de uso
if __name__ == '__main__':
    app = wx.App()
    ruta_archivo_original = "mi_archivo.txt"  # Reemplaza con la ruta de tu archivo
    ruta_carpeta_destino = "backups"  # Reemplaza con la ruta de tu carpeta de destino

    # Asegurarse de que el directorio de copias de seguridad existe
    if not os.path.exists(ruta_carpeta_destino):
        os.makedirs(ruta_carpeta_destino)

    crear_copia_seguridad(ruta_archivo_original, ruta_carpeta_destino)
    app.MainLoop()