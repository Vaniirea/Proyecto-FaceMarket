-- Crear base de datos
CREATE DATABASE FM_Productos;
GO

-- Usar base de datos
USE FM_Productos;
GO

USE FM_Productos;
GO

-- Crear tabla con campo de Código
CREATE TABLE Productos (
    IdProducto INT PRIMARY KEY IDENTITY(1,1),
    Codigo VARCHAR(10) UNIQUE NOT NULL,   -- Aquí va el código como '001', '002', etc.
    Nombre VARCHAR(100) NOT NULL,
    Precio DECIMAL(10, 2) NOT NULL,
    Inventario INT NOT NULL
);
GO


--10 productos script
INSERT INTO Productos (Codigo, Nombre, Precio, Inventario) VALUES
('001', 'Manzana', 1.00, 50),
('002', 'Banana', 0.60, 40),
('003', 'Pan', 2.00, 30),
('004', 'Leche', 1.80, 25),
('005', 'Jugo de Naranja', 2.50, 20),
('006', 'Huevos (12u)', 3.20, 35),
('007', 'Arroz (1kg)', 1.90, 60),
('008', 'Azúcar (1kg)', 1.70, 45),
('009', 'Aceite (1L)', 3.80, 22),
('010', 'Galletas', 1.50, 50);
GO


--consultar productos
SELECT 
    IdProducto,
    Codigo,
    Nombre,
    Precio,
    Inventario
FROM Productos;
GO
