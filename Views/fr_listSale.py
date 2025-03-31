from Views.dl_ConfirmarVenta import ConfirmacionVentaDialog
import sys
import os
import datetime
import re
import wx
import wx.lib.mixins.listctrl as listmix
import wx.adv
from module.eventos import EVT_ACTUALIZAR_PRODUCTOS, ActualizarProductosEvent  # Importar el evento
from module.ReproductorSonido import ReproductorSonido
from module.GestionCliente import GestionCliente
from module.GestionVenta import GestionVenta, Venta
from module.Productos import Producto  # Asegurar que importamos la gestión de productos
from module.GestionProducto import  GestionProducto  # Asegurar que importamos la gestión de productos
import re
Producto  # Asegurar que importamos la gestión de productos
# Inicialización de la gestión de ventas y productos
gestion_cliente = GestionCliente()
gestion_producto = GestionProducto()
gestion_venta = GestionVenta()

class ListSale(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=None, title="Ventas", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        panel = wx.Panel(self)
        
        # Crear la lista de ventas
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(460, 250))
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'Fecha', width=100)
        self.list_ctrl.InsertColumn(2, 'Cliente', width=150)        
        self.list_ctrl.InsertColumn(3, 'Total', width=100)
        
        self.cargar_ventas()
        
        # Evento para doble clic en una venta
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mostrar_detalle_ventas)

        # Botón para agregar venta
        btn_nuevo = wx.Button(panel, label="Nueva Venta", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)
        
        # Botón para cerrar
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        
        self.Show()
    
    def cargar_ventas(self):
        self.list_ctrl.DeleteAllItems()  # Limpiar la lista antes de cargar nuevas ventas
        ventas = gestion_venta.obtener_todos()

        for id_venta, datos in ventas.items():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(id_venta))
            self.list_ctrl.SetItem(index, 1, datos["fecha"])
            cliente=gestion_cliente.buscar_cliente(datos["id_cliente"])            
            self.list_ctrl.SetItem(index, 2, str(cliente["nombre"]))
            self.list_ctrl.SetItem(index, 3, str(datos["total"]))  # Ahora sí muestra el total
    
    def mostrar_detalle_ventas(self, event):
        
        index = event.GetIndex()
        id_venta = self.list_ctrl.GetItemText(index)

        datos= gestion_venta.buscar_venta(id_venta)
        

        if not datos:  # Verifica si el diccionario está vacío
            wx.MessageBox("No hay productos disponibles para mostrar.", "Error", wx.OK | wx.ICON_ERROR) 
            print("no hay productos ")
        if datos:            
            print("Datos de la venta antes de pasar al diálogo:", datos)  # Depurar aquí
            dialogo = DetalleVentaDialog(self, id_venta, datos)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_ventas()  # Actualizar la lista
    
    def abrir_dialogo_nuevo(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        dialogo = AgregarVentaDialog(self,gestion_venta        )
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_ventas()  # Actualiza la lista después de agregar una venta        
        dialogo.Destroy()

    def cerrar_ventana(self, event):
        ReproductorSonido.reproducir("screenCurtainOff.wav")
        self.Close()


class DetalleVentaDialog(wx.Dialog):
    def __init__(self, parent, id_venta, datos):
        super().__init__(parent, title="Detalle de Venta", size=(500, 400))
        
        # Guardamos el diccionario de productos y otros datos necesarios
        
        self.id_venta = id_venta
        self.datos = datos
        
        # Panel de la ventana
        panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Mostrar detalles de la venta
        self.lista_productos = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.sizer.Add(self.lista_productos, 1, flag=wx.EXPAND|wx.ALL, border=5)
        cliente=gestion_cliente.buscar_cliente(self.datos.id_cliente)
        #print(f"Tipo de cliente: {type(cliente)}")
        #print(f"nombre del cliente: {cliente['nombre']}")
        self.lbl_cliente = wx.StaticText(panel, label=f"Cliente: {cliente['nombre']}")
        self.sizer.Add(self.lbl_cliente, 0, flag=wx.ALL, border=5)

        self.lbl_total = wx.StaticText(panel, label=f"Total: ${self.datos.total}")
        self.sizer.Add(self.lbl_total, 0, flag=wx.ALL, border=5)

        # Cargar los productos seleccionados en la venta
        print(f"datos:{self.datos.__dict__}")
        self.cargar_productos()
    # Botón para cerrar el diálogo
        self.btn_cerrar = wx.Button(panel, label="Cerrar")
        self.sizer.Add(self.btn_cerrar, 0, flag=wx.CENTER|wx.ALL, border=5)

            # Bind the close button to the Close method
        self.btn_cerrar.Bind(wx.EVT_BUTTON, self.on_cerrar)

        panel.SetSizerAndFit(self.sizer)

    def cargar_productos(self):
        """Carga los productos en la lista del diálogo de detalle."""
        # Recorremos los productos asociados a la venta
        for producto_info in self.datos.productos:
            producto_id = producto_info["id_producto"]
            cantidad = producto_info["cantidad"]

            # Buscar el producto en gestion_productos
            producto = gestion_producto.buscar_producto(producto_id)

            if producto:
                item_text = f"ID: {producto['id']} - {producto['nombre']} - Cantidad: {cantidad} - Precio: ${producto['precio']}"
                self.lista_productos.Append(item_text)
            else:
                print(f"Error: Producto con ID {producto_id} no encontrado.")


    def on_cerrar(self, event):
            self.EndModal(wx.ID_OK)  # Cierra el diálogo cuando se hace clic en el botón "Cerrar"



# Clase para agregar una nueva venta con selección de producto por nombre
import wx.lib.newevent
# 🔥 Crear un evento personalizado para actualizar la lista de productos en otra ventana
ActualizarProductosEvent, EVT_ACTUALIZAR_PRODUCTOS = wx.lib.newevent.NewEvent()

class AgregarVentaDialog(wx.Dialog):
    def __init__(self, parent,gestion_ventas):
        super().__init__(parent, title="Nueva Venta", size=(400, 400))      
        self.parent_productos = parent  # Referencia a la ventana de productos
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.nombre_archivo_productos = 'data/productos.json'
        self.gestion_ventas=gestion_ventas

        
                # Fecha
        fecha_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_fecha_venta = wx.StaticText(panel, label="Fecha:")
        self.date_picker_venta = wx.adv.DatePickerCtrl(panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        fecha_sizer.Add(lbl_fecha_venta, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
        fecha_sizer.Add(self.date_picker_venta, flag=wx.EXPAND)
        vbox.Add(fecha_sizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Cliente
        vbox.Add(wx.StaticText(panel, label="Cliente:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_cliente = wx.SearchCtrl(panel, style=wx.TE_PROCESS_ENTER)
        vbox.Add(self.txt_cliente, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        
        self.lista_clientes = wx.ListBox(panel, style=wx.LB_SINGLE)
        vbox.Add(self.lista_clientes, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)
        self.txt_cliente.Bind(wx.EVT_TEXT, self.filtrar_clientes)
        #self.lista_clientes.Bind(wx.EVT_LISTBOX, self.seleccionar_cliente)
        self.txt_cliente.Bind(wx.EVT_KEY_DOWN, self.on_key_cliente)  # Detectar Enter y navegación
        
        self.cargar_clientes()

        # Buscar Producto
        vbox.Add(wx.StaticText(panel, label="Buscar Producto:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_buscar_producto = wx.TextCtrl(panel)
        vbox.Add(self.txt_buscar_producto, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.txt_buscar_producto.Bind(wx.EVT_TEXT, self.filtrar_productos)

        # Lista de productos
        self.list_productos = wx.ListBox(panel, style=wx.LB_SINGLE)
        vbox.Add(self.list_productos, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)
        self.list_productos.SetFocus()  # Establecer el foco en la lista  
        self.list_productos.Bind(wx.EVT_LISTBOX_DCLICK, self.agregar_producto)
        self.list_productos.Bind(wx.EVT_KEY_DOWN, self.navegar_productos)

        # Productos seleccionados
        vbox.Add(wx.StaticText(panel, label="Productos seleccionados:"), flag=wx.LEFT | wx.TOP, border=10)
        self.list_productos_seleccionados = wx.ListBox(panel, style=wx.LB_SINGLE)
        vbox.Add(self.list_productos_seleccionados, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10, proportion=1)

        # Botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        self.btn_eliminar_producto = wx.Button(panel, label="Eliminar Producto")
        self.btn_agregar_producto = wx.Button(panel, label="Agregar Producto")
        hbox.Add(self.btn_eliminar_producto, flag=wx.LEFT, border=10)
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)
        self.Bind(wx.EVT_BUTTON, self.guardar_venta, btn_ok)
        self.btn_eliminar_producto.Bind(wx.EVT_BUTTON, self.eliminar_producto)
        self.btn_agregar_producto.Bind(wx.EVT_BUTTON, self.agregar_producto)

        self.productos_seleccionados = []
        self.productos_dict = self.cargar_productos()
        self.actualizar_lista_productos()
        
        self.lista_clientes.Bind(wx.EVT_LISTBOX_DCLICK, self.seleccionar_cliente)  # Doble clic para seleccionar

        # Total de la venta
        vbox.Add(wx.StaticText(panel, label="Total:"), flag=wx.LEFT | wx.TOP, border=10)
        self.lbl_total = wx.TextCtrl(panel, style=wx.TE_READONLY)
        self.lbl_total.SetValue("$0.00")  # Establecer el valor inicial
        vbox.Add(self.lbl_total, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        self.Layout()  # Layout inicial del diálogo
        self.txt_cliente.SetFocus()  # Establecer el foco en txt_cliente
        
        
        # 🔥 Atajos de teclado
        accel_tbl = wx.AcceleratorTable([
        (wx.ACCEL_CTRL, ord('G'), btn_ok.GetId()),  # Ctrl + G para guardar
        (wx.ACCEL_CTRL, ord('E'), self.btn_eliminar_producto.GetId()),  # Ctrl + E para eliminar producto
        (wx.ACCEL_CTRL, ord('A'), self.btn_agregar_producto.GetId()),  # Ctrl + E para eliminar producto
        (wx.ACCEL_CTRL, ord('B'), self.txt_buscar_producto.GetId()),  # Ctrl + B para buscar producto
    ])
        self.SetAcceleratorTable(accel_tbl)
 

    def ShowModal(self):
        self.productos_dict = self.cargar_productos()  # Recargar productos antes de mostrar
        self.actualizar_lista_productos()
        return super().ShowModal()

    def cargar_clientes(self):
        """Carga los clientes en la lista."""
        self.clientes_dict = gestion_cliente.obtener_todos()
        self.lista_clientes.Clear()
        for id_cliente, datos in self.clientes_dict.items():
            self.lista_clientes.Append(f"{datos['nombre']} ({datos['telefono']})")


    def filtrar_clientes(self, event):
        print("filtro")
        filtro = self.txt_cliente.GetValue()
        self.lista_clientes.Clear()
        clientes_filtrados = gestion_cliente.obtener_clientes_filtrados(filtro)

        for id_cliente, datos in clientes_filtrados.items():
            self.lista_clientes.Append(f"{datos['nombre']} ({datos['telefono']})")

        if self.lista_clientes.GetCount() > 0:
            self.lista_clientes.SetFocus()
            seleccion = self.lista_clientes.GetStringSelection()
            if seleccion:
                wx.CallAfter(self.lista_clientes.SetLabel, seleccion)
    

    
    def seleccionar_cliente(self, event=None):
        """Selecciona el cliente y devuelve el foco al campo de texto."""
        seleccion = self.lista_clientes.GetStringSelection()
        if seleccion:
            self.txt_cliente.SetValue(seleccion.split(' (')[0])  # Guarda solo el nombre
            self.lista_clientes.Hide()  # Oculta la lista después de seleccionar
            self.txt_cliente.SetFocus()  # Devuelve el foco al campo de texto

    def on_key_cliente(self, event):
        """Permite seleccionar el cliente solo con Enter (deshabilita las flechas)."""
        keycode = event.GetKeyCode()

        if keycode == wx.WXK_RETURN:  # Solo se selecciona con Enter
            self.seleccionar_cliente()
        else:
            event.Skip()  # Permite otros eventos del teclado, pero no las flechas
    def anunciar_seleccion(self):
        """Fuerza la lectura de la selección en lectores de pantalla."""
        seleccion = self.lista_clientes.GetStringSelection()
        if seleccion:
            wx.CallAfter(self.lista_clientes.SetLabel, seleccion)

    def cargar_productos(self):
        self.list_productos.Clear()
        productos = gestion_producto.obtener_productos()  
        #print("Tipo de 'productos':", type(productos))  
        #print("Contenido de 'productos':", productos)  # Imprime el contenido completo
        productos_dict = {}  # Se crea un diccionario vacío.
        
        if productos:
            for id_producto, producto in productos.items():  # Iteramos sobre items (clave, valor)
                try:
                    item_text = f"Código: {id_producto} - {producto['nombre']} - Stock: {producto['stock']} - Precio: ${producto['precio']}"
                    self.list_productos.Append(item_text)
                    productos_dict[id_producto] = producto  # Usamos el ID como clave
                except KeyError as e:
                    print(f"Error al procesar producto {id_producto}: {e}")
                    print(f"Datos del producto: {producto}")
                    continue

        return productos_dict
            
    def actualizar_lista_productos(self, event=None):
        self.list_productos.Clear()
        productos = gestion_producto.obtener_productos()

        if not isinstance(productos, dict):
            print("❌ Error: `obtener_productos()` no devolvió un diccionario")
            return

        if productos:
            for id_producto, producto in productos.items():
                try:
                    self.list_productos.Append((
                        str(producto['nombre']),
                        str(id_producto),
                        str(producto['stock']),
                        str(producto['precio'])
                    ))
                except KeyError as e:
                    print(f"Error al procesar producto {id_producto}: {e}")
                    print(f"Datos del producto: {producto}")
                    continue


    def filtrar_productos_noanda(self, event):
        filtro = self.txt_buscar_producto.GetValue()
        self.actualizar_lista_productos(filtro)

    def filtrar_productos(self, event):
        filtro = self.txt_buscar_producto.GetValue()
        self.list_productos.Clear()
        productos_filtrados = gestion_producto.obtener_productos_filtrados(filtro) # Esta función no existe, tendrías que crearla

        if productos_filtrados:
            for id_producto, producto in productos_filtrados.items():
                try:
                    self.list_productos.Append((
                        str(producto['nombre']),
                        str(id_producto),
                        str(producto['stock']),
                        str(producto['precio'])
                    ))
                except KeyError as e:
                    print(f"Error al procesar producto {id_producto}: {e}")
                    print(f"Datos del producto: {producto}")
                    continue
    
    def eliminar_producto(self, event):
        seleccion = self.list_productos_seleccionados.GetSelection()
        if seleccion != wx.NOT_FOUND:
            seleccion_str = self.list_productos_seleccionados.GetString(seleccion)
            self.productos_seleccionados.remove(seleccion_str)
            self.list_productos_seleccionados.Delete(seleccion)
            self.actualizar_total()

    def navegar_productos(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN:
            self.agregar_producto(None)
        elif keycode == wx.WXK_DELETE:
            self.eliminar_producto(None)
        elif keycode == wx.WXK_UP:
            current_selection = self.list_productos.GetSelection()
            if current_selection > 0:
                self.list_productos.SetSelection(current_selection - 1)
        elif keycode == wx.WXK_DOWN:
            current_selection = self.list_productos.GetSelection()
            if current_selection < self.list_productos.GetCount() - 1:
                self.list_productos.SetSelection(current_selection + 1)
        else:
            event.Skip()



#permite agregar varios productos


    def agregar_producto(self, event):
        seleccion = self.list_productos.GetStringSelection()
        print(f"Seleccion: {seleccion}")
        if seleccion:
            producto = gestion_producto.obtener_productos_por_nombre(seleccion)

            if producto:
                producto_id, producto_info = next(iter(producto.items())) # Obtener el primer producto del diccionario.
                if producto_info:
                    if producto_info["stock"] > 0:
                        cantidad_str = wx.GetTextFromUser("Ingrese la cantidad:", "Cantidad", "1")
                        if cantidad_str:
                            if cantidad_str.isdigit():
                                cantidad = int(cantidad_str)
                                if cantidad <= producto_info["stock"]:
                                    producto_seleccionado = {
                                        "id_producto": int(producto_id),
                                        "cantidad": cantidad,
                                        "descripcion": seleccion
                                    }
                                    producto_existente = next((p for p in self.productos_seleccionados if p["id_producto"] == int(producto_id)), None)
                                    if producto_existente:
                                        producto_existente["cantidad"] += cantidad
                                        self.actualizar_lista_seleccionados()
                                    else:
                                        self.productos_seleccionados.append(producto_seleccionado)
                                        self.list_productos_seleccionados.Append(f"{seleccion} - Cantidad: {cantidad}")
                                    self.actualizar_total()
                                else:
                                    wx.MessageBox("La cantidad ingresada es mayor al stock disponible.", "Error", wx.OK | wx.ICON_ERROR)
                            else:
                                wx.MessageBox("Ingrese una cantidad válida.", "Error", wx.OK | wx.ICON_ERROR)
                        else:
                            print("El usuario canceló el ingreso de cantidad")
                    else:
                        wx.MessageBox("No hay stock disponible para este producto.", "Error", wx.OK | wx.ICON_ERROR)
                else:
                    wx.MessageBox("Producto no encontrado.", "Error", wx.OK | wx.ICON_ERROR)
            else:
                wx.MessageBox("No se encontró el producto en la base de datos.", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Seleccione un producto.", "Error", wx.OK | wx.ICON_ERROR)
        def actualizar_lista_seleccionados(self):
            self.list_productos_seleccionados.Clear()
            for producto in self.productos_seleccionados:
                self.list_productos_seleccionados.Append(f"{producto['descripcion']} - Cantidad: {producto['cantidad']}")


    def GetFechaVenta(self):
        """Devuelve la fecha de venta seleccionada como un objeto datetime.date."""
        wx_datetime = self.date_picker_venta.GetValue()  # Obtiene el objeto wx.DateTime
        year = wx_datetime.GetYear()  # Obtiene el año
        month = wx_datetime.GetMonth() + 1  # Los meses en wxPython son 0-based, así que sumamos 1
        day = wx_datetime.GetDay()  # Obtiene el día
        
        # Crea un objeto datetime.date de Python
        return datetime.date(year, month, day)
    def guardar_venta(self, event):
        """
        Guarda la venta en la base de datos.
        """
        # 1. Obtener la fecha 
        fecha_venta_date = self.GetFechaVenta()

        # Formatear la fecha como una cadena (opcional, según cómo quieras guardarla)
        #fecha_venta_formateada = fecha_venta_date.strftime('%Y-%m-%d') # Ejemplo: AAAA-MM-DD
        # Otro formato común:
        fecha_venta_formateada = fecha_venta_date.strftime('%d/%m/%Y') # Ejemplo: DD/MM/AAAA

        print(f"Fecha de venta (date): {fecha_venta_date}")

        # 2. Obtener el ID del cliente (ejemplo: desde un campo de texto).
        cliente_str = self.txt_cliente.GetValue()
        print(cliente_str)
        id_cliente=gestion_cliente.buscar_cliente_nombre(cliente_str)
        #print(f"id del cliente obtenido:{id_cliente}")

        # 3. Obtener el total de la venta (ejemplo: desde la etiqueta lbl_total).
        total_venta_str = self.lbl_total.GetLabel().replace("$", "")
        try:
            total_venta = float(total_venta_str)
        except ValueError:
            wx.MessageBox("Total de venta inválido.", "Error", wx.OK | wx.ICON_ERROR)
            return

        # 4. Obtener los productos vendidos (desde self.productos_seleccionados).
        productos_vendidos = self.productos_seleccionados
        #print(f"{fecha_venta_formateada} { id_cliente}")
        # 5. Llamar al método registrar_venta de GestionVentas.
        if self.gestion_ventas.registrar_venta(fecha_venta_formateada, id_cliente, productos_vendidos, total_venta):
            wx.MessageBox("Venta guardada correctamente.", "Éxito", wx.OK | wx.ICON_INFORMATION)
            # Limpiar la lista de productos seleccionados y actualizar la interfaz.
            self.productos_seleccionados = []
            self.list_productos_seleccionados.Clear()
            self.lbl_total.SetLabel("$0.00")
            self.Layout()
        else:
            wx.MessageBox("Error al guardar la venta.", "Error", wx.OK | wx.ICON_ERROR)

        """
        Actualiza la interfaz de usuario con el total de la venta.
        """

    def actualizar_total(self):
        total_venta = self.gestion_ventas.calcular_total_venta_desde_db(self.productos_seleccionados)

        if total_venta is not None:
            self.lbl_total.SetLabel(f"${total_venta:.2f}")
        else:
            self.lbl_total.SetLabel("$0.00")

        self.Layout()

