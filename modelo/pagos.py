from abc import ABC, abstractmethod


class Metodo_Pago(ABC):
    def __init__(self):
        self._permite_delivery = True
        self._ultimo_comprobante = ""

    @property
    def permite_delivery(self):
        return self._permite_delivery

    @abstractmethod
    def procesar_pago(self, monto):
        pass

    def comprobante(self):
        return self._ultimo_comprobante


class Efectivo(Metodo_Pago):
    def __init__(self, cancelado):
        super().__init__()
        if cancelado <= 0:
            raise ValueError("El monto en efectivo debe ser mayor que cero.")
        self._cancelado = round(float(cancelado), 2)

    @property
    def cancelado(self):
        return self._cancelado

    def procesar_pago(self, monto):
        total = round(float(monto), 2)
        if self._cancelado < total:
            raise ValueError("El efectivo recibido no cubre el total del pedido.")
        cambio = round(self._cancelado - total, 2)
        self._ultimo_comprobante = (
            f"Método: Efectivo | Total: Bs {total:.2f} | "
            f"Recibido: Bs {self._cancelado:.2f} | Cambio: Bs {cambio:.2f}"
        )
        return total


class QR(Metodo_Pago):
    def __init__(self, codigo):
        super().__init__()
        cod = str(codigo).strip()
        if len(cod) != 10 or not cod.isdigit():
            raise ValueError("El código de transacción QR debe tener 10 dígitos.")
        self._codigo = cod

    @property
    def codigo(self):
        return self._codigo

    def procesar_pago(self, monto):
        total = round(float(monto), 2)
        self._ultimo_comprobante = (
            f"Método: QR | Total: Bs {total:.2f} | Código transacción: {self._codigo}"
        )
        return total


class Tarjeta(Metodo_Pago):
    def __init__(self, comision=0.03):
        super().__init__()
        self._permite_delivery = False
        self._comision = float(comision)

    @property
    def comision(self):
        return self._comision

    def procesar_pago(self, monto):
        subtotal = round(float(monto), 2)
        recargo = round(subtotal * self._comision, 2)
        total_final = round(subtotal + recargo, 2)
        self._ultimo_comprobante = (
            f"Método: Tarjeta | Pedido: Bs {subtotal:.2f} | "
            f"Comisión (3%): Bs {recargo:.2f} | Total cobrado: Bs {total_final:.2f}"
        )
        return total_final