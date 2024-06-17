import json
import os


valor_asiento_normal = 78900
valor_asiento_vip = 240000

def menu():
    os.system("CLS")
    print("""
          +--------------------------+
                Menu Vuelos Duoc
          +--------------------------+
            1. Ver asientos disponibles
            2. Comprar asiento
            3. Anular vuelo
            4. Modificar datos de pasajero
            5. Salir
        """)

def elejir_opcion_menu_principal():
    print("Bienvenidos a vuelos duoc!")
    while True:
        try:
            menu()
            op = int(input("-> "))
            if type(op) != int:
                raise ValueError
            if op == 1:
                ver_asientos_disponibles()
                input("[ENTER] para continuar...")
            elif op == 2:
                comprar_asiento()
                input("[ENTER] para continuar...")
            elif op == 3:
                anular_vuelo()
                input("[ENTER] para continuar...")
            elif op == 4:
                print("Cual asiento del pasajero que desea modificar? ")
                asiento = int(input("-> "))
                if type(asiento) != int:
                    raise ValueError
                modificar_datos_del_pasajero(asiento)
            elif op == 5:
                print("[ENTER] para salir.")
                print("Bye!")
                break
            else:
                print("Opcion no es valida, por favor intente denuevo!")
                input("[ENTER] para continuar...")
        except ValueError:
            print("Ingrese una opcion valida")
    
def ver_asientos_disponibles():
    print("Los asientos disponibles son:")
    fila = 1
    columna = 0
    asientos = ""

    with open('lista_asientos.json', 'r') as asientos:
        lista_de_asientos = json.load(asientos)

    print("|", end=" ")
    columna = 0
    index = 0
    for asiento in lista_de_asientos:
            if columna <= 3:
                if asiento == "X":
                    print(f"[{asiento} ] ", end=" ")
                else:
                    print(f"[{asiento}] ", end=" ")
                columna += 1
                if columna == 3 and fila == 1:
                    print("\t", end=" ")
                    columna = 0
                    fila += 1
                elif columna == 3 and fila == 2:
                    print("|")
                        
                    if index != 41:
                        if index == 29:
                            print("============================================")
                        print("|", end=" ")
                    

                    columna = 0
                    fila -= 1
           
            index += 1

def ingresar_nombre_del_pasajero():
    nombre = input("Ingrese nombre > ")
    return nombre

def ingresar_rut_del_pasajero():
    rut = input("Ingrese rut > ")
    return rut

def ingresar_telefono_del_pasajero():
    telefono = input("Ingrese numero de telefono > ")
    return telefono

def ingresar_banco_del_pasajero():
    banco = input("Ingresa banco >")
    return banco.lower()
            
            
def comprar_asiento():
    while True:
        asiento_seleccionado = seleccion_de_asientos()
    
        if asiento_seleccionado != 0:
            registrar_datos_pasajeros(asiento_seleccionado)
            reservar_asiento(asiento_seleccionado)
            banco_pasajero = banco_del_pasajero(asiento_seleccionado)
            descuento(banco_pasajero)
            break
            

def seleccion_de_asientos():
    asiento_seleccionado = 0
    while True:
        try:
            asiento_seleccionado = int(input("Selecciona un asiento entre el 1 al 42: "))
            if type(asiento_seleccionado) is not int:
                raise ValueError
            break
        except ValueError:
            print("Dato incorrecto, debe ser numerico. Porfavor intente denuevo!")
            input("[Enter] para continuar...")
        
        
    
    with open('lista_asientos.json', 'r') as asientos:
        asientos = json.load(asientos)
        
    if asientos[asiento_seleccionado - 1] != "X":
        print(f"El asiento {asiento_seleccionado} esta disponible")
        while True:
            respuesta = input("¿aceptas el asiento si/no?").lower()
            if respuesta == "si" or respuesta == "no":
                break
            else:
                print("Respuesta debe ser [Si/No]")

        if respuesta == "si":
            valor_de_asiento(asiento_seleccionado)
            return asiento_seleccionado
    else:
        print("Asiento no disponible, porfavor elejir otro")
        ver_asientos_disponibles()
        input("[ENTER] para continuar...")
        return 0
    
        
def valor_de_asiento(asiento):
    if int(asiento) >= 31 and int(asiento) <= 42:
        print(f"El siento {asiento} es asiento-vip y su valor es de {valor_asiento_vip} pesos.")
    else:
        print(f"El siento {asiento} es asiento-normal y su valor es de {valor_asiento_normal} pesos.")

def descuento(banco):
    if banco == "banco duoc":
        descuento = valor_asiento_normal * 0.85
        print(f"Usted por ser cliente Banco Duoc, tiene un descuento del 15%. El total es {descuento}")

def banco_del_pasajero(asiento):
    with open('datos_pasajeros.json', 'r') as datos_pasajeros:
        lista_de_pasajeros = json.load(datos_pasajeros)

    for pasajero in lista_de_pasajeros:
        if pasajero["asiento"] == asiento:
            return pasajero['banco']
        
    
