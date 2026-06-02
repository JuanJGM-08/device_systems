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

# Estructura del proyecto

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
---

# Reflexión sobre FastAPI

FastAPI facilita el desarrollo de APIs REST gracias a su rapidez, validaciones automáticas y documentación integrada con Swagger UI. Durante el desarrollo se aprendió a trabajar con rutas, parámetros, validaciones con Pydantic y respuestas HTTP estructuradas de manera organizada.

# Presentacion de Video
[Ver video](https://www.loom.com/share/19a31984ae5540718d48f6c05c179278)