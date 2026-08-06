------------------------------------------------------------------------------------------------
----------------- Archivo de todas queries o comandos que necesito recordar --------------------
------------------------------------------------------------------------------------------------


-- Listar todos los triggers
SELECT 
    event_object_schema AS schema_name,
    event_object_table AS table_name,
    trigger_name,
    string_agg(event_manipulation, ', ') AS event,
    action_timing AS activation
FROM 
    information_schema.triggers
GROUP BY 
    1, 2, 3, 5
ORDER BY 
    schema_name, table_name, trigger_name;

/* 
-------------------------Lista de todos los triggers
schema_name  | table_name |              trigger_name               | event  | activation 
--------------+------------+-----------------------------------------+--------+------------
 rgv_proyecto | gastos     | trg_01_validar_transicion_estado_gastos | UPDATE | BEFORE
 rgv_proyecto | gastos     | trg_02_liquidar_gastos                  | UPDATE | BEFORE
 rgv_proyecto | gastos     | trg_03_validar_cancelacion_gastos       | UPDATE | BEFORE
 rgv_proyecto | pagos      | trg_01_validar_transicion_estado_pagos  | UPDATE | BEFORE
 rgv_proyecto | pagos      | trg_02_actualizar_saldo_pagado          | UPDATE | BEFORE
 rgv_proyecto | pagos      | trg_aumentar_monto_pagado               | UPDATE | AFTER
 rgv_proyecto | pagos      | trg_forzar_estado_inicial_gastos        | INSERT | BEFORE
 rgv_proyecto | pagos      | trg_forzar_estado_inicial_pagos         | INSERT | BEFORE
 rgv_proyecto | pagos      | trg_validar_monto_pagos                 | INSERT | BEFORE
(9 rows)


-----------------------------List of functions
   Schema    |                 Name                  | Result data type | Argument data types | Type 
--------------+---------------------------------------+------------------+---------------------+------
 rgv_proyecto | fn_actualizar_saldo_pagado            | trigger          |                     | func
 rgv_proyecto | fn_aumentar_monto_pagado              | trigger          |                     | func
 rgv_proyecto | fn_forzar_estado_inicial_gastos       | trigger          |                     | func
 rgv_proyecto | fn_forzar_estado_inicial_pagos        | trigger          |                     | func
 rgv_proyecto | fn_liquidar_gastos                    | trigger          |                     | func
 rgv_proyecto | fn_validar_cancelacion_gastos         | trigger          |                     | func
 rgv_proyecto | fn_validar_monto_pagos                | trigger          |                     | func
 rgv_proyecto | fn_verificar_transicion_estado_gastos | trigger          |                     | func
 rgv_proyecto | fn_verificar_transicion_estado_pagos  | trigger          |                     | func
(9 rows)

*\