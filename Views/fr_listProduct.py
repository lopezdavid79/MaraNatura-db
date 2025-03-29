import wx
import wx.lib.mixins.listctrl as listmix
from module.eventos import EVT_ACTUALIZAR_PRODUCTOS, ActualizarProductosEvent
from module.ReproductorSonido import ReproductorSonido
from module.GestionProducto import GestionProducto
from Views.fr_producto import VentanaProducto
from Views.fr_listSale import AgregarVentaDialog

gestion_producto= GestionProducto()

class ListProducto(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=None, title="Nuevo Producto", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)
        self.parent_venta = parent
        panel = wx.Panel(self)
        self.Bind(EVT_ACTUALIZAR_PRODUCTOS, lambda event: self.actualizar_lista_productos(event))

        # Campo de búsqueda
        label_buscar = wx.StaticText(panel, label="Buscar Producto:", pos=(10, 245))
        self.search_ctrl = wx.TextCtrl(panel, pos=(10, 270), size=(200, -1), style=wx.TE_PROCESS_ENTER)
        self.search_ctrl.Bind(wx.EVT_TEXT_ENTER, self.buscar_productos)  # Vincular Enter
       
        btn_buscar = wx.Button(panel, label="Buscar", pos=(220, 270))
        btn_buscar.Bind(wx.EVT_BUTTON, self.buscar_productos)

        # Crear la lista de productos
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(460, 250))
        self.list_ctrl.InsertColumn(0, 'Producto', width=50)
        self.list_ctrl.InsertColumn(1, 'Código', width=150)
        self.list_ctrl.InsertColumn(2, 'Stock', width=80)
        self.list_ctrl.InsertColumn(3, 'Precio', width=80)

        # Cargar productos en la lista
        self.cargar_productos()

        # Evento para detectar tecla Enter
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mostrar_detalle_producto)

        # Botón para agregar producto
        btn_nuevo = wx.Button(panel, label="Nuevo Producto", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)

        # Botón para cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.on_close)

        # Botón para actualizar
        btn_actual = wx.Button(panel, label="Actualizar", pos=(150, 300))
        btn_actual.Bind(wx.EVT_BUTTON, self.actualizar_lista_productos)

        # Capturar eventos de teclado
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

        self.Show()

    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("N"):  # Ctrl + N
            self.abrir_dialogo_nuevo(None)
        elif control_presionado and key_code == ord("C"):  # Ctrl + C -> Cerrar ventana
            self.on_close(None)
        event.Skip()  # Permitir que otros eventos se procesen

    def cargar_productos(self, nombre_busqueda=None):
        self.list_ctrl.DeleteAllItems()
        productos = gestion_producto.obtener_todos()

        if not isinstance(productos, dict):  # Verifica si productos es un diccionario
            print("❌ Error: `obtener_todos()` no devolvió un diccionario")
            return

        for id_producto, datos_producto in productos.items():
            id_producto = int(id_producto)  # Convierte el ID a entero
            nombre = datos_producto["nombre"]
            detalle = datos_producto["detalle"]
            stock = datos_producto["stock"]
            precio = datos_producto["precio"]

            # Aquí puedes agregar los productos a self.list_ctrl
            self.list_ctrl.Append((nombre, id_producto, stock, precio))

#mostrar el detalle del producto
    def mostrar_detalle_producto(self, event):
        index = event.GetIndex()
        # El ID del producto está en la segunda columna (índice 1)
        id_producto = int(self.list_ctrl.GetItemText(index, 1))

        datos= gestion_producto.buscar_producto(id_producto)
        if datos:            
            dialogo = DetalleProductoDialog(self, id_producto, datos)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_productos()
        else:
            print(f"❌ Error: Producto con ID {id_producto} no encontrado")


    def abrir_dialogo_nuevo(self, event):
        dialogo = VentanaProducto(self)
        dialogo.ShowModal()
        dialogo.Destroy()
        self.cargar_productos()

    def on_close(self, event):
        self.Close()

    def actualizar_lista_productos(self, event=None):
        self.cargar_productos()

    def buscar_productos(self, event):
        nombre_busqueda = self.search_ctrl.GetValue()
        self.cargar_productos(nombre_busqueda)

class DetalleProductoDialog(wx.Dialog):
    def __init__(self, parent, id_producto, producto):
        super().__init__(parent, title=f"Detalle del Producto {id_producto}", size=(300, 200))
        panel = wx.Panel(self)
        # Aquí puedes agregar los controles para mostrar los detalles del producto
        # ...

