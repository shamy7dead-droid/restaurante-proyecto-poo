from modelo.clientes import Cliente
from modelo.productos import Plato, Bebida, Combo
from modelo.pagos import Efectivo, QR, Tarjeta
from modelo.pedidos import Local, Para_llevar, Delivery
from restaurante import Restaurante


def ejecutar_pruebas():
    # 1. Caso de referencia Variante A: Combo (Silpancho Bs 35 + Mocochinchi Bs 6) = Bs 36.90
    # y 2 combos por delivery a Quillacollo = Bs 88.80
    silpancho = Plato("Silpancho", 35.0)
    mocochinchi_vaso = Bebida("Mocochinchi", 6.0, "vaso")
    combo_base = Combo("Combo Valluno")
    combo_base.agregar_p(silpancho, 1)
    combo_base.agregar_p(mocochinchi_vaso, 1)
    assert combo_base.calc_precio() == 36.90

    cli1 = Cliente(1, "Carlos Mamani", "71234567")
    ped_ref = Delivery(cli1, "Quillacollo")
    ped_ref.agregar(combo_base, 2)
    assert ped_ref.calc_total() == 88.80

    # 2. Combo que contiene otro combo (recursividad de precio y conteo de platos)
    sopa_mani = Plato("Sopa de maní", 18.0)
    combo_familiar = Combo("Combo Familiar")
    combo_familiar.agregar_p(combo_base, 1)
    combo_familiar.agregar_p(sopa_mani, 1)
    assert combo_familiar.calc_precio() == 49.41
    assert combo_familiar.contar_platos() == 2

    # 3. Un combo no puede contenerse a sí mismo
    try:
        combo_familiar.agregar_p(combo_familiar, 1)
        assert False, "Debió fallar al agregarse a sí mismo"
    except ValueError:
        pass

    # 4. Variante A: Chicharrón solo los domingos y disponibilidad heredada en Combo
    chicharron = Plato("Chicharrón", 45.0, ["domingo"])
    assert chicharron.disponible("domingo") is True
    assert chicharron.disponible("martes") is False
    combo_domingo = Combo("Combo Dominical")
    combo_domingo.agregar_p(chicharron, 1)
    combo_domingo.agregar_p(mocochinchi_vaso, 1)
    assert combo_domingo.disponible("domingo") is True
    assert combo_domingo.disponible("viernes") is False

    # 5. Bebida jarra cuesta 3 veces el vaso y no suma envase de plato
    mocochinchi_jarra = Bebida("Mocochinchi", 6.0, "jarra")
    assert mocochinchi_jarra.calc_precio() == 18.00
    assert mocochinchi_jarra.contar_platos() == 0

    # 6. Variante A Para llevar: Bs 2 por envase por cada plato (incluidos dentro de combos)
    ped_llevar = Para_llevar(cli1)
    ped_llevar.agregar(combo_familiar, 1)
    ped_llevar.agregar(mocochinchi_jarra, 1)
    assert ped_llevar.calc_cargos() == 4.00
    assert ped_llevar.calc_total() == round(49.41 + 18.00 + 4.00, 2)

    # 7. Variante A Delivery: envío gratis desde Bs 150 solo en Cercado; mínimo Bs 40
    ped_cercado_gratis = Delivery(cli1, "Cercado")
    ped_cercado_gratis.agregar(silpancho, 5)
    assert ped_cercado_gratis.calc_cargos() == 0.00

    ped_quillacollo_caro = Delivery(cli1, "Quillacollo")
    ped_quillacollo_caro.agregar(silpancho, 5)
    assert ped_quillacollo_caro.calc_cargos() == 15.00

    ped_minimo = Delivery(cli1, "Cercado")
    ped_minimo.agregar(silpancho, 1)
    try:
        ped_minimo.calc_total()
        assert False, "Debió fallar por pedido mínimo < Bs 40"
    except ValueError:
        pass

    # 8. Local: mesa 1 a 15, sin dos pedidos abiertos en la misma mesa y reporte
    rest = Restaurante()
    p_local1 = Local(cli1, 5)
    p_local1.agregar(silpancho, 1)
    rest.nuevo_pedido(p_local1)
    p_local2 = Local(cli1, 5)
    p_local2.agregar(sopa_mani, 1)
    try:
        rest.nuevo_pedido(p_local2)
        assert False, "Debió bloquear segundo pedido abierto en mesa 5"
    except ValueError:
        pass

    rep = rest.reporte()
    assert rep["ventas_por_tipo"]["Local"] == 35.00
    assert rep["top_3_productos"][0] == ("Silpancho", 1)

    # 9. Transiciones de estado y bloqueo de edición fuera de REGISTRADO
    p_local1.cambiar_est("EN_PREPARACION")
    try:
        p_local1.agregar(sopa_mani, 1)
        assert False, "No debe permitir agregar fuera de REGISTRADO"
    except ValueError:
        pass
    try:
        p_local1.cambiar_est("CANCELADO")
        assert False, "No debe permitir cancelar desde EN_PREPARACION"
    except ValueError:
        pass

    # 10. Métodos de pago, bloqueo de Tarjeta en Delivery, validación de teléfono y Regla 9
    pago_efectivo = Efectivo(100.0)
    pago_efectivo.procesar_pago(88.80)
    assert "Cambio: Bs 11.20" in pago_efectivo.comprobante()

    pago_tarjeta = Tarjeta()
    assert pago_tarjeta.procesar_pago(100.0) == 103.00

    try:
        ped_ref.registrar_pago(pago_tarjeta)
        assert False, "Delivery no debe aceptar tarjeta"
    except ValueError:
        pass

    devolucion = ped_ref.retraso(75)
    assert devolucion == 15.00
    assert ped_ref.calc_cargos() == 0.00

    try:
        Cliente(2, "Ana", "41234567")
        assert False, "Teléfono inválido debe lanzar error"
    except ValueError:
        pass

    print("Todas las pruebas (10/10) pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_pruebas()