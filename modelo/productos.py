from abc import ABC, abstractmethod


def _normalizar_dia(dia):
    texto = str(dia).strip().lower()
    reemplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
    for acento, plano in reemplazos.items():
        texto = texto.replace(acento, plano)
    return texto


class Producto(ABC):
    def __init__(self, nombre, precio):
        if precio <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._nombre = str(nombre).strip()
        self._precio = round(float(precio), 2)

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = round(float(valor), 2)

    def contiene(self, objetivo):
        return self is objetivo

    @abstractmethod
    def calc_precio(self):
        pass

    @abstractmethod
    def disponible(self, dia):
        pass

    @abstractmethod
    def contar_platos(self):
        pass


class Plato(Producto):
    TODOS_LOS_DIAS = (
        "lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"
    )

    def __init__(self, nombre, precio, dias_disp=None):
        super().__init__(nombre, precio)
        if dias_disp:
            self._dias_disp = tuple(_normalizar_dia(d) for d in dias_disp)
        else:
            self._dias_disp = self.TODOS_LOS_DIAS

    @property
    def dias_disp(self):
        return self._dias_disp

    def disponible(self, dia):
        return _normalizar_dia(dia) in self._dias_disp

    def calc_precio(self):
        return round(self._precio, 2)

    def contar_platos(self):
        return 1


class Bebida(Producto):
    def __init__(self, nombre, precio, tipo_envase="vaso"):
        super().__init__(nombre, precio)
        envase = str(tipo_envase).strip().lower()
        if envase not in ("vaso", "jarra"):
            raise ValueError("El tipo de envase de la bebida debe ser 'vaso' o 'jarra'.")
        self._tipo_envase = envase

    @property
    def tipo_envase(self):
        return self._tipo_envase

    def calc_precio(self):
        if self._tipo_envase == "jarra":
            return round(self._precio * 3, 2)
        return round(self._precio, 2)

    def disponible(self, dia):
        return True

    def contar_platos(self):
        return 0


class Combo_Producto:
    def __init__(self, producto, cantidad=1):
        if cantidad < 1 or cantidad > 20:
            raise ValueError("La cantidad debe estar entre 1 y 20.")
        self._producto = producto
        self._cantidad = int(cantidad)

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor):
        if valor < 1 or valor > 20:
            raise ValueError("La cantidad debe estar entre 1 y 20.")
        self._cantidad = int(valor)


class Combo(Producto):
    DESCUENTO_VARIANTE_A = 0.10

    def __init__(self, nombre):
        super().__init__(nombre, 1.0)
        self._productos = []

    @property
    def productos(self):
        return list(self._productos)

    def contiene(self, objetivo):
        if self is objetivo:
            return True
        for item in self._productos:
            if item.producto.contiene(objetivo):
                return True
        return False

    def agregar_p(self, producto, cantidad=1):
        if producto.contiene(self):
            raise ValueError("Un combo no puede contenerse a sí mismo.")
        for item in self._productos:
            if item.producto is producto:
                item.cantidad = item.cantidad + cantidad
                return
        self._productos.append(Combo_Producto(producto, cantidad))

    def calc_precio(self):
        total_items = sum(item.cantidad for item in self._productos)
        if total_items < 2:
            raise ValueError("Un combo debe contener 2 o más productos.")
        suma = sum(item.producto.calc_precio() * item.cantidad for item in self._productos)
        return round(suma * (1 - self.DESCUENTO_VARIANTE_A), 2)

    def disponible(self, dia):
        if not self._productos:
            return False
        for item in self._productos:
            if not item.producto.disponible(dia):
                return False
        return True

    def contar_platos(self):
        return sum(item.producto.contar_platos() * item.cantidad for item in self._productos)