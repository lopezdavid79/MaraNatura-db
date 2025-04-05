import wx
from backapp import BackupFrame
from reports.rp_ventas import  ReporteVentasFrame
from Views.fr_listProduct import ListProducto
from Views.fr_listPedido import ListPedido
from Views.fr_producto import VentanaProducto
from Views.fr_listSale import ListSale
from Views.fr_cliente import VentanaCliente  # Importamos la ventana de clientes
from Views.fr_listClient  import ListaClientes  # Importamos la gestión de clientes
from module.ReproductorSonido  import ReproductorSonido 


class Principal(wx.Frame):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.report_frame = None
        # Crear la barra de menú
        menubar = wx.MenuBar()

        # Crear el menú "Archivo"
        file_menu = wx.Menu()
        new_product_item = wx.MenuItem(file_menu, wx.ID_ANY, "Nuevo producto")
        file_menu.Append(new_product_item)
        file_menu.AppendSeparator()
        list_product_item = wx.MenuItem(file_menu, wx.ID_ANY, "Lista de Productos")
        file_menu.Append(list_product_item)
        file_menu.AppendSeparator()
        list_pedido_item = wx.MenuItem(file_menu, wx.ID_ANY, "Lista de Pedidos")
        file_menu.Append(list_pedido_item)
        
        # Crear el menú "Clientes"
        client_menu = wx.Menu()
        new_client_item = wx.MenuItem(client_menu, wx.ID_ANY, "Nuevo Cliente")
        client_menu.Append(new_client_item)
        client_menu.AppendSeparator()
        list_client_item = wx.MenuItem(client_menu, wx.ID_ANY, "Lista de Clientes")
        client_menu.Append(list_client_item)

        # Crear el menú "Ventas"
        sales_menu = wx.Menu()
        new_sale_item = wx.MenuItem(sales_menu, wx.ID_ANY, "Lista de Ventas")
        report_sale_item = wx.MenuItem(sales_menu, wx.ID_ANY, "Reporte de Ventas")
        sales_menu.Append(new_sale_item)
        sales_menu.Append(report_sale_item)
# Crear el menú "Opciones"
        mas_menu = wx.Menu()
        backapp_item = wx.MenuItem(mas_menu, wx.ID_ANY, "BackApps BD")
        mas_menu.Append(backapp_item)
        mas_menu.AppendSeparator()
        exit_item = wx.MenuItem(mas_menu, wx.ID_ANY, "Salir")
        mas_menu.Append(exit_item)

        
        # Añadir los menús a la barra de menú
        menubar.Append(file_menu, "Productos")
        menubar.Append(client_menu, "Clientes")  # Agregamos la sección de clientes
        menubar.Append(sales_menu, "Ventas")
        menubar.Append(mas_menu, "Opciones")
        self.SetMenuBar(menubar)

        # Enlazar los eventos de los menús
        self.Bind(wx.EVT_MENU, self.on_new_product, new_product_item)
        self.Bind(wx.EVT_MENU, self.on_list_product, list_product_item)
        self.Bind(wx.EVT_MENU, self.on_list_pedido, list_pedido_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_new_client, new_client_item)  # Nuevo Cliente
        self.Bind(wx.EVT_MENU, self.on_list_client, list_client_item)  # Lista de Clientes
        self.Bind(wx.EVT_MENU, self.on_list_sale, new_sale_item)
        self.Bind(wx.EVT_MENU, self.on_report_sale, report_sale_item)
        self.Bind(wx.EVT_MENU, self.on_backapps, backapp_item)
        # Reproducir sonido de inicio
        ReproductorSonido.reproducir("Inicio.wav")
        self.SetTitle("Gestión Ventas de Mara Natura")
        self.SetSize((600, 400))
        self.Centre()

    def on_new_product(self, event):
        """Abre el formulario para agregar un nuevo producto."""
        producto_form = VentanaProducto(self, id=None, title="Nuevo Producto")
        producto_form.Show()

    def on_list_product(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        """Abre el formulario de lista de productos."""
        list_producto_form = ListProducto(self, id=None, title="Lista de Productos")
        list_producto_form.Show()


    def on_list_pedido(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        """Abre el formulario de lista de productos."""
        list_pedido_form = ListPedido(self, id=None, title="Lista de Pedidos")
        list_pedido_form.Show()

    

    def on_new_client(self, event):
        """Abre el formulario para agregar un nuevo cliente."""
        cliente_form = VentanaCliente(self, id=None, title="Nuevo Cliente")
        cliente_form.Show()

    def on_list_client(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        list_client_form = ListaClientes(self, id=None, title="Lista de Clientes")
        list_client_form.Show()



    
    def on_list_sale(self, event):
        """Abre el formulario de lista de ventas."""
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        list_sale_form = ListSale(self, id=None, title="Lista de Ventas")
        list_sale_form.Show()



    def on_report_sale(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        frame = ReporteVentasFrame(None, "Reporte de Ventas")
        frame.Show()

    def on_exit(self, event):
        """Cierra la aplicación."""
        ReproductorSonido.reproducir("Salir.wav")
        wx.CallLater(1000, self.Close)  # Espera 1 segundo antes de cerrar
        #self.Close()
        wx.Exit()
        


    def on_backapps(self, event):
        """Abre el formulario de lista de ventas."""
        ReproductorSonido.reproducir("screenCurtainOn.wav")

        backapps_form = BackupFrame(self, title="BackApps Bs")
        backapps_form.Show()
