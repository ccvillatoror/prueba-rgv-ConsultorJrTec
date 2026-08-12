# Plataforma de manejo de Gastos y Pagos de la Empresa SA de CV

Este repositorio para subir el código y el material del desarrollo de la Prueba de Programación para el puesto de Consultor Jr de Tecnología en RGV Soluciones.

## Archivo Main
El archivo principal del proyecto es `src/application.py`.

## Proceso de diseño
### ¿Cómo acceder a la aplicación?
Para consultar la aplicación en línea, use el siguiente link: [prueba-rgv-consultorjrtec.onrender.com/login](prueba-rgv-consultorjrtec.onrender.com/login) (Consultado el 11 de agosto).

Puede usar las siguientes **credenciales:**
- **Usuario:**
- **Contraseña:**

Después de iniciar sesión, el usuario tiene dos posibles caminos: Pagos y Gastos.

### Diagramas de los Gastos
Un Gasto puede estar "En proceso", "Aprobado", "Cancelado" y "Liquidado". El siguiente diagrama muestra cómo se puede pasar entre los estados, de "En proceso" se puede cancelar o aprobar y de "Aprobado" se puede pasar a "Liquidado" sólo si el monto gastado se cubre por completo con pagos. Una vez cancelado un gasto, no se puede revertir.

![Diagrama del flujo entre estados](/proceso/img/Flujos-Gastos-estados.jpg)

El flujo del programa se ilustra en el siguiente diagrama.

![Diagrama del proceso de Gastos](/proceso/img/Flujos-Gastos-todo.jpg)

### Diagramas de los Pagos
Un Gasto puede estar "En proceso", "Aprobado" y "Cancelado". El siguiente diagrama muestra cómo se puede pasar entre los estados, de "En proceso" se puede cancelar o aprobar y pero de "Aprobado" no se puede cancelar, ni revertir el estado de "Cancelado".

![Diagrama del flujo entre estados](/proceso/img/Flujos-Pagos-estados.jpg)

El flujo del programa con respecto a los pagosx se ilustra en el siguiente diagrama.

![Diagrama del proceso de Gastos](/proceso/img/Flujos-Pagos-todo.jpg)

### Video del funcionamiento del proyecto
En este video se puede ver todas las funciones del programa en funcionamiento.

