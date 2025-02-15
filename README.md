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
Se utilizará **SCRUM**, una metodología ágil que facilita la gestión de proyectos complejos mediante ciclos iterativos llamados sprints. Cada sprint tiene una duración fija, generalmente de dos semanas, y se enfoca en entregar incrementos funcionales del producto. Los componentes clave de SCRUM incluyen:

1. **Roles**
   - **Product Owner (Propietario del Producto)**: Gestiona el Product Backlog, priorizando las funcionalidades según el valor para el negocio.
   - **Scrum Master**: Facilita el proceso SCRUM, eliminando impedimentos y asegurando que el equipo siga las prácticas ágiles.
   - **Equipo de Desarrollo**: Grupo multidisciplinario responsable de construir el producto.

2. **Artefactos**
   - **Product Backlog**: Lista priorizada de requisitos y funcionalidades del producto.
   - **Sprint Backlog**: Conjunto de tareas seleccionadas del Product Backlog para el sprint actual.
   - **Incremento**: Resultado funcional entregable al final de cada sprint.

3. **Eventos**
   - **Sprint Planning**: Reunión para planificar el trabajo del próximo sprint.
   - **Daily Scrum**: Reunión diaria de 15 minutos para sincronizar al equipo.
   - **Sprint Review**: Revisión del incremento al final del sprint.
   - **Sprint Retrospective**: Reflexión sobre el proceso para identificar mejoras.
## Cronograma de Actividades
- **Actividad Principal**:	Subtemas	Fecha Inicio	Fecha Final
- **Análisis y Planificación-**	Definir los requerimientos detallados del sistema.	03/02/2025	16/02/2025
	Diseñar la arquitectura del sistema y la base de datos.	03/02/2025	16/02/2025
	Seleccionar tecnologías adecuadas (Python, OpenCV, SQL Server).	03/02/2025	16/02/2025
- **Desarrollo del Reconocimiento Facial**:	Implementar la captura y procesamiento de imágenes.	17/02/2025	16/03/2025
	Entrenar modelos de reconocimiento facial.	17/02/2025	16/03/2025
	Pruebas de precisión y mejora del modelo.	17/02/2025	16/03/2025
- **Integración con la Base de Datos**:	Crear la base de datos de clientes y productos.	17/03/2025	30/03/2025
	Desarrollar la conexión del sistema con la base de datos.	17/03/2025	30/03/2025
	Implementar consultas de saldo y compras.	17/03/2025	30/03/2025
- **Implementación del Módulo de Compras**:	Integrar el reconocimiento facial con el sistema de pagos.	31/03/2025	13/04/2025
	Validar la disponibilidad del saldo del cliente.	31/03/2025	13/04/2025
	Generar reportes de compras y transacciones.	31/03/2025	13/04/2025
- **Desarrollo de la Interfaz de Usuario**:	Crear la interfaz para clientes y administradores.	14/04/2025	27/04/2025
	Optimizar la usabilidad y experiencia del usuario.	14/04/2025	27/04/2025
	Realizar pruebas de funcionalidad.	14/04/2025	27/04/2025
- **Pruebas y Optimización**:	Realizar pruebas unitarias e integrales.	28/04/2025	11/05/2025
	Optimizar el rendimiento y corregir errores.	28/04/2025	11/05/2025
	Garantizar la seguridad de los datos.	28/04/2025	11/05/2025
- **Despliegue y Documentación**:	Implementar el sistema en un entorno real.	12/05/2025	23/05/2025
	Capacitar a los administradores de la tienda.	12/05/2025	23/05/2025
	Redactar documentación técnica y manuales de usuario.	12/05/2025	23/05/2025

![Diagrama de la metodologia SCRUM](images/metodologia-scrum.png)

