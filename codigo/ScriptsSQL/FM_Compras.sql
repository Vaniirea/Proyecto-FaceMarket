-- Crear base de datos
CREATE DATABASE FM_Compras;
GO

-- Usar base de datos
USE FM_Compras;
GO

-- Crear tabla Compras
CREATE TABLE Compras (
    IdCompra INT PRIMARY KEY IDENTITY(1,1),
    Fecha DATETIME NOT NULL DEFAULT GETDATE(),
    Total DECIMAL(10, 2) NOT NULL,
    IdClienteCompro INT NOT NULL
    -- NOTA: FK cruzada a FM_Clientes no se puede definir directamente
);
GO
