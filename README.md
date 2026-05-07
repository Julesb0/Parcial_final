# Sistema de Seguimiento de Proyectos Académicos

## Usuarios de prueba para ingresar al sistema

Estas son las cuentas disponibles para que el profesor pueda probar el sistema.

| Rol | Usuario | Contraseña |
|---|---|---|
| Estudiante | julio | Estudiante123 |
| Estudiante | william | Estudiante123 |
| Estudiante | diego | Estudiante123 |
| Estudiante | mike | Estudiante123 |
| Docente | docente | Docente123 |
| Administrador | admin | Admin12345 |

---

## Evidencia del flujo de trabajo GitFlow

La siguiente imagen muestra el historial de ramas, commits y merges realizados durante el desarrollo del proyecto.

<img width="1538" height="265" alt="Evidencia GitFlow" src="https://github.com/user-attachments/assets/85e6f3f5-d85d-4e8e-bfee-0d7e367e0e24" />

---

## Acceso al sistema

Después de ejecutar el servidor con Django, el profesor puede ingresar desde el navegador usando la dirección local que aparece en la terminal.

Para entrar al panel de administración, se debe agregar `/admin/` al final de la dirección local del servidor.

---

## Descripción del proyecto

Este proyecto corresponde al **Sistema de Seguimiento de Proyectos Académicos**, desarrollado con Django.

La aplicación permite registrar proyectos académicos, gestionarlos mediante distintos estados, agregar comentarios, enviar notificaciones por correo electrónico y facilitar la comunicación entre estudiantes y docentes durante el proceso de revisión académica.

El sistema fue desarrollado como parte del ejercicio académico propuesto, cumpliendo con los requisitos de autenticación, roles, gestión de proyectos, comentarios, filtros, exportación de información y uso de vistas basadas en clases.

---

## Integrantes

- Julio
- William
- Diego
- Mike

---

## Funcionalidades principales

### Autenticación y roles

El sistema maneja autenticación mediante inicio y cierre de sesión.

Roles implementados:

- **Estudiante:** puede crear, editar, eliminar y consultar sus propios proyectos.
- **Docente:** puede revisar proyectos, cambiar estados, asignar calificación y comentar.
- **Administrador:** puede gestionar usuarios, grupos, proyectos y comentarios desde el panel administrativo de Django.

---

### Gestión de proyectos

Los estudiantes pueden:

- Registrar proyectos académicos.
- Editar proyectos propios.
- Eliminar proyectos propios.
- Consultar el detalle de sus proyectos.
- Subir un documento asociado al proyecto.

Los docentes pueden:

- Consultar los proyectos de todos los estudiantes.
- Revisar proyectos.
- Cambiar el estado del proyecto.
- Asignar calificación.
- Registrar la fecha de revisión.

Estados disponibles:

- Enviado
- En Revisión
- Aprobado

---

### Gestión de comentarios

Cada comentario registra:

- Usuario que realiza el comentario.
- Fecha de creación.
- Texto del comentario.
- Proyecto asociado.

Cuando se crea un comentario, el sistema genera una notificación por correo electrónico dirigida al estudiante correspondiente.

Cuando un proyecto queda en estado **Aprobado**, el sistema bloquea la creación de nuevos comentarios.

---

### Visualización y reportes

El sistema permite:

- Filtrar proyectos por estado.
- Filtrar proyectos por estudiante.
- Exportar la lista de proyectos en formato CSV.
- Exportar la lista de proyectos en formato PDF.

---

## Tecnologías utilizadas

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap
- django-crispy-forms
- crispy-bootstrap5
- ReportLab
- Git
- GitHub
- GitFlow

---



