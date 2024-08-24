# My Django Project

This is a Django project template.

![Badge en Desarollo](https://img.shields.io/badge/STATUS-EN%20DESAROLLO-green)
![Python](https://img.shields.io/badge/Python-3.10.x-lightblue)
![Django](https://img.shields.io/badge/Django-4.2.x-blue)
![Boostrap](https://img.shields.io/badge/Boostrap-5.x-yellow)
![HTML](https://img.shields.io/badge/HTML-5-violet)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.x-orange)
![Docker](https://img.shields.io/badge/Docker-20.x-blue)

## Pasos

1. Crear 3 Archivos requirements.txt Dockerfile docker-compose.yml

2. Configurar los archivos Estos archivos son los que están en el ejemplo con la configuración predeterminada

3. Ejecutar el comando:

```sh
docker compose run web django-admin startproject [nombre_proyecto] .
```
(Va con el punto al final)

```sh
docker compose up
```

4. Ingresamos al VSC al Docker con el Explorador remoto y creamos las carpetas extras

```sh
mkdir -p ./{templates,media,static/{css,js,img,lib}}
```

5. configurar en
   settings.py

```py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
```

```py
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
```

```py
#Aquí las aplicaciones por defecto
BASE_APP = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
#Aquí las aplicaciones de terceros
THIRD_APP = [
    #Configuración para

]
#Aquí las aplicaciones propias (Ordenar alfabéticamente)
OWN_APP = [

]
INSTALLED_APPS = BASE_APP + THIRD_APP + OWN_APP
```

```py
LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'
```

```py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], #Se agrega para definir la carpeta templates en la raiz del proyecto
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

```py
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / 'media'
```

```py
STATICFILES_DIRS = [
    BASE_DIR / 'static', ]
```

```py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": 'nombre_de_la_base_de_datos', #Reemplazar por el nombre de la base de datos del archivo docker-compose.yml
        "USER": config('USER_DB'),
        "PASSWORD": config('PASSWORD_DB'),
        "HOST": "db",
        "PORT": "5432",
    }
}
```

## License

This project is licensed under the MIT License.

## Contacto

- **Correo Electrónico**: alucase@gmail.com
- **LinkedIn**: [Lucas Acosta](https://www.linkedin.com/in/alucase/)
- **GitHub**: [ALucasE](https://github.com/ALucasE)
- **Web**: [alucase.github.io](https://alucase.github.io/)

---

¡Gracias por visitar mi github! Espero que disfrutes explorando mis proyectos.