[Vídeo de página web](https://drive.google.com/)

En este video se ve un demo de las consultas que se pueden hacer a la API.

[Vídeo de demo API](https://drive.google.com/)


### Diagrama de la base de datos
La base de datos cuenta con cuatro tablas: Cuentas, Gastos, Pagos y Usuarios. Contiene lo mínimo para resolver este reto.


![Diagrama de la base de datos](/proceso/img/DiagramaBD.jpg)

## Documentación de la API

### Endpoints disponibles
### 1. Iniciar Sesión (Login)
Primer paso para verificar las credenciales y obtener el token de acceso.

- **URL:** `/api/login`
- **Método:** `POST`
- **Cabeceras obligatorias:** `Content-Type: application/json`
- **Cuerpo de la petición (JSON):**
```
{
  "user": "SU_USUARIO",
  "password": "SU_CONTRASEÑA"
}
```

- **Respuesta Exitosa (Código 200 OK):**

```
{
  "mensaje": "Ha ingresado correctamente",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

```

- **Respuesta de Error (Código 401 Unauthorized):**

```
{
  "error": "Usuario o contraseña incorrectos"
}

```

### 2. Índice
Devuelve una lista de las funciones disponibles de la api.
- **URL:** `/api/`
- **Método:** `GET`
- **Requiere autenticación:** Sí (JWT)
- **Ejemplos con cURL:**
```
curl https://prueba-rgv-consultorjrtec.onrender.com/api/ \
     -H "Authorization: Bearer TU_TOKEN_JWT"
```
- **Respuesta Exitosa (Código 200 OK):**
```
{
  "autenticacion":"HTTP Basic Auth (usuario y contraseña de la aplicación)",
  "filtros":{
      "gastos":"?estado=En proceso|Aprobado|Liquidado|Cancelado",
      "pagos":"?estado=En proceso|Aprobado|Cancelado"
      },
  "recursos":{
      "cuenta_por_id":"/api/cuentas/<id>",
      "cuentas":"/api/cuentas",
      "gasto_por_id":"/api/gastos/<id>",
      "gastos":"/api/gastos",
      "pago_por_id":"/api/pagos/<id>",
      "pagos":"/api/pagos"
      }
}
```

### 3. Gastos
#### Obtener lista de gastos

Devuelve una lista de todos los gastos registrados en la base de datos. Permite filtrar los resultados por estado.

- **URL:** `/api/gastos`
- **Método:** `GET`
- **Requiere autenticación:** Sí (JWT)
- **Parámetros de búsqueda:** 
    - `estado` (opcional): Los valores permitidos son `En proceso`, `Aprobado`, `Liquidado`, `Cancelado`
- **Ejemplos con cURL:**
```
curl https://prueba-rgv-consultorjrtec.onrender.com/api/gastos?estado=En%20proceso \
     -H "Authorization: Bearer TU_TOKEN_JWT"

curl https://prueba-rgv-consultorjrtec.onrender.com/api/gastos?estado=Aprobado \
     -H "Authorization: Bearer TU_TOKEN_JWT"

```
Donde `TU_TOKEN_JWT` es el token dado en la respuesta del `login`.


- **Respuesta Exitosa (Código 200 OK):**

```
[
  {"concepto":"Compra de insumos",
  "estado":"Aprobado",
  "fecha":"Mon, 27 Jul 2026 00:00:00 GMT",
  "id":1,
  "monto_gastado":3000.0,
  "monto_pagado":2500.0,
  "saldo_pendiente":500.0},
  {"concepto":"Compra plásticos Pablín",
  "estado":"Cancelado",
  "fecha":"Tue, 28 Jul 2026 00:00:00 GMT",
  "id":2,
  "monto_gastado":6000.0,
  "monto_pagado":0.0,
  "saldo_pendiente":6000.0}
]

```
#### Obtener Gasto por ID

Devuelve la información detallada de un único gasto.

- **URL:** `/api/gastos/<id>`
- **Método:** `GET`
- **Requiere autenticación:** Sí (JWT)`
- **Ejemplo con cURL:**
```
curl https://prueba-rgv-consultorjrtec.onrender.com/api/gastos/1 \
     -H "Authorization: Bearer TU_TOKEN_JWT"

```
Donde `TU_TOKEN_JWT` es el token dado en la respuesta del `login`.

- **Respuesta Exitosa (Código 200 OK):**

```
{ 
  "concepto":"Compra de insumos",
  "estado":"Aprobado",
  "fecha":"Mon, 27 Jul 2026 00:00:00 GMT",
  "id":1,
  "monto_gastado":3000.0,
  "monto_pagado":2500.0,
  "saldo_pendiente":500.0

  } 
```
- **Respuesta de Error (Código 404 Not Found):**

```
{
  "error": "El gasto con el ID solicitado no existe."
}
```

### 4. Pagos

Devuelve una lista de todos los pagos registrados en la base de datos. Permite filtrar los resultados por estado y por el id del gasto relacionado.

- **URL:** `/api/pagos`
- **Método:** `GET`
- **Requiere autenticación:** Sí (JWT)
- **Parámetros de búsqueda:** 
    - `estado` (opcional): Los valores permitidos son `En proceso`, `Aprobado`, `Cancelado`
    - `id_gasto` (opcional): Un entero.
- **Ejemplos con cURL:**
```
curl https://prueba-rgv-consultorjrtec.onrender.com/api/pagos?estado=Cancelado \
     -H "Authorization: Bearer TU_TOKEN_JWT"

curl https://prueba-rgv-consultorjrtec.onrender.com/api/pagos?id_gasto=4 \
     -H "Authorization: Bearer TU_TOKEN_JWT"

```
Donde `TU_TOKEN_JWT` es el token dado en la respuesta del `login`.


- **Respuesta Exitosa (Código 200 OK):**

```
[
  {"cuenta":1,
  "estado":"Cancelado",
  "fecha":"Thu, 30 Jul 2026 00:00:00 GMT",
  "id":4,
  "id_gasto":4,
  "monto_pagado":1000.0},
  
  {"cuenta":1,
  "estado":"Aprobado",
  "fecha":"Sat, 08 Aug 2026 00:00:00 GMT",
  "id":36,
  "id_gasto":4,
  "monto_pagado":100.0},
  
  {"cuenta":1,
  "estado":"En proceso","fecha":"Mon, 10 Aug 2026 00:00:00 GMT",
  "id":54,
  "id_gasto":4,
  "monto_pagado":5000.0}

]

```
#### Obtener Pago por ID

Devuelve la información detallada de un único pago.

- **URL:** `/api/pagos/<id>`
- **Método:** `GET`
- **Requiere autenticación:** Sí (JWT)`
- **Ejemplo con cURL:**
```
curl https://prueba-rgv-consultorjrtec.onrender.com/api/pagos/1 \
     -H "Authorization: Bearer TU_TOKEN_JWT"

```
Donde `TU_TOKEN_JWT` es el token dado en la respuesta del `login`.

- **Respuesta Exitosa (Código 200 OK):**

```
{ 
  "cuenta":1,
  "estado":"Aprobado",
  "fecha":"Sat, 01 Aug 2026 00:00:00 GMT",
  "id":1,
  "id_gasto":1,
  "monto_pagado":2000.0

  } 
```
- **Respuesta de Error (Código 404 Not Found):**

```
{
  "error": "El pago con el ID solicitado no existe."
}
```

### 5. Cuentas

Devuelve una lista de todas las cuentas registradas en la base de datos. Permite filtrar los resultados por el id de la cuenta.

- **URL:** `/api/cuentas`
- **Método:** `GET`
- **Requiere autenticación:** Sí (JWT)
- **Ejemplo con cURL:**
```
curl https://prueba-rgv-consultorjrtec.onrender.com/api/cuentas \
     -H "Authorization: Bearer TU_TOKEN_JWT"
```
Donde `TU_TOKEN_JWT` es el token dado en la respuesta del `login`.

- **Respuesta Exitosa (Código 200 OK):**

```
[
 {"id":1,
  "saldo":943740.0 },

  {"id":2,
  "saldo":5000.0}
]

```
#### Obtener Cuenta por ID

Devuelve la información detallada de una única cuenta.

- **URL:** `/api/cuentas/<id>`
- **Método:** `GET`
- **Requiere autenticación:** Sí (JWT)`
- **Ejemplo con cURL:**
```
curl https://prueba-rgv-consultorjrtec.onrender.com/api/cuentas/2 \
     -H "Authorization: Bearer TU_TOKEN_JWT"

```
Donde `TU_TOKEN_JWT` es el token dado en la respuesta del `login`.

- **Respuesta Exitosa (Código 200 OK):**

```
{ 
  "id":2,
  "saldo":5000.0
  } 
```
- **Respuesta de Error (Código 404 Not Found):**

```
{
  "error": "La cuenta con el ID solicitado no existe."
}
```


### 6. Códigos de Estados Comunes
La API utiliza los códigos de estado HTTP estándar para indicar el éxito o fracaso de una petición:

| Código | Significado | Descripción |
|---|---|---|
| `200 OK` | Exito | La petición fue correcta y se devuelven los datos. |
| `400 Bad Request` | Error del Cliente | Faltan datos obligatorios o el JSON está mal escrito. |
| `401 Unauthorized` | No Autorizado | No enviaste el token JWT, expiró o está mal escrito. |
| `404 Not Found` | No Encontrado | El recurso o la URL que buscas no existe. |
| `500 Internal Error` | Error del Servidor | Hubo un problema interno en el código de la aplicación. |

## Futuras mejoras
En la página de ver los gastos agregar una columna para el monto que falta por pagar, restando el monto gastado menos el monto pagado.

En la página de ver los pagos agregar el concepto del gasto además de su id.

El objetivo era hostear la aplicación usando AWS Elastic Beanstalk, pero por un error del .zip no pude. Lo seguiré intentando.

Se le puede agregar una página para ver las cuentas y los pagos realizados con esa cuenta.

La página no tiene para agregar usuarios, se puede implementar. Dependiendo de los objetivos, se puede hasta tener un sistema de permisos asociados a un usuario.