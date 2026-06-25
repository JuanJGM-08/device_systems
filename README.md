# device_systems API REST 

## Descripción de la aplicación

device_systems es una API REST desarrollada con FastAPI para la gestión de usuarios. La aplicación permite listar usuarios, consultar usuarios por ID, filtrar usuarios por rol o estado y registrar nuevos usuarios utilizando validaciones con Pydantic.

---

# Tecnologías utilizadas

- Python
- FastAPI
- Uvicorn
- Pydantic v2
- Swagger UI

---

# Estructura del proyecto EV08

```bash
device_systems/
│── app/
│   │── main.py
│   │
│   ├── schemas/
│   │   │── user_schema.py
│   │
│   ├── routes/
│   │   │── user_routes.py
│
│── requirements.txt
│── README.md
```

---

# Instalación de dependencias

## Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

---

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Archivo requirements.txt

```txt
fastapi
uvicorn
pydantic
email-validator
```

---

# Ejecución del servidor

```bash
python -m uvicorn app.main:app --reload
```

Abrir en el navegador:

```txt
http://127.0.0.1:8000/docs
```

---

# Tabla de endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/users` | Obtener todos los usuarios |
| GET | `/users/{user_id}` | Obtener usuario por ID |
| GET | `/users?role=admin` | Filtrar usuarios por rol |
| GET | `/users?is_active=true` | Filtrar usuarios activos |
| POST | `/users` | Registrar nuevo usuario |

---

# Ejemplos de peticiones GET y POST

## GET /users

```txt
GET http://127.0.0.1:8000/users
```

---

## GET /users/{user_id}

```txt
GET http://127.0.0.1:8000/users/1
```

---

## GET /users?role=admin

```txt
GET http://127.0.0.1:8000/users?role=admin
```

---

## GET /users?is_active=true

```txt
GET http://127.0.0.1:8000/users?is_active=true
```

---

## POST /users

```json
{
  "name": "Carlos Ruiz",
  "email": "carlos@example.com",
  "role": "user",
  "is_active": true
}
```

---

# Capturas de Swagger UI


<details>
<summary><b> Capturas GET/POST (Click para abrir)</b></summary>


## Captura 1 — Swagger UI funcionando

![SwaggerUI](images/01.png)
---

## Captura 2 — GET /users

![Get/Users](images/02.png)
---

## Captura 3 — POST /users

![POST/users](images/03.png)
---

## Captura 3 - POST /Validacion Correo Repetido

![POST/ Validacion](images/03-2.png)
---

## Captura 4 — GET /users/{user_id}

![GET/users/{user_id}](images/04.png)

</details>

# Capturas Put/Patch/Delete

<details>
<summary><b> Capturas PUT/PACH/DELETE (Click para abrir)</b></summary>

## Captura 1 — PUT/users/{user_id}

![PUT/users/{user_id}](images/PUT_1.png)


![PUT/users/{user_id}](images/PUT_2.png)

## Captura 1 - PUT Validacion Error


![PUT/users/{user_id}](images/PUT_ERROR.png)
---

## Captura 2 - PATCH/users/{users_id}

![PATCH/users/{user_id}](images/PATCH_1.png)
---

![PATCH/users/{user_id}](images/PATCH_2.png)
---

## Captura 2 - PATCH Validacion Error

![PATCH/users/{user_id}](images/PATCH_ERROR.png)
---

## Captura 3 - DELETE/users/{users_id}

![DELETE/users/{user_id}](images/PATCH_1.png)
---

## Captura 3 - DELETE Validacion Error

![DELETE/users/{user_id}](images/PATCH_ERROR.png)
---

</details>


# Reflexión sobre FastAPI

FastAPI facilita el desarrollo de APIs REST gracias a su rapidez, validaciones automáticas y documentación integrada con Swagger UI. Durante el desarrollo se aprendió a trabajar con rutas, parámetros, validaciones con Pydantic y respuestas HTTP estructuradas de manera organizada.

