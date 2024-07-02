CREATE TABLE Cliente(
    Id_Cliente INT NOT NULL AUTO_INCREMENT,
    Nombre VARCHAR(15),
    ApellidoPaterno VARCHAR(15),
    ApellidoMaterno VARCHAR(15),
    DNI VARCHAR(8),
    TallaDerecha DECIMAL(4,2),
    TallaIzquierda DECIMAL(4,2),
    Imagen LONGBLOB,
    PRIMARY KEY (Id_Cliente)
);