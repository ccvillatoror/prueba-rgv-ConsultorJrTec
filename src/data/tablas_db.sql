------------------------------------------------------------------------------------------------
--------------- Archivo de los comandos para crear las tablas de la Base de Datos --------------
------------------------------------------------------------------------------------------------

-- Creación de tablas de la base de datos

DROP TABLE IF EXISTS cuentas;
DROP TABLE IF EXISTS gastos;
DROP TABLE IF EXISTS pagos;
DROP TABLE IF EXISTS usuarios;

CREATE TABLE cuentas(idCuenta SERIAL NOT NULL primary key, saldo decimal(11,2) NOT NULL);

CREATE TABLE gastos(idGasto SERIAL NOT NULL primary key, 
                    fechaGasto date NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                    concepto varchar(100) NOT NULL, 
                    montoGastado decimal(10,2) NOT NULL, 
                    estado varchar(20) NOT NULL DEFAULT 'En proceso' CHECK (estado IN ('Cancelado', 'Aprobado', 'Liquidado', 'En proceso')), 
                    montoPagado decimal(10,2) NOT NULL DEFAULT '0');

CREATE TABLE pagos(idPago SERIAL NOT NULL primary key,
                   fechaPago date NOT NULL DEFAULT CURRENT_TIMESTAMP, 
                   idGasto INT NOT NULL,
                   foreign key (idGasto) references gastos (idGasto),
                   cuentaAsociada INT NOT NULL DEFAULT 1,
                   foreign key (cuentaAsociada) references cuentas (idCuenta),
                   montoPagado decimal(10,2) NOT NULL DEFAULT '0',
                   estado varchar(20) NOT NULL DEFAULT 'En proceso' CHECK (estado IN ('Cancelado', 'Aprobado', 'En proceso')));

CREATE TABLE usuarios(idUsuario SERIAL NOT NULL primary key,
                      usuario varchar(20) NOT NULL UNIQUE,
                      contraseña varchar(180) NOT NULL);