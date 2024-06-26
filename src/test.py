import csv
import sys
from datetime import datetime

class Cliente:
    def __init__(self, nombre, apellido, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}, DNI: {self.dni}'


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


class Reserva:
    def __init__(self, cliente, fecha_inicio, fecha_fin, costo_total):
        self.cliente = cliente
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.costo_total = costo_total
    
    def __str__(self):
        return f'Reserva de {self.cliente} desde {self.fecha_inicio} hasta {self.fecha_fin}. Costo total: {self.costo_total}'


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
                habitacion.actualizar_estado()
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
            if habitacion.esta_disponible(fecha_inicio, fecha_fin):
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
                        habitacion.actualizar_estado()  # Actualizar el estado de la habitación

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


def mostrar_menu():
    print("\n--- Sistema de Gestión de Reservas en un Hotel ---")
    print("1. Registrar cliente")
    print("2. Realizar reserva")
    print("3. Consultar habitaciones disponibles")
    print("4. Generar reporte de habitaciones libres")
    print("5. Generar reporte de ganancias")
    print("6. Salir")

def main():
    hotel = Hotel('Hotel Ejemplo')
    hotel.cargar_habitaciones_desde_csv('..\\data\\habitaciones.csv')
    hotel.cargar_clientes_desde_csv('..\\data\\clientes.csv')
    hotel.cargar_reservas_desde_csv('..\\data\\reservas.csv')
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre = input("Nombre: ")
            apellido = input("Apellido: ")
            dni = input("DNI: ")
            hotel.registrar_cliente(nombre, apellido, dni)
            print("Cliente registrado exitosamente.")

        elif opcion == '2':
            dni = input("DNI del cliente: ")
            numero_habitacion = int(input("Número de habitación: "))
            fecha_inicio = datetime.strptime(input("Fecha de inicio (YYYY-MM-DD): "), '%Y-%m-%d')
            fecha_fin = datetime.strptime(input("Fecha de fin (YYYY-MM-DD): "), '%Y-%m-%d')
            if hotel.realizar_reserva(dni, numero_habitacion, fecha_inicio, fecha_fin):
                print("Reserva realizada exitosamente.")
            else:
                print("No se pudo realizar la reserva. Verifique la disponibilidad de la habitación y los datos ingresados.")

        elif opcion == '3':
            fecha_inicio = datetime.strptime(input("Fecha de inicio (YYYY-MM-DD): "), '%Y-%m-%d')
            fecha_fin = datetime.strptime(input("Fecha de fin (YYYY-MM-DD): "), '%Y-%m-%d')
            disponibles = hotel.listar_habitaciones_disponibles(fecha_inicio, fecha_fin)
            if disponibles:
                print("Habitaciones disponibles:")
                for habitacion in disponibles:
                    print(habitacion)
            else:
                print("No hay habitaciones disponibles en el rango de fechas especificado.")

        elif opcion == '4':
            fecha_inicio = datetime.strptime(input("Fecha de inicio (YYYY-MM-DD): "), '%Y-%m-%d')
            fecha_fin = datetime.strptime(input("Fecha de fin (YYYY-MM-DD): "), '%Y-%m-%d')
            print("Reporte de habitaciones libres:")
            hotel.reporte_habitaciones_libres(fecha_inicio, fecha_fin)

        elif opcion == '5':
            fecha_inicio = datetime.strptime(input("Fecha de inicio (YYYY-MM-DD): "), '%Y-%m-%d')
            fecha_fin = datetime.strptime(input("Fecha de fin (YYYY-MM-DD): "), '%Y-%m-%d')
            ganancias = hotel.reporte_ganancias(fecha_inicio, fecha_fin)
            print(f"Ganancias totales desde {fecha_inicio.date()} hasta {fecha_fin.date()}: {ganancias}")

        elif opcion == '6':
            print("Saliendo del sistema. ¡Hasta luego!")
            sys.exit()
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()
