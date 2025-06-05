# Gestión de Biblioteca - DJANGO

El siguiente proyecto es una aplicación web creada con **Django** y **Django REST Framework** que permite gestionar libros y préstamos. Tiene protección de rutas para administradores y usuarios regulares, además de un diseño atractivo y dinámico.

---

## Tecnologías utilizadas

* Python 3.11
* Django 5.2.2
* Django REST Framework
* SQLite3 (por defecto)
* HTML + CSS
* Postman (para las pruebas realizadas en la API)

---

## Instalación y ejecución local

```bash
# 1) Clonar el repositorio

git clone https://github.com/victor-j10/biblioteca-django.git
cd biblioteca-django

# 2) Crear un entorno virtual
a python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate

# 3) Instalar las dependencias
pip install -r requirements.txt

# 4) Aplicar las migraciones
python manage.py migrate

# 5) Crear un superusuario (opcional)
python manage.py createsuperuser

# 6) Ejecutar el servidor
python manage.py runserver
```

---

## Roles y autenticación

* **Administrador:** Puede crear, editar y eliminar libros. También puede visualizar los libros en una tabla.
* **Usuario regular:** Puede ver los libros disponibles, tomar libros prestados, devolver los libros prestados y revisar su historial.

> El acceso a ciertas funciones está restringido según el rol del usuario. Para ello se utiliza un sistema de autenticación con `LoginRequiredMixin` y control por permisos en las vistas.

---

## Endpoints de la API REST

La API está construida con Django REST Framework y permite:

| Método | Endpoint            | Descripción             | Requiere Autenticación |
| ------ | ------------------- | ----------------------- | ---------------------- |
| GET    | /api/books/         | Lista todos los libros  | ❌                      |
| GET    | /api/books//        | Detalles de un libro    | ❌                      |
| POST   | /api/books/create/  | Crear un libro          | ✅ (Admin)              |
| PUT    | /api/books//edit/   | Editar un libro         | ✅ (Admin)              |
| DELETE | /api/books//delete/ | Eliminar un libro       | ✅ (Admin)              |
| POST   | /api/books/borrow/  | Tomar prestado un libro | ✅ (Usuario regular)    |
| POST   | /api/books/return/  | Devolver un libro       | ✅ (Usuario regular)    |

---

## 🧪 Pruebas con Postman

1. Obtener un token de acceso desde:

   ```text
   /api/api-token-auth/
   ```

   usa tus credenciales (`username` y `password`).

2. Usar el token en las peticiones con autorización tipo **Bearer Token**.

---

## Funcionalidades implementadas

* ✅ Autenticación de usuarios
* ✅ CRUD de libros (admin)
* ✅ Préstamo y devolución de libros (usuario)
* ✅ Panel web con vistas adaptadas según el rol
* ✅ API REST documentada y funcional
* ✅ Protección de vistas con `LoginRequiredMixin`

---

## Despliegue

Este proyecto se desplegará en **Heroku**. Archivos requeridos:

* `requirements.txt`
---

## Autor

Desarrollado por **Victor Hernandez** como parte de una prueba técnica.

---
