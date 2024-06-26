class Reserva:
    def __init__(self,cliente,fecha_inicio,fecha_fin,costo_total):
        self.cliente= cliente
        self.fecha_inicio= fecha_inicio
        self.fecha_fin= fecha_fin
        self.costo_total= costo_total
    
    def __str__(self):
        return f'Reserva de {self.cliente} desde {self.fecha_inicio} hasta {self.fecha_fin}. Costo total: {self.costo_total}'

        