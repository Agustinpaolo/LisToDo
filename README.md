Este proyecto es una aplicación web simple para gestionar tareas, desarrollada utilizando Flask y SQLite. 
La aplicación permite a los usuarios registrarse, iniciar sesión y gestionar sus tareas personales mediante funcionalidades de CRUD (Crear, Leer, Actualizar y Eliminar). 
Con una interfaz intuitiva y estilizada con Bootstrap, los usuarios pueden agregar nuevas tareas, marcarlas como completadas, editarlas o eliminarlas. 
Además, cuenta con contadores en tiempo real para mostrar el número de tareas pendientes y completadas, así como alertas visuales para confirmar las acciones realizadas.
Requisitos e Instalación

    Requisitos previos:
        Python 3.10 o superior.
        Flask y Flask-Login instalados (utilizando pip install flask flask-login).
        Werkzeug para la gestión de contraseñas (pip install werkzeug).

    Instalación:
        Clona este repositorio: git clone <URL_DEL_REPOSITORIO>.
        Entra al directorio del proyecto: cd to_do_app.
        Instala las dependencias necesarias: pip install -r requirements.txt (si el archivo está configurado).
        Ejecuta el archivo app.py: python app.py.
        Accede a la aplicación desde tu navegador en: http://127.0.0.1:5000.

Funcionalidades Principales

    Registro e inicio de sesión: Los usuarios pueden crear una cuenta con un nombre de usuario y contraseña seguros.
    Gestión de tareas: Crear, leer, editar, completar y eliminar tareas. Las tareas completadas se resaltan visualmente.
    Filtros y búsqueda: Los usuarios pueden buscar tareas específicas o filtrar por estado (pendientes o completadas).
    Alertas visuales: Mensajes dinámicos confirman las acciones del usuario (tarea creada, eliminada, editada, etc.).
    Persistencia de datos: Todas las tareas y usuarios se almacenan en una base de datos SQLite.

Si necesitas más ayuda o deseas contribuir, no dudes en abrir un issue en el repositorio o enviar un pull request.
