Bitacora de uso de IA
Proyecto POO

Estudiante: Jhamil Gustavo Mamani Poma

Registro 1

Fecha: 24/11/2026
Herramienta: Gemini
Consulta textual: Hola. Voy a programar mi proyecto de POO en Python, se llama restaurante valluno la idea , sigue estrictamente el PDF guía adjunto y mi diagrama de clases  que también adjunto.

Reglas de trabajo para este chat:
1. Variante asignada: a
2. Fidelidad total al diagrama: Usa exactamente los nombres de clases, atributos protegidos y métodos de mi hoja sellada (Producto, Plato, Bebida, Combo, Combo_Producto, Pedido, Local, Para_llevar, Delivery, Producto_Pedido, Metodo_Pago, Efectivo, QR, Tarjeta, Cliente y Restaurante), sin inventar elementos extra.
3. Estructura del repositorio: Cumple con la estructura de la guía (modelo/productos.py, modelo/pedidos.py, modelo/pagos.py, modelo/clientes.py, restaurante.py, main.py, pruebas.py con al menos 8 assert, y docs/).
4. Restricciones técnicas: Solo biblioteca estándar de Python, polimorfismo real sin usar isinstance ni type, y aplicación estricta de las reglas de mi variante.
5. Metodología: No hagas todo el código por mí. Guíame archivo por archivo en orden de dependencia: yo escribo el código, te lo paso para revisión y corregimos juntos antes de hacer cada commit.

Ya tengo creada la estructura de carpetas y voy a empezar programando modelo/clientes.py, pero antes de nada ayudame a no olvidarme sobre los commits, asi no incumpla con la pista de mal uso de ia.
Qué se aceptó: La aclaracion de ideas respecto a la guia y como empezar a codificar.
Qué se modificó y por qué: Aun nada, el avance que se tenia ahi quedo tal cual.

Registro 2

Fecha: 24/11/2026
Herramienta: Gemini
Consulta textual: Estoy desarrollando un sistema de pedidos en Python con POO. En mi clase Cliente tengo los atributos protegidos _id_cliente, _nombre y _telefono. ¿Cómo puedo usar @property y @telefono.setter para que al instanciar un cliente en __init__ se valide automáticamente que el teléfono tenga 8 dígitos, sea numérico y empiece con 6 o 7, lanzando un ValueError si no cumple?
Qué se aceptó: La estructura de atributos protegidos, los @property de solo lectura y la asignación self.telefono = telefono dentro de __init__ para activar automáticamente el setter.
Qué se modificó y por qué: Se codificó modelo/clientes.py respetando los nombres exactos del diagrama sin agregar __init__.py en modelo/, y se registró el primer commit del módulo.

Registro 3

Fecha: 24/11/2026
Herramienta: Gemini
Consulta textual: Ya tengo lista mi clase Cliente en modelo/clientes.py. Ahora necesito implementar modelo/productos.py con la clase abstracta Producto y sus subclases Plato, Bebida y Combo (usando la clase intermedia Combo_Producto). Según mi variante: Bebida en jarra cuesta el triple que en vaso; Plato recibe una lista opcional de días disponibles; y Combo aplica un 10% de descuento, exige 2 o más productos y puede contener otros combos. ¿Cómo diseño los métodos polimórficos para calcular precios, verificar disponibilidad por día, contar cuántos platos físicos tiene un producto y evitar que un combo se contenga a sí mismo sin usar isinstance()?
Qué se aceptó: El diseño polimórfico de calc_precio(), disponible(dia), contar_platos() y el método recursivo contiene(objetivo) para evitar auto-contención en combos sin usar isinstance().
Qué se modificó y por qué: Se aplicó el descuento del 10% de la Variante A, se normalizaron los nombres de los días sin tildes para evitar fallos de comparación y se documentó contiene() en diagrama_v2.

Registro 4

