import csv
from datetime import datetime
from cliente import Cliente
from habitacion import Habitacion
from reserva import Reserva

class Hotel:
    def __init__(self, nombre):
        self.nombre = nombre
        self.habitaciones = []
        self.clientes = []

    def registrar_cliente(self, nombre, apellido, dni):
        cliente = Cliente(nombre, apellido, dni)
        self.clientes.append(cliente)
        self.guardar_clientes_csv('..\\data\\clientes.csv')

    def realizar_reserva(self, cliente_dni, numero_habitacion, fecha_inicio, fecha_fin):
        cliente = self.buscar_cliente(cliente_dni)
        if cliente:
            habitacion = self.buscar_habitacion(numero_habitacion)
            if habitacion and habitacion.esta_disponible(fecha_inicio, fecha_fin):
                costo_total = (fecha_fin - fecha_inicio).days * habitacion.valor_por_noche
                reserva = Reserva(cliente, fecha_inicio, fecha_fin, costo_total)
                habitacion.reservas.append(reserva)
                habitacion.cambiar_estado('ocupada')
                self.guardar_reservas_csv('..\\data\\reservas.csv')
                return True
        return False

    def buscar_cliente(self, dni):
        for cliente in self.clientes:
            if cliente.dni == dni:
                return cliente
        return None

    def buscar_habitacion(self, numero):
        for habitacion in self.habitaciones:
            if habitacion.numero == numero:
                return habitacion
        return None

    def listar_habitaciones_disponibles(self, fecha_inicio, fecha_fin):
        disponibles = []
        for habitacion in self.habitaciones:
            if habitacion.estado == 'disponible' and habitacion.esta_disponible(fecha_inicio, fecha_fin):
                disponibles.append(habitacion)
        return disponibles

    def reporte_habitaciones_libres(self, fecha_inicio, fecha_fin):
        disponibles = self.listar_habitaciones_disponibles(fecha_inicio, fecha_fin)
        for habitacion in disponibles:
            print(habitacion)

    def reporte_ganancias(self, fecha_inicio, fecha_fin):
        total_ganancias = 0
        for habitacion in self.habitaciones:
            for reserva in habitacion.reservas:
                if fecha_inicio <= reserva.fecha_fin and fecha_fin >= reserva.fecha_inicio:
                    total_ganancias += reserva.costo_total
        return total_ganancias

    def cargar_habitaciones_desde_csv(self, archivo_csv):
        with open(archivo_csv, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir el encabezado
            for row in reader:
                numero, capacidad, valor_por_noche, estado = int(row[0]), int(row[1]), int(row[2]), row[3]
                habitacion = Habitacion(numero, capacidad, valor_por_noche, estado)
                self.habitaciones.append(habitacion)

    def cargar_clientes_desde_csv(self, archivo_csv):
        with open(archivo_csv, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir el encabezado
            for row in reader:
                nombre, apellido, dni = row[0], row[1], row[2]
                cliente = Cliente(nombre, apellido, dni)
                self.clientes.append(cliente)

    def cargar_reservas_desde_csv(self, archivo_csv):
        with open(archivo_csv, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Omitir el encabezado
            for row in reader:
                cliente_dni, fecha_inicio, fecha_fin, costo_total, numero_habitacion = row[0], row[1], row[2], float(row[3]), int(row[4])
                cliente = self.buscar_cliente(cliente_dni)
                if cliente:
                    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
                    habitacion = self.buscar_habitacion(numero_habitacion)
                    if habitacion:
                        reserva = Reserva(cliente, fecha_inicio, fecha_fin, costo_total)
                        habitacion.reservas.append(reserva)

    def guardar_clientes_csv(self, archivo_csv):
        with open(archivo_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['nombre', 'apellido', 'dni'])
            for cliente in self.clientes:
                writer.writerow([cliente.nombre, cliente.apellido, cliente.dni])

    def guardar_reservas_csv(self, archivo_csv):
        with open(archivo_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['cliente_dni', 'fecha_inicio', 'fecha_fin', 'costo_total', 'numero_habitacion'])
            for habitacion in self.habitaciones:
                for reserva in habitacion.reservas:
                    writer.writerow([reserva.cliente.dni, reserva.fecha_inicio.strftime('%Y-%m-%d'), reserva.fecha_fin.strftime('%Y-%m-%d'), reserva.costo_total, habitacion.numero])
