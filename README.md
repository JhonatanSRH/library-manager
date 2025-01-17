# Gestion de libros

Este proyecto es una aplicación backend desarrollada con Django y con conexion a MongoDB. A continuación, se detallan los pasos para instalar y ejecutar el proyecto en tu entorno local.

## Requisitos previos

Asegúrate de tener instalados los siguientes componentes:

- Python 3.x
- pip (gestor de paquetes de Python)
- virtualenv (opcional, pero recomendado)

## Instalación

1. Clona el repositorio en tu máquina local:

    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd library-manager
    ```

2. (Opcional) Crea y activa un entorno virtual:

    ```bash
    virtualenv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3. Crea un archivo .env con las variables de entorno:

    ```bash
    SECRET_KEY="Clave secreta de la aplicación"
    MONGO_URI="String de conexion a un cluster de MongoDB"
    ```

4. Instala las dependencias del proyecto:

    ```bash
    pip install -r requirements.txt
    ```

5. Realiza las migraciones de la base de datos:

    ```bash
    python manage.py migrate
    ```

6. Crea un superusuario para acceder al panel de administración:

    ```bash
    python manage.py createsuperuser
    ```

7. (Opcional) Añadir datos iniciales a MongoDB:

    ```bash
    python manage.py add_books
    ```

## Ejecución

1. Inicia el servidor de desarrollo de Django:

    ```bash
    python manage.py runserver
    ```

2. Abre tu navegador web y navega a `http://127.0.0.1:8000` para ver la aplicación en funcionamiento.

3. Accede al panel de administración en `http://127.0.0.1:8000/admin` e inicia sesión con el superusuario que creaste anteriormente.

## Licencia

Este proyecto está bajo la Licencia MIT.
