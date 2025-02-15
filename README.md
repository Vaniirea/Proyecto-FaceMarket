# Sistema de Reconocimiento Facial para Compras Inteligentes

## Descripción
Este proyecto tiene como objetivo desarrollar un sistema de reconocimiento facial que identifique a los clientes en una tienda y se conecte a una base de datos para verificar su saldo disponible y los productos que están comprando. Optimiza la experiencia de compra y la seguridad del proceso de pago mediante la autenticación facial.

## Integrantes del Equipo
- **Evanibaldo Rea Aviña** - Lider del proyecto
- **Juan José Hernández Olmos** - Desarrollo Backend
- **Juan Francisco Reyes Jasso** - Desarrollo de la Interfaz
- **Evanibaldo Rea Aviña** - Integración y Base de Datos

## Objetivo del Proyecto
Desarrollar un sistema basado en reconocimiento facial que identifique a los clientes en una tienda y se conecte a una base de datos para verificar su saldo disponible y los productos adquiridos. Esto permitirá agilizar el proceso de compra y mejorar la seguridad en los pagos.

## Alcance del Proyecto
1. **Autenticación del Cliente**: Identificación mediante reconocimiento facial.
2. **Conexión con la Base de Datos**: Consulta del saldo disponible y los productos comprados.
3. **Verificación de Saldo**: Validación de la capacidad de pago del cliente.
4. **Registro de Compras**: Almacenamiento de los productos adquiridos.
5. **Interfaz para Administradores**: Panel de control para la gestión de clientes, productos y ventas.
6. **Notificaciones y Alertas**: Avisos en caso de saldo insuficiente y opciones de pago alternativo.

## Requerimientos
### Requerimientos Funcionales
1. **Autenticación del Cliente**
   - Identificación del cliente mediante reconocimiento facial.
   - Acceso a su información financiera y de compras.
2. **Gestor de Compras**
   - Consulta de saldo antes de realizar una compra.
   - Registro automático de los productos adquiridos.
3. **Interfaz Administrativa**
   - Panel de gestión de clientes, productos y ventas.
   - Emisión de reportes de transacciones.
4. **Notificaciones**
   - Alertas por saldo insuficiente y sugerencia de métodos de pago.

### Requerimientos No Funcionales
1. **Seguridad**
   - Cifrado de datos para proteger la información del cliente.
2. **Escalabilidad**
   - Permitir la incorporación de nuevos clientes y productos sin afectar el rendimiento.
3. **Usabilidad**
   - Interfaz intuitiva para clientes y administradores.
4. **Rendimiento**
   - Identificación facial en menos de 5 segundos.
5. **Disponibilidad**
   - Operativo al menos el 80% del tiempo laboral.

## Metodología de Desarrollo
Se utilizará **SCRUM**, una metodología ágil que permite desarrollar el sistema en ciclos iterativos, con entregas incrementales y pruebas constantes. Se organizarán sprints de 2 semanas.

**Tecnologías Utilizadas**
- **Lenguaje de Programación**: Python
- **Librerías**: OpenCV para el reconocimiento facial
- **Base de Datos**: SQL Server
- **Metodología de Desarrollo**: SCRUM
