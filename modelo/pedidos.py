from abc import ABC, abstractmethod


class Producto_Pedido:
    def __init__(self, pedido, producto, cantidad=1):
        if cantidad < 1 or cantidad > 20:
            raise ValueError("La cantidad de un producto en el pedido debe ir de 1 a 20.")
        self._pedido = pedido
        self._producto = producto
        self._cantidad = int(cantidad)

    @property
    def pedido(self):
        return self._pedido

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if valor < 1 or valor > 20:
            raise ValueError("La cantidad de un producto en el pedido debe ir de 1 a 20.")
        self._cantidad = int(valor)

    def calc_subtotal(self):
        return round(self._producto.calc_precio() * self._cantidad, 2)

    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad


class Pedido(ABC):
    TRANSICIONES = {
        "REGISTRADO": ("EN_PREPARACION", "CANCELADO"),
        "EN_PREPARACION": ("LISTO",),
        "LISTO": ("ENTREGADO",),
        "ENTREGADO": (),
        "CANCELADO": (),
    }

    def __init__(self, cliente):
        self._cliente = cliente
        self._pedidos = []
        self._estado = "REGISTRADO"
        self._metodo_pago = None

    @property
    def cliente(self):
        return self._cliente

    @property
    def pedidos(self):
        return list(self._pedidos)

    @property
    def estado(self):
        return self._estado

    @property
    def metodo_pago(self):
        return self._metodo_pago

    def agregar(self, producto, cantidad=1):
        if self._estado != "REGISTRADO":
            raise ValueError("Solo se pueden agregar productos en estado REGISTRADO.")
        for item in self._pedidos:
            if item.producto is producto:
                item.cantidad = item.cantidad + cantidad
                return
        self._pedidos.append(Producto_Pedido(self, producto, cantidad))

    def quitar(self, producto):
        if self._estado != "REGISTRADO":
            raise ValueError("Solo se pueden quitar productos en estado REGISTRADO.")
        for item in self._pedidos:
            if item.producto is producto:
                self._pedidos.remove(item)
                return
        raise ValueError("El producto no se encuentra en el pedido.")

    def cambiar_est(self, nuevo_estado):
        destino = str(nuevo_estado).strip().upper()
        if destino not in self.TRANSICIONES.get(self._estado, ()):
            raise ValueError(f"Cambio de estado inválido: {self._estado} -> {destino}.")
        self._estado = destino

    def _calc_subtotal(self):
        return round(sum(item.calc_subtotal() for item in self._pedidos), 2)

    @abstractmethod
    def calc_cargos(self):
        pass

    def calc_total(self):
        if not self._pedidos:
            raise ValueError("El pedido no contiene productos.")
        return round(self._calc_subtotal() + self.calc_cargos(), 2)

    def _validar_metodo_pago(self, metodo_pago):
        pass

    def registrar_pago(self, metodo_pago):
        self._validar_metodo_pago(metodo_pago)
        total = self.calc_total()
        metodo_pago.procesar_pago(total)
        self._metodo_pago = metodo_pago
        return metodo_pago.comprobante()

    def tipo_pedido(self):
        return "Pedido"

    def mostrar_detalle(self):
        lineas = [
            f"--- Detalle de Pedido ({self.tipo_pedido()}) ---",
            f"Cliente: {self._cliente.nombre} (Tel: {self._cliente.telefono})",
            f"Estado: {self._estado}",
            "Productos:",
        ]
        for item in self._pedidos:
            lineas.append(
                f"  - {item.producto.nombre} x{item.cantidad}: Bs {item.calc_subtotal():.2f}"
            )
        subtotal = self._calc_subtotal()
        cargos = self.calc_cargos()
        total = round(subtotal + cargos, 2)
        lineas.append(f"Subtotal: Bs {subtotal:.2f}")
        lineas.append(f"Cargos adicionales: Bs {cargos:.2f}")
        lineas.append(f"Total: Bs {total:.2f}")
        if self._metodo_pago is not None:
            lineas.append(self._metodo_pago.comprobante())
        return "\n".join(lineas)


class Local(Pedido):
    def __init__(self, cliente, n_mesa):
        super().__init__(cliente)
        mesa = int(n_mesa)
        if mesa < 1 or mesa > 15:
            raise ValueError("El número de mesa debe estar entre 1 y 15.")
        self._n_mesa = mesa

    @property
    def n_mesa(self):
        return self._n_mesa

    def tipo_pedido(self):
        return f"Local (Mesa {self._n_mesa})"

    def verificar_disp(self, pedidos_existentes):
        for pedido in pedidos_existentes:
            if pedido is not self and getattr(pedido, "n_mesa", None) == self._n_mesa:
                if pedido.estado not in ("ENTREGADO", "CANCELADO"):
                    return False
        return True

    def calc_cargos(self):
        return 0.0


class Para_llevar(Pedido):
    def __init__(self, cliente, envase=2.0):
        super().__init__(cliente)
        self._envase = round(float(envase), 2)

    @property
    def envase(self):
        return self._envase

    def tipo_pedido(self):
        return "Para llevar"

    def calc_cargos(self):
        total_platos = sum(item.contar_platos() for item in self._pedidos)
        return round(total_platos * self._envase, 2)


class Delivery(Pedido):
    TARIFAS_ZONA = {
        "cercado": 8.0,
        "quillacollo": 15.0,
        "sacaba": 15.0,
        "vinto": 20.0,
    }

    def __init__(self, cliente, lugar):
        super().__init__(cliente)
        zona = str(lugar).strip().lower()
        if zona not in self.TARIFAS_ZONA:
            raise ValueError("Zona no válida. Opciones: Cercado, Quillacollo, Sacaba, Vinto.")
        self._lugar = zona.capitalize()
        self._c_envio = self.TARIFAS_ZONA[zona]
        self._devolucion_retraso = 0.0

    @property
    def lugar(self):
        return self._lugar

    @property
    def c_envio(self):
        return self._c_envio

    def tipo_pedido(self):
        return f"Delivery ({self._lugar})"

    def _validar_metodo_pago(self, metodo_pago):
        if not metodo_pago.permite_delivery:
            raise ValueError("El delivery solo acepta pago en Efectivo o QR.")

    def calc_cargos(self):
        subtotal = self._calc_subtotal()
        if subtotal < 40.0:
            raise ValueError("El pedido mínimo para delivery es de Bs 40.00.")
        if self._lugar.lower() == "cercado" and subtotal >= 150.0:
            costo = 0.0
        else:
            costo = self._c_envio
        return round(max(0.0, costo - self._devolucion_retraso), 2)

    def retraso(self, minutos_entrega):
        if minutos_entrega > 60:
            envio_cobrado = self.calc_cargos()
            self._devolucion_retraso = envio_cobrado
            return round(envio_cobrado, 2)
        return 0.0