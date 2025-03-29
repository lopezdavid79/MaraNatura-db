import wx

# Crear un nuevo tipo de evento
EVT_ACTUALIZAR_PRODUCTOS_TYPE = wx.NewEventType()

# Crear un Binder para poder usar en Bind()
EVT_ACTUALIZAR_PRODUCTOS = wx.PyEventBinder(EVT_ACTUALIZAR_PRODUCTOS_TYPE, 1)

# Definir la clase del evento personalizado
class ActualizarProductosEvent(wx.PyCommandEvent):  # PyCommandEvent permite propagación
    def __init__(self, id=wx.ID_ANY):
        super().__init__(EVT_ACTUALIZAR_PRODUCTOS_TYPE, id)
