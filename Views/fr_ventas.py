import wx

class Principal(wx.Frame):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        # Crear la barra de menú
        menubar = wx.MenuBar()

        # Crear el menú "Archivo"
        file_menu = wx.Menu()
        new_product_item = wx.MenuItem(file_menu, wx.ID_ANY, "Nuevo producto")
        file_menu.Append(new_product_item)
        file_menu.AppendSeparator()  # Separador
        exit_item = wx.MenuItem(file_menu, wx.ID_ANY, "Salir")
        file_menu.Append(exit_item)

        # Crear el menú "Ventas"
        sales_menu = wx.Menu()
        new_sale_item = wx.MenuItem(sales_menu, wx.ID_ANY, "Nueva venta")
        sales_menu.Append(new_sale_item)

        # Añadir los menús a la barra de menú
        menubar.Append(file_menu, "Archivo")
        menubar.Append(sales_menu, "Ventas")
        self.SetMenuBar(menubar)

        # Enlazar los eventos de los menús
        self.Bind(wx.EVT_MENU, self.on_new_product, new_product_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        self.Bind(wx.EVT_MENU, self.on_new_sale, new_sale_item)

        self.SetTitle("Gestión de Productos y Ventas")
        self.SetSize((600, 400))
        self.Centre()

    def on_new_product(self, event):
        # Aquí se abriría el formulario para agregar un nuevo producto
        print("Agregar nuevo producto")

    def on_exit(self, event):
        self.Close()

    def on_new_sale(self, event):
        # Aquí se abriría el formulario para registrar una nueva venta
        print("Nueva venta")

if __name__ == "__main__":
    app = wx.App()
    frame = Principal(None)
    frame.Show()
    app.MainLoop()