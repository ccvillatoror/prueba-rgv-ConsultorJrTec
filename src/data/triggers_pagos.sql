------------------------------------------------------------------------------------------------
--------- Archivo de todas las funciones y triggers relacionadas con la tabla de pagos ---------
------------------------------------------------------------------------------------------------


-- Al agregar un nuevo pago, verifica que el monto a pagar sea menor al monto que queda por pagar del gasto asociado.
CREATE OR REPLACE FUNCTION fn_validar_monto_pagos()
RETURNS TRIGGER AS $$
DECLARE 
    montoDisponible decimal(10,2);
    estadoGasto varchar(20);
BEGIN
    SELECT gastos.montoGastado - gastos.montoPagado, gastos.estado
    INTO montoDisponible, estadoGasto
    FROM gastos
    WHERE gastos.idGasto = NEW.idGasto;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'El gasto con idGasto % no existe.', NEW.idGasto;
    END IF;

    IF estadoGasto IS DISTINCT FROM 'Aprobado' THEN
        RAISE EXCEPTION 'El gasto está % y no puede recibir pagos.', estadoGasto;
    END IF;

    IF NEW.montoPagado > montoDisponible THEN
        RAISE EXCEPTION 'El monto del pago (%) excede el saldo del gasto (%).', 
            NEW.montoPagado, montoDisponible;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crea trigger para la función anterior, se activa para cada pago agregado
CREATE TRIGGER trg_validar_monto_pagos
BEFORE INSERT ON pagos
FOR EACH ROW
EXECUTE FUNCTION fn_validar_monto_pagos();

-- Función para que todos los pagos inicialmente agregados sean siempre en estado 'En proceso'
CREATE OR REPLACE FUNCTION fn_forzar_estado_inicial_pagos()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.estado IS DISTINCT FROM 'En proceso' THEN
        RAISE WARNING 'El pago será creado con estado ''En proceso'' (recibido: %).', NEW.estado;
    END IF;

    NEW.estado = 'En proceso';

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger de la función anterior, se activa al agregar un nuevo pago.
CREATE TRIGGER trg_forzar_estado_inicial_pagos
BEFORE INSERT ON pagos
FOR EACH ROW
EXECUTE FUNCTION fn_forzar_estado_inicial_pagos();


-- Verificar que al Aceptar un pago, el saldo en Cuenta sea suficiente y restarle el saldo de ser el caso.
CREATE OR REPLACE FUNCTION fn_actualizar_saldo_pagado()
RETURNS TRIGGER AS $$
DECLARE
    saldoDisponible decimal(10,2);
BEGIN
    SELECT saldo
    INTO saldoDisponible
    FROM cuentas
    WHERE idCuenta = NEW.cuentaAsociada;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'La cuenta % no existe.', NEW.cuentaAsociada;
    END IF;

    IF saldoDisponible < NEW.montoPagado THEN
        RAISE EXCEPTION 'No hay suficiente saldo para completar la transacción.';
    END IF;

    UPDATE cuentas
    SET saldo = saldo - NEW.montoPagado
    WHERE idCuenta = NEW.cuentaAsociada;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crea trigger para la función anterior, se activa al actualizar un pago
CREATE TRIGGER trg_02_actualizar_saldo_pagado
BEFORE UPDATE ON pagos
FOR EACH ROW
WHEN (OLD.estado IS DISTINCT FROM 'Aprobado' AND NEW.estado = 'Aprobado')
EXECUTE FUNCTION fn_actualizar_saldo_pagado();

-- Actualizar el montoPagado en el gasto asociado al Aprobar un pago.
CREATE OR REPLACE FUNCTION fn_aumentar_monto_pagado()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE gastos
    SET montoPagado = gastos.montoPagado + NEW.montoPagado
    WHERE gastos.idGasto = NEW.idGasto;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crea trigger para la función anterior, se activa al actualizar un pago
CREATE TRIGGER trg_aumentar_monto_pagado
AFTER UPDATE ON pagos
FOR EACH ROW
WHEN (OLD.estado IS DISTINCT FROM 'Aprobado' AND NEW.estado = 'Aprobado')
EXECUTE FUNCTION fn_aumentar_monto_pagado();

-- Un pago no puede pasar de Aprobado a Cancelado, ni se puede cambiar el estado ya cancelado.
CREATE OR REPLACE FUNCTION fn_verificar_transicion_estado_pagos()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.estado = 'Cancelado' THEN
        RAISE EXCEPTION 'El pago % está cancelado y no puede cambiar de estado.', OLD.idPago;
    END IF;

    IF OLD.estado = 'Aprobado' THEN
        RAISE EXCEPTION 'El pago % ya está Aprobado y no puede cambiar de estado.', OLD.idPago;
    END IF;
    
    RETURN NEW;

END;
$$ LANGUAGE plpgsql;

-- Trigger de la función anterior, se activa al actualizar el estado de un pago
CREATE TRIGGER trg_01_validar_transicion_estado_pagos
BEFORE UPDATE ON pagos
FOR EACH ROW
WHEN (OLD.estado IS DISTINCT FROM NEW.estado)
EXECUTE FUNCTION fn_verificar_transicion_estado_pagos();