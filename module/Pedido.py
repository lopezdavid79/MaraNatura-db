class Pedido:
    def __init__(self, id, fecha, cliente, detalle, estado):
        self.id = id
        self.fecha = fecha
        self.cliente = cliente
        self.detalle = detalle
        self.estado = estado

    def __str__(self):
        return f"ID: {self.id}, Fecha: {self.fecha}, Cliente: {self.cliente}, Detalle: {self.detalle}, Estado: {self.estado}"

    def a_diccionario(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "cliente": self.cliente,
            "detalle": self.detalle,
            "estado": self.estado
        }