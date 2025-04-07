[Volver al README](https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/README.md)

## Fase de Desarrollo

Durante esta fase se han implementado todas las funcionalidades principales del sistema. A continuación, se detallan los componentes desarrollados, su estado actual y su propósito dentro del sistema.

### Reconocimiento facial
Se implementó un sistema de reconocimiento facial basado en imágenes previamente almacenadas por cliente. Cada cliente tiene una carpeta en el sistema (`faces/IDCliente/`) que contiene múltiples imágenes con diferentes ángulos y expresiones para aumentar la precisión. Estas imágenes son codificadas al iniciar el programa y comparadas en tiempo real al momento del pago. Este reconocimiento permite identificar al cliente sin requerir interacción manual.

### Base de datos y conexión
Se implementaron tres bases de datos independientes en SQL Server:
- **FM_Clientes**: Almacena el nombre del cliente y su saldo.
- **FM_Productos**: Contiene todos los productos disponibles con código, nombre, precio e inventario.
- **FM_Compras**: Preparada para registrar futuras compras por cliente.

El sistema se conecta automáticamente a las bases mediante el archivo `conexion.py` y obtiene datos en tiempo real al ejecutar acciones dentro del sistema (como escanear productos o consultar saldo).

### Carga dinámica de productos
Los productos se cargan desde la base de datos `FM_Productos` en lugar de estar definidos directamente en el código. Se implementó una función que lee todos los productos al iniciar el programa y permite agregarlos al carrito ingresando su código.

### Validación de saldo y pago
El cliente puede seleccionar la opción “Pagar con Face ID”, momento en el cual el sistema:
1. Verifica su rostro con la base de datos de imágenes.
2. Consulta su saldo en la base de datos.
3. Si el saldo es suficiente, descuenta el monto total de la compra.
4. Muestra un mensaje de confirmación y genera el ticket de compra.

Si no hay saldo suficiente, se muestra una alerta y no se permite continuar con el pago.

### Interfaz gráfica del sistema
La interfaz fue diseñada en `tkinter` y está compuesta por tres pantallas principales:
- **ProductPage**: Permite escanear productos, ver el carrito y proceder al pago.
- **PaymentPage**: Muestra el total a pagar y ofrece métodos como Face ID, tarjeta y QR.
- **TicketPage**: Genera un resumen de compra y permite guardar un ticket en formato `.txt`.

Los colores, botones y tipografías fueron ajustados para que la experiencia sea clara, moderna y accesible.

### Seguimiento SCRUM
Se utilizaron tableros tipo Kanban en GitHub Projects para llevar el control de tareas por sprint. Entre las tareas marcadas como completadas están:
- Captura y codificación de imágenes.
- Entrenamiento y pruebas del sistema de reconocimiento facial.
- Creación y conexión de bases de datos.
- Validación de saldo y ejecución de pagos.
- Generación de reportes visuales y tickets.

## Código
#### Conexion.py
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/codigo/conexion.py
#### Diseño.py
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/codigo/dise%C3%B1o.py
#### Cara.py
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/codigo/face.py
#### Main.py
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/codigo/main.py
#### Pueba.py
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/codigo/prueba.py
#### Pueba por foto.py
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/codigo/prueba_por_foto.py

## Imagenes
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/Imagenes.md

## Script De BD
#### FM_Clientes
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/ScriptsSQL/FM_Clientes.sql
#### FM_Compras
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/ScriptsSQL/FM_Compras.sql
#### FM_Productos
https://github.com/Vaniirea/Proyecto-FaceMarket/blob/main/ScriptsSQL/FM_Productos.sql
