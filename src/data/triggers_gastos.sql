------------------------------------------------------------------------------------------------
-------- Archivo de todas las funciones y triggers relacionadas con la tabla de gastos --------
------------------------------------------------------------------------------------------------

-- Un gasto no se puede cambiar el estado ya cancelado, ni de Aprobado a Cancelado.
CREATE OR REPLACE FUNCTION fn_verificar_transicion_estado_gastos()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.estado = 'Cancelado' THEN
        RAISE EXCEPTION 'El gasto % está cancelado y no puede cambiar de estado. Cree uno nuevo.', OLD.idGasto;
    END IF;

    IF OLD.estado = 'Liquidado' THEN
        RAISE EXCEPTION 'El gasto % está liquidado y no puede cambiar de estado. Cree uno nuevo.', OLD.idGasto;
    END IF;

    IF OLD.estado = 'Aprobado' AND NEW.estado = 'Cancelado' THEN
        RAISE EXCEPTION 'El gasto % ya está Aprobado y no puede ser cancelado.', OLD.idGasto;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger de la función anterior, se activa al actualizar el estado de un gasto
CREATE TRIGGER trg_01_validar_transicion_estado_gastos
BEFORE UPDATE ON gastos
FOR EACH ROW
WHEN (OLD.estado IS DISTINCT FROM NEW.estado)
EXECUTE FUNCTION fn_verificar_transicion_estado_gastos();

-- Función para que todos los gastos inicialmente agregados sean siempre en estado 'En proceso'
CREATE OR REPLACE FUNCTION fn_forzar_estado_inicial_gastos()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.estado IS DISTINCT FROM 'En proceso' THEN
        RAISE WARNING 'El gasto será creado con estado ''En proceso'' (recibido: %).', NEW.estado;
    END IF;

    NEW.estado = 'En proceso';

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger de la función anterior, se activa al agregar un nuevo pago.
CREATE TRIGGER trg_forzar_estado_inicial_gastos
BEFORE INSERT ON pagos
FOR EACH ROW
EXECUTE FUNCTION fn_forzar_estado_inicial_gastos();

-- Al actualizar el valor del montoPagado, si es igual al montoGastado, cambiar el estado a 'Liquidado'
CREATE OR REPLACE FUNCTION fn_liquidar_gastos()
RETURNS TRIGGER AS $$
BEGIN

    IF NEW.estado IS DISTINCT FROM 'Cancelado' AND NEW.montoPagado >= NEW.montoGastado THEN
        NEW.estado = 'Liquidado';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger de la función anterior, se activa al actualizar gastos.
CREATE TRIGGER trg_02_liquidar_gastos
BEFORE UPDATE ON gastos
FOR EACH ROW
WHEN (OLD.montoPagado IS DISTINCT FROM NEW.montoPagado)
EXECUTE FUNCTION fn_liquidar_gastos();

-- Antes de cancelar un pago, checar si no hay pagos asociados aprobados. Si hay, no se pueden cancelar. 
-- Si no hay, cancelar sólo los pagos En proceso asociados.
CREATE OR REPLACE FUNCTION fn_validar_cancelacion_gastos()
RETURNS TRIGGER AS $$
DECLARE
    pagosAprobados INT;
BEGIN
    SELECT count(idPago)
    INTO pagosAprobados
    FROM pagos
    WHERE idGasto = NEW.idGasto AND estado = 'Aprobado';

    RAISE WARNING 'Todos los pagos En proceso serán cancelados.';

    UPDATE pagos
    SET estado = 'Cancelado'
    WHERE pagos.idGasto = NEW.idGasto AND pagos.estado = 'En proceso';

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger de la función anterior, se activa al actualizar el estado de un gasto
CREATE TRIGGER trg_03_validar_cancelacion_gastos
BEFORE UPDATE ON gastos
FOR EACH ROW
WHEN (OLD.estado IS DISTINCT FROM NEW.estado AND NEW.estado = 'Cancelado')
EXECUTE FUNCTION fn_validar_cancelacion_gastos();