if __name__ == '__main__':
    app = wx.App(False)
    frame = ListProducto(None)
    app.MainLoop()
    def abrir_dialogo_nuevo(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        dialogo = AgregarProductoDialog(self)
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_producto()  # Actualiza la lista después de agregar una venta
        dialogo.Destroy()
    
    def cerrar_ventana(self, event):
        print("Producto agregado, actualizando lista...")
        self.cargar_productos()
        event.Skip()  # Permitir que la ventana se cierre normalmente

    def actualizar_lista_productos(self,event):
        ReproductorSonido.reproducir("refresh.wav")
        self.list_ctrl.DeleteAllItems()  # Limpiar la lista antes de cargar nuevos productos
        self.cargar_productos()   #Vuelve a cargar los productos del archivo JSON        
        #print("Productos obtenidos:", productos)  # 🛠️ Depuración
        
            
    def on_close(self, event):
        ReproductorSonido.reproducir("screenCurtainOff.wav")
        self.Close()
    
    

class DetalleProductoDialog(wx.Dialog):
    def __init__(self, parent, id_producto, datos):
        super().__init__(parent, title="Detalle del Producto", size=(300, 250))
        self.id_producto = id_producto

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Mostrar detalles
        vbox.Add(wx.StaticText(panel, label=f"Código: {id_producto}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Nombre: {datos['nombre']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Detalle: {datos.get('detalle', 'No disponible')}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Stock: {datos['stock']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Precio: {datos['precio']}"), flag=wx.LEFT | wx.TOP, border=10)

        # Botón para editar
        btn_editar = wx.Button(panel, label="Editar")
        btn_editar.Bind(wx.EVT_BUTTON, self.editar_producto)
#boton para eliminar 
        btn_delete = wx.Button(panel, label="Eliminar")
        btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_producto)
        # Botón para cerrar
        btn_cerrar = wx.Button(panel, wx.ID_CANCEL, "Cerrar")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_editar, flag=wx.RIGHT, border=10)
        hbox.Add(btn_delete, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cerrar)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def editar_producto(self, event):
        dialogo = EditarProductoDialog(self, self.id_producto)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)  # Cierra el diálogo y recarga la lista
        dialogo.Destroy()



    def eliminar_producto(self, event):
            dialogo = EliminarProductoDialog(self, self.id_producto,gestion_producto)
            if dialogo.ShowModal() == wx.ID_OK:
                self.EndModal(wx.ID_OK)  # Cierra el diálogo y recarga la lista
            dialogo.Destroy()




