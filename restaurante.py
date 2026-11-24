class Restaurante:
    def __init__(self):
        self._productos = []
        self._clientes = []
        self._pedidos = []

    @property
    def productos(self):
        return list(self._productos)

    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def pedidos(self):
        return list(self._pedidos)

    def registrar_producto(self, producto):
        self._productos.append(producto)

    def menu(self, dia=None):
        if dia is None:
            return list(self._productos)
        return [p for p in self._productos if p.disponible(dia)]

    def registrar_cliente(self, cliente):
        self._clientes.append(cliente)

    def nuevo_pedido(self, pedido):
        if hasattr(pedido, "verificar_disp"):
            if not pedido.verificar_disp(self._pedidos):
                raise ValueError(f"La mesa {pedido.n_mesa} ya tiene un pedido abierto.")
        self._pedidos.append(pedido)

    def reporte(self):
        ventas_por_tipo = {"Local": 0.0, "Para llevar": 0.0, "Delivery": 0.0}
        conteo_productos = {}

        for pedido in self._pedidos:
            if pedido.estado == "CANCELADO":
                continue
            tipo_base = pedido.tipo_pedido().split(" (")[0]
            if tipo_base in ventas_por_tipo:
                ventas_por_tipo[tipo_base] = round(
                    ventas_por_tipo[tipo_base] + pedido.calc_total(), 2
                )
            for item in pedido.pedidos:
                nombre = item.producto.nombre
                conteo_productos[nombre] = conteo_productos.get(nombre, 0) + item.cantidad

        top_3 = sorted(conteo_productos.items(), key=lambda x: x[1], reverse=True)[:3]
        return {
            "ventas_por_tipo": ventas_por_tipo,
            "top_3_productos": top_3,
        }