def registrar_datos_pasajeros(seleccion_asiento):
    nombre = ingresar_nombre_del_pasajero()
    rut = ingresar_rut_del_pasajero()
    telefono = ingresar_telefono_del_pasajero()
    banco = ingresar_banco_del_pasajero()

    datos_pasajero = { 
            "nombre": nombre,
            "rut": rut,
            "telefono": telefono,
            "banco": banco,
            "asiento": seleccion_asiento}
    
    if os.stat('datos_pasajeros.json').st_size == 0:
        with open('datos_pasajeros.json', 'w') as datos_pasajeros:
            datos_pasajeros.write('[]')

    with open("datos_pasajeros.json", "r") as datos_pasajeros:
        datos_pasajeros = json.load(datos_pasajeros)
        index = 0
        for pasajero in datos_pasajeros:
            if pasajero["asiento"] == seleccion_asiento:
                datos_pasajeros[index].update(datos_pasajero)
                break
            index += 1
        else:
            datos_pasajeros.append(datos_pasajero)
        
        with open('datos_pasajeros.json', 'w') as asientos:
            json.dump(datos_pasajeros, asientos)


def reservar_asiento(seleccion_asiento):
    with open('lista_asientos.json', 'r') as asientos:
        asientos_lista = json.load(asientos)
    
    if asientos_lista[seleccion_asiento - 1] != "X":
        asientos_lista[seleccion_asiento - 1] = "X"

    with open("lista_asientos.json", 'w', encoding='utf-8') as asientos:
        asientos.write(json.dumps(asientos_lista, indent=2))

def anular_asiento(numero_de_asiento):
    with open('lista_asientos.json', 'r') as asientos:
        lista_de_asientos = json.load(asientos)
    
    lista_de_asientos[numero_de_asiento - 1] = numero_de_asiento

    
    with open("lista_asientos.json", 'w', encoding='utf-8') as asientos:
        asientos.write(json.dumps(lista_de_asientos))
    print("Asiento anulado: OK")

def remover_datos_pasajero(numero_de_asiento):
    with open('datos_pasajeros.json', 'r') as datos:
        lista_de_datos = json.load(datos)

    index = 0
    for pasajero in lista_de_datos:
        if pasajero["asiento"] == numero_de_asiento:
            del lista_de_datos[index]
        index += 1

    with open("datos_pasajeros.json", 'w', encoding='utf-8') as lista_asientos:
        lista_asientos.write(json.dumps(lista_de_datos, indent=2))
    print("Datos del pasajero removido: OK")

def anular_vuelo():
    numero_de_asiento = int(input("Ingrese numero de pasaje a anular > "))
    anular_asiento(numero_de_asiento)
    remover_datos_pasajero(numero_de_asiento)

def menu_modificar_datos_pasajero():
    print("""
            Si desea cambiar uno de los datos del pasajero,
            Porfavor seleccione una opcion
            1) Nombre
            2) Rut
            3) Telefono
            4) Banco
            0) Salir
          """)

def seleccionar_datos_a_cambiar():
    datos_ingresados = ""
    datos = {"nombre": "",
             "rut": "",
             "telefono": "",
             "banco": ""}
    opcion = -1
    while True:
        try:
            opcion = int(input("Ingrese opcion > "))
        except ValueError:
            print("Ingrese una opcion valida")
            menu_modificar_datos_pasajero()
        if opcion == 1:
            nombre = ingresar_nombre_del_pasajero()
            datos["nombre"] = nombre
            datos_ingresados += "Nombre: Ok\n"
        elif opcion == 2:
            rut = ingresar_rut_del_pasajero()
            datos["rut"] = rut
            datos_ingresados += "Rut: Ok\n"
        elif opcion == 3:
            telefono = ingresar_telefono_del_pasajero()
            datos["telefono"] = telefono
            datos_ingresados += "Telefono: Ok\n"
        elif opcion == 4:
            banco = ingresar_banco_del_pasajero()
            datos["banco"] = banco
            datos_ingresados += "Banco: Ok\n"
        elif opcion == 0:
            if datos_ingresados == "":
                print("Cero datos ingresados.")
                print("Hasta pronto!")
            else:
                print(datos_ingresados)
                print("Hasta pronto!")
            break
    return datos

def modificar_datos_del_pasajero(asiento):
    with open('datos_pasajeros.json', 'r') as datos_pasajeros:
        if os.stat('datos_pasajeros.json').st_size == 0:
            with open('datos_pasajeros.json', 'w') as datos_pasajeros:
                datos_pasajeros.write('[]')
                with open('datos_pasajeros.json', 'r') as archivo:
                    lista_datos = json.load(archivo)
                    print()
                    if not lista_datos:
                        print('No datos en la base de datos...')
                        input("[ENTER] para continuar...")
        else:
            with open('datos_pasajeros.json', 'r') as archivo:
                    lista_datos = json.load(archivo)

    datos_pasajero = {}
    menu_modificar_datos_pasajero()
    datos_cambiados = seleccionar_datos_a_cambiar()
    index = 0

    for pasajero in lista_datos:
        if pasajero["asiento"] == asiento:
            datos_pasajero.update(pasajero)
            datos_pasajero.update(datos_cambiados)
            lista_datos[index].update(datos_pasajero)
        index += 1
    
    with open('datos_pasajeros.json', 'w') as archivo:
        json.dump(lista_datos, archivo)
    input('[ENTER] para continuar...')