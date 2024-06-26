from datetime import datetime

class Habitacion:
    def __init__(self, numero, capacidad, valor_por_noche, estado='disponible'):
        self.numero = numero
        self.capacidad = capacidad
        self.valor_por_noche = valor_por_noche
        self.estado = estado
        self.reservas = []

    def __str__(self):
        return f'Habitacion {self.numero}, Capacidad: {self.capacidad}, Valor por noche: {self.valor_por_noche}'

    def esta_disponible(self, fecha_inicio, fecha_fin):
        for reserva in self.reservas:
            if fecha_inicio <= reserva.fecha_fin and fecha_fin >= reserva.fecha_inicio:
                return False
        return True

    def actualizar_estado(self):
        hoy = datetime.today().date()
        for reserva in self.reservas:
            if reserva.fecha_inicio.date() <= hoy <= reserva.fecha_fin.date():
                self.estado = 'ocupada'
                return
        self.estado = 'disponible'
