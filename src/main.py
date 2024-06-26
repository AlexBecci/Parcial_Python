import sys
from datetime import datetime
from hotel import Hotel

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