class EditarProductoDialog(wx.Dialog):
    def __init__(self, parent, id_producto):
        super().__init__(parent, title="Editar Producto", size=(300, 250))
        self.id_producto = id_producto

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        productos = gestion_producto.obtener_todos()
        # Buscar el producto por ID en la lista
        producto = productos.get(str(id_producto), {})  # Obtén el producto por ID

        # Si el producto existe, cargamos sus datos
        if producto:
            # Campos editables
            vbox.Add(wx.StaticText(panel, label="Nombre:"), flag=wx.LEFT | wx.TOP, border=10)
            self.txt_nombre = wx.TextCtrl(panel, value=producto.get("nombre", ""))
            vbox.Add(self.txt_nombre, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
            
            vbox.Add(wx.StaticText(panel, label="Detalle:"), flag=wx.LEFT | wx.TOP, border=10)
            self.txt_detalle= wx.TextCtrl(panel, value=producto.get("detalle", ""))
            vbox.Add(self.txt_detalle, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

            vbox.Add(wx.StaticText(panel, label="Stock:"), flag=wx.LEFT | wx.TOP, border=10)
            self.txt_stock = wx.TextCtrl(panel, value=str(producto.get("stock", "")))
            vbox.Add(self.txt_stock, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

            vbox.Add(wx.StaticText(panel, label="Precio:"), flag=wx.LEFT | wx.TOP, border=10)
            self.txt_precio = wx.TextCtrl(panel, value=str(producto.get("precio", "")))
            vbox.Add(self.txt_precio, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

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
        else:
            wx.MessageBox(f"No se encontró el producto con ID {id_producto}", "Error", wx.OK | wx.ICON_ERROR)

    def guardar_cambios(self, event):
        nombre = self.txt_nombre.GetValue()
        detalle= self.txt_detalle.GetValue()
        stock = self.txt_stock.GetValue()
        precio = self.txt_precio.GetValue()

        if not nombre or not detalle or not stock or not precio:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            stock = int(stock)
            precio = float(precio)
            gestion_producto.editar_producto(self.id_producto, nombre,detalle,stock, precio)
            wx.MessageBox("Producto actualizado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except ValueError:
            wx.MessageBox("Stock debe ser un número entero y precio un número válido", "Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)



#eliminar producto
class EliminarProductoDialog(wx.Dialog):
    def __init__(self, parent, id_producto, gestion_productos):
        super().__init__(parent, title="Eliminar Producto", size=(300, 150))
        self.id_producto = id_producto
        self.parent = parent  # Guardamos la referencia al padre para actualizar la lista
        self.gestion_producto= gestion_producto # Guardamos la referencia a la gestión de productos

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        productos = self.gestion_productos.obtener_todos()
        producto = next((p for p in productos if p["id"] == id_producto), None)

        if producto:
            mensaje = f"¿Estás seguro de que deseas eliminar el producto '{producto['nombre']}'?"
            vbox.Add(wx.StaticText(panel, label=mensaje), flag=wx.ALL, border=10)
            
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            btn_ok = wx.Button(panel, wx.ID_OK, "Eliminar")
            btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
            hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
            hbox.Add(btn_cancel)
            
            vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
            panel.SetSizer(vbox)
            
            self.Bind(wx.EVT_BUTTON, self.eliminar_producto, btn_ok)
        else:
            wx.MessageBox(f"No se encontró el producto con ID {id_producto}", "Error", wx.OK | wx.ICON_ERROR)
            self.EndModal(wx.ID_CANCEL)

    def eliminar_producto(self, event):
        try:
            self.gestion_productos.eliminar_producto(self.id_producto)
            wx.MessageBox("Producto eliminado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
            if hasattr(self.parent, "cargar_productos"):
                self.parent.cargar_productos()  # Actualizar la lista de productos en la ventana principal
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

class AgregarProductoDialog(wx.Dialog):
    def __init__(self, parent, id=None, title="Nuevo Producto", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        self.id = id  
        self.SetTitle(title)

        # Panel principal
        panel = wx.Panel(self)

        # Crear el sizer principal antes de los campos
        sizer_principal = wx.BoxSizer(wx.VERTICAL)

        # Definición de los campos de entrada (ahora incluimos el sizer principal en la llamada)
        self.txt_id = self.crear_campo(panel, "Código:", sizer_principal)
        self.txt_producto = self.crear_campo(panel, "Producto:", sizer_principal)
        self.txt_detalle = self.crear_campo(panel, "Detalle:", sizer_principal)
        self.txt_stock = self.crear_campo(panel, "Stock:", sizer_principal)
        self.txt_precio = self.crear_campo(panel, "Precio:", sizer_principal)

        # Botones de acción
        btn_guardar = wx.Button(panel, label="Guardar")
        btn_guardar.Bind(wx.EVT_BUTTON, self.guardar_producto)
        btn_cerrar = wx.Button(panel, label="Cerrar")
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)

        # Añadir botones al sizer
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer.Add(btn_guardar, 0, wx.ALL, 5)
        btn_sizer.Add(btn_cerrar, 0, wx.ALL, 5)
        sizer_principal.Add(btn_sizer, 0, wx.CENTER)

        # Área de mensajes
        self.lbl_mensaje = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER)
        sizer_principal.Add(self.lbl_mensaje, 0, wx.ALL | wx.EXPAND, 5)

        # Configurar el panel y el sizer
        panel.SetSizer(sizer_principal)
        panel.Layout()

        # Capturar eventos de teclado
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)

        self.Show()

    def crear_campo(self, panel, label, sizer_principal):
        """Función auxiliar para crear etiquetas y campos de entrada y añadirlos al sizer principal."""
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        static_text = wx.StaticText(panel, label=label, size=(80, -1))
        text_ctrl = wx.TextCtrl(panel, size=(200, -1))
        
        sizer.Add(static_text, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        # Agregar el sizer de cada campo al sizer principal
        sizer_principal.Add(sizer, 0, wx.ALL | wx.EXPAND, 5)
        
        return text_ctrl  # Devolver el wx.TextCtrl en lugar del BoxSizer

    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("G"):  # Ctrl + G
            self.guardar_producto(None)
        elif control_presionado and key_code == ord("C"):  # Ctrl + C -> Cerrar ventana
            self.cerrar_ventana(None)

        event.Skip()

    def guardar_producto(self, event):
        id_producto = self.txt_id.GetValue()
        nombre = self.txt_producto.GetValue()
        detalle = self.txt_detalle.GetValue()
        stock = self.txt_stock.GetValue()
        precio = self.txt_precio.GetValue()

        # Validación de campos vacíos
        if not all([id_producto, nombre, detalle, stock, precio]):
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.")
            return

        # Validación de tipos de datos
        try:
            id_producto = int(id_producto)
            stock = int(stock)
            precio = float(precio)
        except ValueError:
            self.mostrar_mensaje("Error: ID, Stock y Precio deben ser números.")
            return

        # Validación de ID positivo
        if id_producto <= 0:
            self.mostrar_mensaje("Error: El ID debe ser un número positivo.")
            return

        # Verificar si el ID ya existe
        if gestion_producto.existe_producto(id_producto):
            self.mostrar_mensaje("Error: Ya existe un producto con ese ID.")
            return

        # Agregar el producto
        gestion_producto.agregar_producto(id_producto, nombre, detalle, stock, precio)

        print(f"Producto guardado: ID={id_producto}, Producto={nombre}, Stock={stock}, Precio={precio}")
        ReproductorSonido.reproducir("Ok.wav")

        wx.MessageBox("Producto guardado con éxito.", "Éxito", wx.OK | wx.ICON_INFORMATION)

        # Limpiar campos
        self.txt_id.SetValue("")
        self.txt_producto.SetValue("")
        self.txt_detalle.SetValue("")
        self.txt_stock.SetValue("")
        self.txt_precio.SetValue("")

    def mostrar_mensaje(self, mensaje, tipo=wx.ICON_ERROR):
        wx.MessageBox(mensaje, "Error", style=tipo)

    def cerrar_ventana(self, event):
        self.Close()
