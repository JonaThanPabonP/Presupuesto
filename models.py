
class Movimiento:
    def __init__(self, fecha, tipo, categoria, detalle, monto):
        self.fecha = fecha
        self.tipo = tipo
        self.categoria = categoria
        self.detalle = detalle
        self.monto = monto

    def nuevo(self):
        return {
            'fecha': self.fecha,
            'tipo': self.tipo,
            'categoria': self.categoria,
            'detalle': self.detalle,
            'monto': int(self.monto),
        }
    
    def editar(self):
        return {
            'fecha': self.fecha,
            'tipo': self.tipo,
            'categoria': self.categoria,
            'detalle': self.detalle,
            'monto': int(self.monto),
        }