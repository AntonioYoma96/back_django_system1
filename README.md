# SmartPeople 2.0 (Backend)
Este repositorio contiene el backend para SmartPeople 2.0. Está basado en [Django](https://www.djangoproject.com/)
junto a su kit de herramientas [Django Rest Framework](https://www.django-rest-framework.org/). Además incorpora
[Sphinx](https://www.sphinx-doc.org/en/master/) para la rápida generación de documentación.

## Tabla de contenidos
1. [Requerimientos](#requerimientos)
2. [Instalando](#instalando)
3. [Mejorando Sphinx](#mejorando-sphinx)
 
## Requerimientos
Para levantar la aplicación, se necesitan las siguientes aplicaciones instaladas:
- Python 3.9

## Instalando
Los pasos para la instalación de esta aplicación son los siguientes:
1. Clonar este repositorio en la ubicación deseada.
2. Correr el comando `pip install -r requirements.txt`.
3. Configurar el ambiente basado en la plantilla [.sample_env](core/.sample_env) creando el archivo de nombre `.env` en
la misma [ubicación](core).
4. Sincronizar la base de datos con esta aplicación Django con el comando `python manage.py migrate`.
    - **NOTA**: Revisar si existen migraciones hechas. En el caso de no ser así, correr el comando
    `python manage.py makemigrations`.
5. Cargar los datos iniciales para el sistema con el comando `python manage.py loaddata [FIXTURE_NAME]` donde
_FIXTURE_NAME_ hace referencia a todos los archivos en la ubicación [fixtures/](fixtures).
    - **NOTA**: Como se puede observar, para cargar los datos se debe realizar archivo por archivo. Esto se puede omitir en
    los sistemas operativos basados en UNIX, ya que permite la serialización del carácter * (asterisco).
6. Correr la aplicación a través del servidor de defect de Django con el comando `python manage.py runserver`.
7. **EXTRA**: Para generar la documentación, basta con moverse a la ubicación `docs/` y ejecutar el comando `make html`.
Como recomendación, eliminar la carpeta `_build` cada vez que se generen estos documentos. Para revisar el resultado,
abrir el archivo _index_ en la ruta `docs/_build/index.html`.
## Mejorando Sphinx
Adicionalmente si se necesita agregar o corregir la documentación, revisar los archivos en formato **ReStructuredText**
(_.rst_) en la ubicación `docs/` para revisar la ruta a las definiciones de los módulos o agregar cualquier contenido
deseado.