class Cliente:

    def __init__(self, id_cliente, nombre, telefono):
        self._id_cliente = id_cliente
        self._nombre = nombre
        self.telefono = telefono

    @property
    def id_cliente(self):
        return self._id_cliente

    @property
    def nombre(self):
        return self._nombre

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        tel = str(valor).strip()
        if len(tel) != 8 or not tel.isdigit() or tel[0] not in ("6", "7"):
            raise ValueError("El teléfono debe tener 8 dígitos y empezar con 6 o 7.")
        self._telefono = tel


