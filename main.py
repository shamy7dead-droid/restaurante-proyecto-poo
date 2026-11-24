from modelo.clientes import Cliente
from modelo.productos import Plato, Bebida, Combo
from modelo.pagos import Efectivo, QR, Tarjeta
from modelo.pedidos import Local, Para_llevar, Delivery
from restaurante import Restaurante


def cargar_datos_iniciales(rest):
    silpancho = Plato("Silpancho", 35.0)
    pique = Plato("Pique macho", 55.0)
    chicharron = Plato("Chicharrón", 45.0, ["domingo"])
    sopa = Plato("Sopa de maní", 18.0)

    moco_vaso = Bebida("Mocochinchi (Vaso)", 6.0, "vaso")
    moco_jarra = Bebida("Mocochinchi (Jarra)", 6.0, "jarra")
    gaseosa = Bebida("Gaseosa 2L", 12.0, "vaso")

    combo_valluno = Combo("Combo Valluno")
    combo_valluno.agregar_p(silpancho, 1)
    combo_valluno.agregar_p(moco_vaso, 1)

    for prod in [silpancho, pique, chicharron, sopa, moco_vaso, moco_jarra, gaseosa, combo_valluno]:
        rest.registrar_producto(prod)

    rest.registrar_cliente(Cliente(1, "Juan Pérez", "71234567"))
    rest.registrar_cliente(Cliente(2, "María Rojas", "65432109"))


def seleccionar_cliente(clientes):
    if not clientes:
        print("No hay clientes registrados.")
        return None
    for i, c in enumerate(clientes, start=1):
        print(f"{i}. [{c.id_cliente}] {c.nombre} (Tel: {c.telefono})")
    idx = int(input("Seleccione número de cliente: ")) - 1
    if idx < 0 or idx >= len(clientes):
        raise ValueError("Selección fuera de rango.")
    return clientes[idx]


def seleccionar_pedido(pedidos):
    if not pedidos:
        print("No hay pedidos registrados.")
        return None
    for i, p in enumerate(pedidos, start=1):
        print(f"{i}. {p.tipo_pedido()} - {p.cliente.nombre} [{p.estado}]")
    idx = int(input("Seleccione número de pedido: ")) - 1
    if idx < 0 or idx >= len(pedidos):
        raise ValueError("Selección fuera de rango.")
    return pedidos[idx]


