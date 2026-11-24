Sistema de Pedidos - Restaurante Sabor Valluno
Proyecto Final de Programacion Orientada a Objetos

Estudiante: Jhamil Gustavo Mamani Poma
Variante asignada: A

De que trata este proyecto:
Este programa es un sistema de consola hecho en Python para administrar los pedidos de un restaurante llamado Sabor Valluno. Permite registrar platos, bebidas, combos y clientes, tomar pedidos en mesa, para llevar o por delivery, calcular cobros segun el metodo de pago y ver un resumen de las ventas del dia.

Como estan organizados los archivos:
1. modelo/clientes.py: Guarda los datos de cada cliente y revisa que su numero de telefono tenga 8 digitos y empiece con 6 o 7.
2. modelo/productos.py: Maneja los platos, bebidas (en vaso o en jarra) y combos con descuento.
3. modelo/pagos.py: Controla los cobros en efectivo (calculando el cambio), por QR (con codigo de 10 digitos) y con tarjeta (con recargo del 3 por ciento).
4. modelo/pedidos.py: Gestiona los pedidos en local (mesas 1 a 15), para llevar (cobrando envases) y delivery (calculando envio por zona), ademas de los estados del pedido.
5. restaurante.py: Es la clase principal que conecta todo el sistema, filtra el menu por dia y arma el reporte de ventas.
6. main.py: Es el menu interactivo en consola para usar el programa paso a paso.
7. pruebas.py: Contiene 10 pruebas automaticas para comprobar que todos los calculos y validaciones funcionen sin errores.
8. docs: Carpeta con los diagramas de clases, el acta de consultas al docente y la bitacora de uso de IA.

Reglas principales del negocio (Variante A):
1. Combos: Se arman con 2 o mas productos y tienen un 10 por ciento de descuento. Un combo no puede contenerse a si mismo.
2. Disponibilidad: El chicharron solo esta disponible los domingos, y si un combo lleva chicharron tambien estara disponible solo ese dia.
3. Bebidas: Una bebida en jarra cuesta el triple que en vaso.
4. Para llevar: Se cobra Bs 2 por envase por cada plato incluido en el pedido.
5. Delivery: El pedido minimo es de Bs 40. El envio cuesta Bs 8 en Cercado (gratis si el pedido llega a Bs 150), Bs 15 en Quillacollo o Sacaba, y Bs 20 en Vinto. Solo se puede pagar en efectivo o QR.
6. Retraso en delivery: Si la entrega tarda mas de 60 minutos, se devuelve el costo de envio al cliente.

Como ejecutar el programa:
Abre la terminal dentro de la carpeta restaurante-proyecto-poo y escribe uno de estos comandos:

Para correr las 10 pruebas automaticas:
py pruebas.py

Para abrir el menu del restaurante en consola:
py main.py