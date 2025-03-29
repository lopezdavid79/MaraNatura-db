class Producto:
    def __init__(self, id, nombre, detalle, stock, precio):
        self.id = id
        self.nombre = nombre
        self.detalle = detalle
        self.stock = stock
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id}, Producto: {self.nombre}, Detalle: {self.detalle}, Stock: {self.stock}, Precio: {self.precio}"