def menu_consola():
    rest = Restaurante()
    cargar_datos_iniciales(rest)

    while True:
        print("\n=== SABOR VALLUNO (VARIANTE A) ===")
        print("1. Registrar producto o armar combo")
        print("2. Listar menú disponible por día")
        print("3. Registrar cliente")
        print("4. Crear pedido y agregar/quitar productos")
        print("5. Ver detalle de pedido")
        print("6. Cambiar estado de pedido")
        print("7. Registrar retraso en delivery (Regla 9)")
        print("8. Cobrar pedido y ver comprobante")
        print("9. Ver reporte de ventas del día")
        print("0. Salir")

        opcion = input("Opción: ").strip()
        try:
            if opcion == "1":
                tipo = input("Tipo (1=Plato, 2=Bebida, 3=Combo): ").strip()
                nombre = input("Nombre: ").strip()
                if tipo == "1":
                    precio = float(input("Precio (Bs): "))
                    dias_txt = input("Días disponibles separados por coma (Enter = todos): ").strip()
                    dias = [d.strip() for d in dias_txt.split(",")] if dias_txt else None
                    rest.registrar_producto(Plato(nombre, precio, dias))
                elif tipo == "2":
                    precio = float(input("Precio por vaso (Bs): "))
                    envase = input("Envase (vaso/jarra): ").strip()
                    rest.registrar_producto(Bebida(nombre, precio, envase))
                elif tipo == "3":
                    combo = Combo(nombre)
                    prods = rest.menu()
                    for i, p in enumerate(prods, start=1):
                        print(f"{i}. {p.nombre} - Bs {p.calc_precio():.2f}")
                    while True:
                        sel = input("Número de producto a agregar (0 para terminar): ").strip()
                        if sel == "0":
                            break
                        idx = int(sel) - 1
                        if idx < 0 or idx >= len(prods):
                            raise ValueError("Producto fuera de rango.")
                        cant = int(input("Cantidad (1-20): "))
                        combo.agregar_p(prods[idx], cant)
                    combo.calc_precio()
                    rest.registrar_producto(combo)
                else:
                    print("Tipo no válido.")
                    continue
                print("Producto registrado correctamente.")

            elif opcion == "2":
                dia = input("Día de la semana (Enter para ver todo): ").strip()
                disponibles = rest.menu(dia if dia else None)
                for p in disponibles:
                    print(f"- {p.nombre} | Precio: Bs {p.calc_precio():.2f} | Platos: {p.contar_platos()}")

            elif opcion == "3":
                cid = len(rest.clientes) + 1
                nombre = input("Nombre del cliente: ").strip()
                tel = input("Teléfono (8 dígitos, empieza en 6 o 7): ").strip()
                rest.registrar_cliente(Cliente(cid, nombre, tel))
                print("Cliente registrado correctamente.")

            elif opcion == "4":
                sub = input("1=Nuevo pedido, 2=Modificar pedido existente: ").strip()
                if sub == "1":
                    cli = seleccionar_cliente(rest.clientes)
                    if not cli:
                        continue
                    t_ped = input("Tipo (1=Local, 2=Para llevar, 3=Delivery): ").strip()
                    if t_ped == "1":
                        mesa = int(input("Número de mesa (1-15): "))
                        ped = Local(cli, mesa)
                    elif t_ped == "2":
                        ped = Para_llevar(cli)
                    elif t_ped == "3":
                        zona = input("Zona (Cercado/Quillacollo/Sacaba/Vinto): ").strip()
                        ped = Delivery(cli, zona)
                    else:
                        print("Tipo inválido.")
                        continue
                    rest.nuevo_pedido(ped)
                elif sub == "2":
                    ped = seleccionar_pedido(rest.pedidos)
                    if not ped:
                        continue
                else:
                    print("Opción inválida.")
                    continue

                prods = rest.menu()
                for i, p in enumerate(prods, start=1):
                    print(f"{i}. {p.nombre} - Bs {p.calc_precio():.2f}")
                accion = input("1=Agregar producto, 2=Quitar producto: ").strip()
                idx = int(input("Número de producto: ")) - 1
                if idx < 0 or idx >= len(prods):
                    raise ValueError("Producto fuera de rango.")
                if accion == "1":
                    cant = int(input("Cantidad (1-20): "))
                    ped.agregar(prods[idx], cant)
                elif accion == "2":
                    ped.quitar(prods[idx])
                else:
                    print("Acción inválida.")
                    continue
                print("Pedido actualizado.")

            elif opcion == "5":
                ped = seleccionar_pedido(rest.pedidos)
                if ped:
                    print("\n" + ped.mostrar_detalle())

            elif opcion == "6":
                ped = seleccionar_pedido(rest.pedidos)
                if ped:
                    nuevo = input("Nuevo estado (EN_PREPARACION/LISTO/ENTREGADO/CANCELADO): ").strip()
                    ped.cambiar_est(nuevo)
                    print(f"Estado cambiado a {ped.estado}.")

            elif opcion == "7":
                ped = seleccionar_pedido(rest.pedidos)
                if not ped:
                    continue
                if not hasattr(ped, "retraso"):
                    print("Esta opción solo aplica a pedidos de tipo Delivery.")
                    continue
                mins = int(input("Minutos transcurridos de entrega: "))
                devuelto = ped.retraso(mins)
                if devuelto > 0:
                    print(f"Retraso registrado (>60 min). Devolución de envío: Bs {devuelto:.2f}")
                else:
                    print("El pedido no superó los 60 minutos; no aplica devolución.")

            elif opcion == "8":
                ped = seleccionar_pedido(rest.pedidos)
                if not ped:
                    continue
                print(f"Total a pagar: Bs {ped.calc_total():.2f}")
                mp = input("Método (1=Efectivo, 2=QR, 3=Tarjeta): ").strip()
                if mp == "1":
                    recibido = float(input("Monto recibido (Bs): "))
                    metodo = Efectivo(recibido)
                elif mp == "2":
                    cod = input("Código de transacción (10 dígitos): ").strip()
                    metodo = QR(cod)
                elif mp == "3":
                    metodo = Tarjeta()
                else:
                    print("Método inválido.")
                    continue
                print(ped.registrar_pago(metodo))

            elif opcion == "9":
                rep = rest.reporte()
                print("\n--- REPORTE DE VENTAS DEL DÍA ---")
                for tipo, monto in rep["ventas_por_tipo"].items():
                    print(f"  {tipo}: Bs {monto:.2f}")
                print("Top 3 productos más vendidos:")
                for nombre, cant in rep["top_3_productos"]:
                    print(f"  - {nombre}: {cant} unidades")

            elif opcion == "0":
                break
            else:
                print("Opción no válida.")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu_consola()