# Presentacion de Video
[Ver video EV07](https://www.loom.com/share/19a31984ae5540718d48f6c05c179278)

---

# Explicación de la estructura del proyecto

Para mejorar la organización del código y facilitar el mantenimiento de la aplicación, el proyecto fue dividido en módulos con responsabilidades específicas.

```bash
device_systems/
│
├── app/
│   │── main.py
│   │
│   ├── routes/
│   │   │── user_routes.py
│   │
│   ├── schemas/
│   │   │── user_schema.py
│   │
│   ├── services/
│   │   │── user_service.py
│   │
│   ├── dependencies/
│   │   │── user_dependencies.py
│   │
│   └── data/
│       │── users_db.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Organización de módulos

### routes

Contiene los endpoints de la API y la definición de las rutas disponibles para cada operación del recurso `users`.

### schemas

Incluye los modelos Pydantic utilizados para validar los datos recibidos y enviados por la API.

### services

Contiene la lógica de negocio de la aplicación, separando el procesamiento de datos de las rutas.

### dependencies

Almacena funciones reutilizables implementadas mediante Dependency Injection utilizando `Depends()`.

### data

Simula una base de datos en memoria donde se almacenan los usuarios registrados durante la ejecución de la aplicación.

### main.py

Actúa como punto de entrada principal de la API y contiene la configuración general de FastAPI.

---

# Implementación de Dependency Injection

La aplicación utiliza Dependency Injection mediante `Depends()` para reutilizar lógica común y evitar duplicación de código en los endpoints.

Se creó el archivo:

```bash
app/dependencies/user_dependencies.py
```

En este archivo se implementaron dependencias encargadas de validar la existencia de usuarios y controlar reglas de negocio antes de ejecutar las operaciones solicitadas.

Ejemplo de uso:

```python
user = Depends(get_user_or_404)
```

Gracias a este enfoque, las validaciones se centralizan en un único lugar, permitiendo que el código sea más limpio, reutilizable y fácil de mantener.

---

# Reflexión final sobre la evolución del proyecto

Durante el desarrollo de esta actividad se logró evolucionar la API inicial de usuarios hacia una solución más completa y profesional. Se implementó el CRUD completo mediante los métodos GET, POST, PUT, PATCH y DELETE, permitiendo realizar operaciones de consulta, creación, actualización y eliminación de usuarios.

Además, se incorporaron validaciones utilizando Pydantic, manejo de errores mediante HTTPException y códigos de estado HTTP adecuados para cada operación. También se mejoró la organización del proyecto mediante una estructura modular y la implementación de Dependency Injection para reutilizar lógica común.

Finalmente, la documentación automática generada por Swagger UI y ReDoc facilitó las pruebas de los endpoints y permitió contar con una API mejor documentada. Esta actividad permitió comprender la importancia de aplicar buenas prácticas en el desarrollo de APIs REST, mejorando la calidad, mantenibilidad y escalabilidad del proyecto.

---

# Video EV08

[Ver Video EV08](https://www.loom.com/share/684ce3de85c74e13abfcdaf837d38786)

# Explicacion de la estructura del proyecto EV09

el objetivo fue que el recurso "users" que se gestionaba en la memoria mediante listas o estructuras temporales, en esta nueva version transformaremos la API para que los usuarios se almacenen, consulten, actualicen y eliminen desde una base de datos usando modelos SQLAlchemy, schemas Pydantic, validaciones, constraints y operaciones CRUD


```bash

├── app/
│   main.py
│   
├───database
│   │   connection.py
│   │   users_db.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           connection.cpython-314.pyc
│           users_db.cpython-314.pyc
│           __init__.cpython-314.pyc
│           
├───dependencies
│   │   database_dependency.py
│   │   user_dependencies.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           database_dependency.cpython-314.pyc
│           user_dependencies.cpython-314.pyc
│           __init__.cpython-314.pyc
│           
├───models
│   │   user_model.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           user_model.cpython-314.pyc
│           __init__.cpython-314.pyc
│           
├───routes
│   │   user_routes.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           user_routes.cpython-314.pyc
│           __init__.cpython-314.pyc
│           
├───schemas
│   │   user_schema.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           user_schema.cpython-314.pyc
│           __init__.cpython-314.pyc
│           
├───services
│   │   user_service.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           user_service.cpython-314.pyc
│           __init__.cpython-314.pyc
│           
└───__pycache__
        main.cpython-314.pyc

```

# Evidencias

<details>
<summary><b> Base Datos + Swagger(Click para abrir)</b></summary>


## Captura 1 — Estructura de archivos

![Estructura de archivos](images/estructura.png)
---

## Captura 2 — Base de Datos

![Base de Datos](images/BaseDatos.png)
---

## Captura 3 — Get/users/

![Get/users/](images/Get.png)
---

## Captura 4 — Post/users/ 

![Post/users/](images/Post.png)
---

## Captura 5 — Get/users/{users_id}

![Get/users/{users_id}](images/Get_id.png)
---

## Captura  6 — Patch/users/{users_id}

![Patch/users/{users_id}](images/Patch.png)
---

## Captura  7 — Delete/users/{users_id}

![Post/users/{users_id}](images/Post_id.png)
---

## Captura  8 — Error correo duplicado (400)

![Error correo duplicado](images/ErrorCodigo.png)
---

## Captura  9 — Datos invalidos (422)

![Datos invalidos](images/Error_2.png)
---

</details>

##  Diferencia entre SQLAlchemy Model y Pydantic Schema

| Aspecto | SQLAlchemy (Model) | Pydantic (Schema) |
|---------|--------------------|--------------------|
| **Qué hace** | Define la estructura de la tabla en BD | Valida los datos que entran/salen por la API |
| **Dónde vive** | En la base de datos (disco duro) | En la memoria RAM (solo durante la petición) |
| **Ejemplo real** | email = Column(String, unique=True) | email: EmailStr |
| **Validación** | Solo tipos básicos (String, Integer) | Reglas complejas (email, longitud, valores permitidos) |
| **Persistencia** |  Los datos se guardan permanentemente |  Los datos se pierden si no se guardan |

### En tu código:

- **`user_model.py`** → SQLAlchemy: le dice a la BD cómo crear la tabla `users`
- **`user_schema.py`** → Pydantic: valida que el email sea válido y el nombre tenga al menos 3 caracteres


---

##  Reflexión: Importancia de la persistencia

### ¿Qué pasaría sin persistencia?

| Situación | Sin persistencia | Con persistencia (tu API) |
|-----------|------------------|---------------------------|
| Reinicias el servidor |  Se pierden todos los usuarios |  Los usuarios siguen ahí |
| Dos clientes consultan |  Cada uno ve datos diferentes |  Todos ven los mismos datos |
| Quieres saber cuándo se creó un usuario |  No es posible |  El campo `created_at` lo guarda |

# Video EV09

[Ver Video EV09](https://www.loom.com/share/a81b89ea654a412fbd9b94c84b087215)

# Explicación de la estructura del proyecto EV10

##  Descripción del Proyecto

API REST para gestión de usuarios, dispositivos y préstamos, desarrollada con FastAPI. Esta versión implementa migraciones con Alembic, asociaciones entre modelos (User, Device, Loan) y consultas con joins para obtener información relacionada.

##  Tecnologías Utilizadas

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- SQLite
- Uvicorn

##  Estructura del Proyecto

```bash

device_systems/
│
├── app/
│   │   main.py
│   │
│   ├───database/
│   │   │   connection.py
│   │   │   users_db.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__/
│   │           connection.cpython-314.pyc
│   │           users_db.cpython-314.pyc
│   │           __init__.cpython-314.pyc
│   │
│   ├───dependencies/
│   │   │   database_dependency.py
│   │   │   user_dependencies.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__/
│   │           database_dependency.cpython-314.pyc
│   │           user_dependencies.cpython-314.pyc
│   │           __init__.cpython-314.pyc
│   │
│   ├───models/
│   │   │   user_model.py
│   │   │   device_model.py
│   │   │   loan_model.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__/
│   │           user_model.cpython-314.pyc
│   │           device_model.cpython-314.pyc
│   │           loan_model.cpython-314.pyc
│   │           __init__.cpython-314.pyc
│   │
│   ├───routes/
│   │   │   user_routes.py
│   │   │   device_routes.py
│   │   │   loan_routes.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__/
│   │           user_routes.cpython-314.pyc
│   │           device_routes.cpython-314.pyc
│   │           loan_routes.cpython-314.pyc
│   │           __init__.cpython-314.pyc
│   │
│   ├───schemas/
│   │   │   user_schema.py
│   │   │   device_schema.py
│   │   │   loan_schema.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__/
│   │           user_schema.cpython-314.pyc
│   │           device_schema.cpython-314.pyc
│   │           loan_schema.cpython-314.pyc
│   │           __init__.cpython-314.pyc
│   │
│   ├───services/
│   │   │   user_service.py
│   │   │   device_service.py
│   │   │   loan_service.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__/
│   │           user_service.cpython-314.pyc
│   │           device_service.cpython-314.pyc
│   │           loan_service.cpython-314.pyc
│   │           __init__.cpython-314.pyc
│   │
│   └───__pycache__/
│           main.cpython-314.pyc
│
├───alembic/
│   │
│   └───versions/
│           └─── 4df4a28f13b7_initial_migration_with_users_devices_.py
│   │
│   │   __init__.py
│   │   env.py
│   │   script.py.mako
│   │
│   └───__pycache__/
│
├───images/
│
├───venv/
│
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── device_systems.db
├── requirements.txt
└── README.md
```

##  Instalación

# Crear entorno virtual
python -m venv venv

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
alembic upgrade head

# Ejecutar servidor
uvicorn app.main:app --reload

##  Endpoints

### Users

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /users | Listar usuarios |
| GET | /users/{id} | Obtener usuario por ID |
| POST | /users | Crear usuario |
| PUT | /users/{id} | Actualizar usuario completo |
| PATCH | /users/{id} | Actualizar usuario parcialmente |
| DELETE | /users/{id} | Eliminar usuario |

### Devices

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /devices | Listar dispositivos |
| GET | /devices/{id} | Obtener dispositivo por ID |
| POST | /devices | Crear dispositivo |
| PUT | /devices/{id} | Actualizar dispositivo completo |
| PATCH | /devices/{id} | Actualizar dispositivo parcialmente |
| DELETE | /devices/{id} | Eliminar dispositivo |

### Loans

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | /loans | Listar préstamos |
| GET | /loans/details | Listar préstamos con JOIN |
| GET | /loans/{id} | Obtener préstamo por ID |
| GET | /loans/user/{id} | Préstamos de un usuario |
| GET | /loans/device/{id} | Préstamos de un dispositivo |
| POST | /loans | Crear préstamo |
| PATCH | /loans/{id}/return | Devolver dispositivo |
| PATCH | /loans/{id} | Actualizar préstamo |
| DELETE | /loans/{id} | Eliminar préstamo |

##  Consultas con JOIN - /loans/details

Ejemplo de respuesta:

{
  "id": 1,
  "status": "active",
  "loan_date": "2024-06-18T10:00:00",
  "user": {
    "id": 1,
    "name": "Juan Perez",
    "email": "juan@test.com"
  },

  "device": {
    "id": 1,
    "name": "Laptop HP",
    "serial_number": "HP-001",
    "device_type": "laptop"
  }
}

##  Migraciones con Alembic

# Generar migración
alembic revision --autogenerate -m "mensaje"

# Aplicar migración
alembic upgrade head

# Ver historial
alembic history

# Ver estado actual
alembic current

##  Evidencias

<details>
<summary><b> Evolucion FASTAPI (Click para abrir)</b></summary>


## Captura 1 — Estructura de archivos

![Ejecucion de alembic](images/Alembicinit.png)
---

## Captura 2 — creación de migración

![creación de migración](images/CrearMigracion.png)
---

## Captura 3 — Aplicar Migracion

![Aplicar migración](images/AplicarMigracion.png)
---

## Captura 4 — Tablas

![Tablas](images/Tablas.png)
---

## Captura 5 — Swagger 

![Swagger](images/Swagger.png)
---

## Captura 6 — creación de usuario, dispositivo y préstamo 

### User

![creación de usuario, dispositivo y préstamo ](images/POSTUser.png)

### Device

![Device](images/Device.png)

### Loans

![Loans](images/Loans.png)
---

## Captura 7 - consultas con joins

![Consulta con Joins](images/Joins.png)
---

## Captura 8 - Filtros
![Filtro Loans](images/LoanFiltro.png)
---

### Device Filtro

![Device Filtro](images/GetDevice.png)
---

### Captura 9 - Devolucion

![Devolucion](images/Devolucion.png)
---


</details>

## Ver Video EV10
[Ver Video EV10](https://www.loom.com/share/a2e6356dee184f7cb353f939fbffd3b8)

# Reflexión Final

### ¿Qué importancia tienen las migraciones con Alembic?

Las migraciones con Alembic son fundamentales porque:

1. **Control de versiones de la base de datos:** Permiten mantener un historial de todos los cambios estructurales, facilitando el trabajo en equipo y la trazabilidad.
2. **Reproducibilidad:** Cualquier desarrollador puede aplicar exactamente los mismos cambios en su entorno local.
3. **Rollback controlado:** Si algo sale mal, se puede revertir a una versión anterior sin perder datos críticos.
4. **Automatización:** Con `--autogenerate`, Alembic detecta automáticamente los cambios en los modelos y genera el código de migración.

### ¿Por qué son importantes las relaciones entre modelos?

1. **Integridad referencial:** Las relaciones con ForeignKey garantizan que los datos estén siempre conectados correctamente (ej: un préstamo siempre pertenece a un usuario y dispositivo existentes).
2. **Eficiencia:** Permiten consultar datos relacionados sin múltiples viajes a la base de datos.
3. **Mantenibilidad:** El código es más limpio y fácil de entender cuando las relaciones están definidas a nivel de modelo.

### ¿Qué ventajas ofrecen las consultas con JOIN?

1. **Reducción de consultas:** En lugar de hacer 3 consultas separadas (usuario, dispositivo, préstamo), se hace una sola con JOIN.
2. **Rendimiento:** Menos viajes a la base de datos = respuesta más rápida.
3. **Datos completos:** Se obtiene toda la información relacionada en un solo objeto JSON.
4. **Filtros avanzados:** Permite filtrar por campos de tablas relacionadas (ej: filtrar préstamos por email del usuario o por tipo de dispositivo).

### Conclusión

La combinación de migraciones, relaciones y JOINs convierte una API básica en una solución profesional, mantenible y escalable. Alembic facilita el control de cambios, las relaciones garantizan la integridad de los datos, y los JOINs optimizan el rendimiento de las consultas.

### ¿Qué se logró con esta actividad?

1. Migraciones con Alembic: Control de versiones de la base de datos, permitiendo cambios estructurados y reversibles.

2. Asociaciones entre modelos: Relaciones One-to-Many entre User-Loan y Device-Loan, garantizando integridad referencial.

3. Consultas con JOIN: Obtención de información relacionada en una sola consulta, mejorando el rendimiento.

4. Arquitectura por capas: Separación clara entre modelos, schemas, servicios y rutas.

5. API REST completa: CRUD completo para Users, Devices y Loans.


# device_systems API REST — EV11

API REST segura para gestión de usuarios, dispositivos y préstamos, desarrollada con FastAPI.

---

## Tecnologías utilizadas

- Python 3.11+
- FastAPI 0.136
- SQLAlchemy 2.0 + Alembic
- Pydantic v2
- passlib[bcrypt] — hash de contraseñas
- python-jose[cryptography] — tokens JWT
- slowapi — rate limiting
- python-dotenv — variables de entorno
- Uvicorn

---

## Estructura del proyecto

```bash
device_systems/
│── app/
│   │── main.py
│   │
│   ├── auth/
│   │   ├── auth_routes.py
│   │   ├── auth_service.py
│   │   └── security.py
│   │
│   ├── database/
│   │   └── connection.py
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── device_model.py
│   │   └── loan_model.py
│   │
│   ├── schemas/
│   │   ├── user_schema.py
│   │   ├── device_schema.py
│   │   ├── loan_schema.py
│   │   └── auth_schema.py
│   │
│   ├── routes/
│   │   ├── user_routes.py
│   │   ├── device_routes.py
│   │   └── loan_routes.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   ├── device_service.py
│   │   └── loan_service.py
│   │
│   ├── dependencies/
│   │   ├── database_dependency.py
│   │   └── auth_dependency.py
│   │
│   └── middlewares/
│       └── request_middleware.py
│
├── alembic/
│   └── versions/
│
├── .env
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## Endpoints

### Autenticación (`/auth`)

| Método | Ruta | Descripción | Límite |
|--------|------|-------------|--------|
| POST | `/auth/register` | Registrar usuario | 3/min |
| POST | `/auth/login` | Iniciar sesión — retorna JWT | 5/min |
| GET | `/auth/me` | Datos del usuario autenticado | — |

### Usuarios (`/users`)

| Método | Ruta | Protección | Límite |
|--------|------|------------|--------|
| GET | `/users/` | Autenticado | 30/min |
| GET | `/users/{id}` | Autenticado | — |
| POST | `/users/` | Público | — |
| PUT | `/users/{id}` | Admin | — |
| PATCH | `/users/{id}` | Admin | — |
| DELETE | `/users/{id}` | Admin | — |

### Dispositivos (`/devices`)

| Método | Ruta | Protección |
|--------|------|------------|
| GET | `/devices/` | Público |
| GET | `/devices/{id}` | Público |
| POST | `/devices/` | Admin o Support |
| PUT | `/devices/{id}` | Admin o Support |
| PATCH | `/devices/{id}` | Admin o Support |
| DELETE | `/devices/{id}` | Solo Admin |

### Préstamos (`/loans`)

| Método | Ruta | Protección | Límite |
|--------|------|------------|--------|
| GET | `/loans/` | Público | — |
| GET | `/loans/details` | Admin o Support | — |
| POST | `/loans/` | Autenticado | 10/min |
| PATCH | `/loans/{id}/return` | Admin o Support | — |

---

## Roles

| Rol | Permisos |
|-----|----------|
| `admin` | Acceso total a todos los endpoints |
| `support` | Crear y editar dispositivos, gestionar devoluciones |
| `user` | Consultar recursos y crear préstamos |

---

## Seguridad

### Hash de contraseñas

Las contraseñas **nunca se almacenan en texto plano**. Se usa `bcrypt` a través de `passlib` para generar un hash seguro antes de persistir en base de datos. La contraseña original nunca puede recuperarse.

Requisitos mínimos de contraseña:
- Mínimo 8 caracteres
- Al menos una mayúscula
- Al menos una minúscula
- Al menos un número
- Sin espacios en blanco

### Tokens JWT

- Firmados con algoritmo HS256
- Expiración configurable vía variable de entorno (por defecto 30 minutos)
- Se envían en cada petición mediante el header: `Authorization: Bearer <token>`
- El payload contiene el email y el rol del usuario

### Rate Limiting

Se usa `slowapi` para limitar el número de peticiones por IP. Al superar el límite configurado la API responde automáticamente con `429 Too Many Requests`.

---

## Middleware personalizado

Cada respuesta incluye automáticamente las siguientes cabeceras:
X-App-Name: device_systems

X-Process-Time: 0.0042

X-Request-ID: 8f42e9c1-...

- `X-App-Name` identifica la aplicación
- `X-Process-Time` muestra el tiempo de procesamiento en segundos
- `X-Request-ID` permite rastrear cada petición individualmente

---

## Evidencias (Capturas)


<details>
<summary><b> Evolucion FASTAPI (Click para abrir)</b></summary>

## Captura 1 — Estructura Proyecto

![Estructura](images/EstructuraEV11.png)

![Estructura](images/Estructura2EV11.png)

---

## Captura 2 - Migracion

![Migracion](images/MigracionEV11.png)

---

## Captura 3 - Register

![Register](images/AuthRegister.png)

---


## Captura 4 - Login + Token

![Login + token](images/AuthLogin.png)

---

## Captura 5 - AuthMe

![AuthMe](images/AuthMe.png)

---

## Captura 6 - Acceso No Token

![Acceso No Token](images/NoToken.png)

---

## Captura 7 - Rol No permitido

![Rol no permitido](images/RolNoPermitido.png)

---

## Captura 8 - Swagger/OpenAPI con OAuth2

![Swagger/OpenAPI con OAuth2](images/SwaggerAuth.png)

---

## Captura 9 - cabeceras del middleware

![cabeceras del middleware](images/Cabezeras.png)

---

## Captura 10 - Rate litiming

![Rate Limiting](images/ManyRequest.png)

---

</details>


## Configuración CORS

### ¿Por qué NO usar `"*"` en `allow_origins` cuando hay credenciales?

Cuando se configura `allow_credentials=True` en el middleware CORS, el estándar de seguridad web **prohíbe explícitamente usar `"*"` como valor de `allow_origins`**. El navegador rechazará la respuesta directamente.

La razón de fondo es más importante: si se permitiera cualquier origen con credenciales activas, un sitio web malicioso podría hacer peticiones autenticadas a tu API usando el token o las cookies del usuario que tenga sesión abierta, abriendo la puerta a ataques **CSRF (Cross-Site Request Forgery)**.

```python
allow_origins=[
    "https://mi-frontend.com",
    "https://admin.mi-empresa.com",
]

#  Prohibido cuando allow_credentials=True
allow_origins=["*"]
```

En producción siempre se deben listar exactamente los dominios autorizados, garantizando que solo el frontend legítimo pueda consumir la API con credenciales y protegiendo a los usuarios autenticados de ataques externos.

---

## Autenticación en Swagger

1. Abrir http://localhost:8000/docs
2. Hacer clic en **Authorize 🔒**
3. Ingresar el email en el campo **username**
4. Ingresar la contraseña en el campo **password**
5. Hacer clic en **Authorize**
6. Todos los endpoints protegidos quedan autenticados automáticamente

## Ver video
[Ver video EV11](https://youtu.be/2HrJUreJnxQ?si=zo412sTWtA6Q8grC)