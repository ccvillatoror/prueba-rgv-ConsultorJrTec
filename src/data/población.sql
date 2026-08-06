-- Instertar el saldo en la cuenta
INSERT INTO cuentas (idCuenta, saldo) VALUES (1, 1000000);
INSERT INTO cuentas (idCuenta, saldo) VALUES (2, 5000);


-- Población inicial de gastos
INSERT INTO gastos (idGasto, fechaGasto, concepto, montoGastado)
        VALUES (1, '2026-07-27', 'Compra de insumos', 3000.00); -- Aprobado

INSERT INTO gastos (idGasto, fechaGasto, concepto, montoGastado)
        VALUES(2, '2026-07-28', 'Compra plásticos Pablín', 6000.00); -- Cancelado

INSERT INTO gastos (idGasto, fechaGasto, concepto, montoGastado)
        VALUES(3, '2026-07-14', 'Muebles de aparadores', 40000.00); -- Liquidado

INSERT INTO gastos (idGasto, fechaGasto, concepto, montoGastado)
        VALUES(4, '2026-07-15', 'Chocolates Turín', 5560.00); -- Aprobado

INSERT INTO gastos (idGasto, fechaGasto, concepto, montoGastado)
        VALUES(5, '2026-07-15', 'Caramelos', 5560.00); -- En proceso

-- Actualizar estados de gastos para poder agregar pagos
UPDATE gastos SET estado='Aprobado' WHERE idGasto=1 OR idGasto=3 OR idGasto=4;
UPDATE gastos SET estado='Cancelado' WHERE idGasto=2;


-- Población inicial de pagos
INSERT INTO pagos (idPago, fechaPago, idGasto, montoPagado, estado, cuentaAsociada)
    VALUES (1, '2026-08-01', 1, 2000.00, 'Aprobado', 1);

INSERT INTO pagos (idPago, fechaPago, idGasto, montoPagado, estado, cuentaAsociada)
    VALUES (2, '2026-08-01', 3, 20000.00, 'Aprobado', 1);

INSERT INTO pagos (idPago, fechaPago, idGasto, montoPagado, cuentaAsociada)
    VALUES (3, '2026-07-30', 3, 20000.00, 1);

INSERT INTO pagos (idPago, fechaPago, idGasto, montoPagado)
    VALUES (4, '2026-07-30', 4, 1000.00); -- Cancelado

-- Actualizar estados de pagos para afectar los gastos.
UPDATE pagos SET estado='Aprobado' WHERE idGasto=1 OR idGasto=3;
UPDATE pagos SET estado='Cancelado' WHERE idGasto=4;

/*
--------- R E S U L T A D O S ---------

-------CUENTAS--------
 idcuenta |   saldo   
----------+-----------
        2 |   5000.00
        1 | 958000.00
(2 rows)



-----------------------------------------GASTOS------------------------------------------
 idgasto | fechagasto |        concepto         | montogastado |   estado   | montopagado 
---------+------------+-------------------------+--------------+------------+-------------
       5 | 2026-07-15 | Caramelos               |      5560.00 | En proceso |        0.00
       4 | 2026-07-15 | Chocolates Turín        |      5560.00 | Aprobado   |        0.00
       2 | 2026-07-28 | Compra plásticos Pablín |      6000.00 | Cancelado  |        0.00
       1 | 2026-07-27 | Compra de insumos       |      3000.00 | Aprobado   |     2000.00
       3 | 2026-07-14 | Muebles de aparadores   |     40000.00 | Liquidado  |    40000.00
(5 rows)


-----------------------------------------PAGOS----------------------------
 idpago | fechapago  | idgasto | cuentaasociada | montopagado |  estado   
--------+------------+---------+----------------+-------------+-----------
      1 | 2026-08-01 |       1 |              1 |     2000.00 | Aprobado
      2 | 2026-08-01 |       3 |              1 |    20000.00 | Aprobado
      3 | 2026-07-30 |       3 |              1 |    20000.00 | Aprobado
      4 | 2026-07-30 |       4 |              1 |     1000.00 | Cancelado
(4 rows)


*/