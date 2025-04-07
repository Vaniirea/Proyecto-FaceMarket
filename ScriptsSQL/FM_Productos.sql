-- Crear base de datos
CREATE DATABASE FM_Clientes;
GO

-- Usar base de datos
USE FM_Clientes;
GO

-- Crear tabla Clientes
CREATE TABLE Clientes (
    IdCliente INT PRIMARY KEY IDENTITY(1,1),
    Nombre VARCHAR(100) NOT NULL,
    Saldo DECIMAL(10, 2) NOT NULL
);
GO

--Ver clientes
SELECT IdCliente, Nombre, Saldo
FROM Clientes;
GO

--primer cliente 
INSERT INTO Clientes (Nombre, Saldo)
VALUES ('Vani Rea', 100.00);
GO