Fecha: 24/11/2026
Herramienta: Gemini
Consulta textual: Continuando con modelo/pagos.py, tengo la clase abstracta Metodo_Pago y tres subclases: Efectivo (que recibe el monto pagado y calcula el cambio), QR (que valida un código numérico de 10 dígitos) y Tarjeta (que aplica una comisión del 3% sobre el monto). Además, los pedidos de tipo Delivery no pueden pagarse con tarjeta. ¿Cómo estructuro estas clases y sus comprobantes para que Delivery rechace el pago con tarjeta mediante polimorfismo sin usar isinstance()?
Qué se aceptó: La propiedad permite_delivery en Metodo_Pago (sobrescrita en False para Tarjeta) y el formato de comprobantes en cada subclase.
Qué se modificó y por qué: Se añadieron validaciones con ValueError para montos insuficientes en efectivo y códigos numéricos de exactamente 10 dígitos en QR.

Registro 5

Fecha: 24/11/2026
Herramienta: Gemini
Consulta textual: Ahora voy a programar modelo/pedidos.py con Pedido (abstracta), Producto_Pedido, Local, Para_llevar y Delivery. Necesito: 1. Controlar transiciones de estado (REGISTRADO -> EN_PREPARACION -> LISTO -> ENTREGADO, y CANCELADO solo desde REGISTRADO), bloqueando agregar o quitar productos si el estado ya no es REGISTRADO. 2. En Local, validar mesas del 1 al 15 y verificar que no haya otro pedido abierto en la misma mesa. 3. En Para_llevar, cobrar Bs 2 por envase por cada plato físico (incluyendo los que vienen dentro de combos). 4. En Delivery, aplicar tarifas por zona (Cercado Bs 8, Quillacollo Bs 15, Sacaba Bs 15, Vinto Bs 20), pedido mínimo de Bs 40, envío gratis en Cercado desde Bs 150 y devolución del costo de envío si la entrega tarda más de 60 minutos. ¿Cómo organizo estos métodos limpiamente?
Qué se aceptó: El diccionario de transiciones válidas en Pedido, el método abstracto calc_cargos(), verificar_disp() en Local y retraso() en Delivery.
Qué se modificó y por qué: Se integró contar_platos() en Para_llevar para cobrar Bs 2.00 por cada plato físico incluso dentro de combos anidados, y se configuraron las tarifas y reglas de la Variante A.

Registro 6

Fecha: 24/11/2026
Herramienta: Gemini
Consulta textual: Con las clases de modelo/ terminadas, necesito crear la clase gestora Restaurante en restaurante.py y el menú de consola en main.py. En Restaurante debo registrar productos, clientes y pedidos (validando disponibilidad de mesa sin isinstance()), filtrar el menú por día de la semana y generar un reporte con ventas totales por tipo de pedido (sin contar cancelados) y el Top 3 de productos más vendidos. ¿Cómo implemento Restaurante y un menú interactivo en main.py con manejo de errores try/except para que no se caiga ante entradas inválidas?
Qué se aceptó: El filtrado polimórfico por día en menu(), la verificación de mesa con hasattr(pedido, "verificar_disp") sin isinstance() y la estructura del menú en consola.
Qué se modificó y por qué: Se precargaron datos iniciales del restaurante Sabor Valluno en main.py y se agregó una opción específica para registrar retrasos en delivery (Regla 9).

Registro 7

Fecha: 24/11/2026
Herramienta: Gemini
Consulta textual: Por último, quiero armar pruebas.py usando assert y bloques try/except ValueError sin librerías externas. Necesito verificar el caso numérico de referencia de mi variante (Combo de Silpancho Bs 35 + Mocochinchi Bs 6 = Bs 36.90, y 2 combos por delivery a Quillacollo = Bs 88.80), además de combos anidados, prevención de auto-contención, disponibilidad de Chicharrón solo los domingos, envases para llevar, envío gratis en Cercado desde Bs 150, bloqueo de mesa duplicada, transiciones de estado, rechazo de tarjeta en delivery, devolución por retraso mayor a 60 minutos y validación de teléfono. ¿Cómo estructuro estos 10 casos de prueba?
Qué se aceptó: La estructura de 10 casos de prueba automatizados cubriendo tanto los cálculos exactos de la Variante A como las excepciones ValueError esperadas.
Qué se modificó y por qué: Se ejecutó py pruebas.py comprobando que los 10 assert pasan correctamente antes de registrar el commit.

Declaración de autoría: Declaro que he revisado, probado y comprendido cada clase, atributo, propiedad, validación y método implementado en el código fuente, asegurando su total correspondencia con mi diagrama de clases y las reglas de negocio de la Variante A.

Firma: Jhamil Gustavo Mamani Poma