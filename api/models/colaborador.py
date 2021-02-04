from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.validators import validate_run


class Colaborador(models.Model):
    """
    El modelo Colaborador es una representación con datos personalizados del usuario del sistema. Agrega valores
    esenciales para la aplicación y es el nucleo para el resto de las relaciones.

    :param usuario: Clave foránea al modelo :class:`users.models.CustomUser` del sistema (relación uno a uno).
    :param run: Campo de texto de RUN del colaborador (Incluye :func:`api.validators.validate_run`, largo máximo: 11
        caracteres).
    :param nombre: Campo de texto para el primer nombre del colaborador (largo máximo: 50 caracteres).
    :param segundo_nombre: Campo de texto para el segundo nombre del colaborador (largo máximo: 50 caracteres,
        opcional).
    :param apellido_paterno: Campo de texto para el primer apellido del colaborador (largo máximo: 50 caracteres).
    :param apellido_materno: Campo de texto para el segundo apellido del colaborador (largo máximo: 50 caracteres).
    :param fecha_nacimiento: Campo de fecha para la fecha de nacimiento del colaborador.
    :param fecha_defuncion: Campo de fecha para la fecha de defunción del colaborador (opcional).
    :param sexo: Clave foránea hacia el modelo :class:`Sexo`.
    :param estado_civil: Clave foránea hacia el modelo :class:`EstadoCivil`.
    :param nacionalidad: Clave foránea hacia el modelo :class:`Nacionalidad`.
    :param direccion: Campo de texto con la dirección del colaborador (opcional).
    :param comuna: Clave foránea hacia el modelo de :class:`Comuna`.
    :param telefono_fijo: Campo de texto para el teléfono fijo del colaborador (opcional).
    :param telefono_movil: Campo de texto para el teléfono móvil del colaborador (opcional).
    :param email_personal: Campo de texto para el email personal de colaborador (Incluye validación de email).
    :param fecha_ingreso: Campo de fecha para la fecha de ingreso del colaborador (no confundir con fecha de creación).
    :param created: Campo de fecha y hora de la fecha de creación del colaborador (Auto generado).
    :param modified: Campo de fecha y hora de la última fecha de modificación del colaborador (Auto generado).

    **Ejemplos de uso**

    Para su creación se necesita un usuario creado libre de asignación a otro modelo. Además también deben haber otros
    campos creados, como :class:`Sexo`, :class:`EstadoCivil`, :class:`Nacionalidad` y :class:`Comuna`.

    *Creación de un Colaborador*

    Ejemplo:
    ::
        # Librería para la carga de fechas
        import datetime

        # Valores de claves foráneas o valores pre cargados
        user_id = 1
        sexo = Sexo.objects.get(pk=1)
        est_civil = EstadoCivil.objects.get(pk=2)
        nac_id = 3
        comuna = Comuna.objects.get(pk=1)
        fecha_nac = datetime.date(1991, 1, 1)

        # Creación del nuevo Colaborador
        nuevo_colaborador = Colaborador.objects.create(
            usuario_id=user_id,
            run='11111111',
            nombre='José',
            apellido_paterno='Perez',
            apellido_materno='Lopez',
            fecha_nacimiento=fecha_nac,
            sexo=sexo,
            estado_civil=est_civil,
            nacionalidad_id=nac_id,
            comuna=comuna,
            email_personal='some@email.com'
            fecha_ingreso=datetime.date(2020, 1, 1)
        )

    *Actualización de un Colaborador*

    Ejemplo:
    ::
        # Obtener algún Colaborador existente
        colaborador = Colaborador.objects.get(pk=1)

        # Generar cambios al colaborador obtenido
        colaborador.nombre = 'Juan'

        # Guardando cambios hechos
        colaborador.save()
    """
    usuario = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    run = models.CharField('RUN', max_length=11, unique=True, validators=[validate_run])
    nombre = models.CharField(_('nombre'), max_length=50)
    segundo_nombre = models.CharField(_('segundo nombre'), max_length=50, blank=True, null=True)
    apellido_paterno = models.CharField(_('apellido paterno'), max_length=50)
    apellido_materno = models.CharField(_('apellido materno'), max_length=50)
    fecha_nacimiento = models.DateField(_('fecha de nacimiento'))
    fecha_defuncion = models.DateField(_('fecha de defunción'), blank=True, null=True)
    sexo = models.ForeignKey('Sexo', on_delete=models.CASCADE)
    estado_civil = models.ForeignKey('EstadoCivil', on_delete=models.CASCADE)
    nacionalidad = models.ForeignKey('Nacionalidad', on_delete=models.CASCADE, default=1)
    direccion = models.CharField(_('dirección'), max_length=200, blank=True, null=True)
    comuna = models.ForeignKey('Comuna', on_delete=models.CASCADE)
    telefono_fijo = models.CharField(_('teléfono fijo'), max_length=20, blank=True, null=True)
    telefono_movil = models.CharField(_('teléfono móvil'), max_length=20, blank=True, null=True)
    correo_personal = models.EmailField(_('correo personal'), default='')
    fecha_ingreso = models.DateField(_('fecha de ingreso'))
    created = models.DateTimeField(_('creado'), auto_now_add=True)
    modified = models.DateTimeField(_('modificado'), auto_now=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('colaborador')
        verbose_name_plural = _('colaboradores')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre y apellidos.
        """
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'

    def simple_name(self):
        """
        Función que sirve para simplificar el llamado del :class:`Colaborador` con un formato más conciso que lo
        identifica.

        :return: Cadena de texto con nombre y apellido paterno.
        """
        return f'{self.nombre} {self.apellido_paterno}'

    @property
    def full_name(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'

    @property
    def last_contrato(self):
        return self.contrato.order_by("fecha_inicio").last()


class Sexo(models.Model):
    """
    El modelo Sexo se encarga de guardar todas las variantes al sexo del :class:`Colaborador`.

    :param nombre: Cadena de texto para el nombre de sexo (largo máximo: 50 caracteres, único).

    **Ejemplos**

    Para la creación y actualización de Sexo se usan los siguientes pasos:

    *Creación de Sexo*

    Ejemplo:
    ::
        sexo = Sexo.objects.create(nombre="Femenino")

    *Actualización de Sexo*

    Ejemplo:
    ::
        # Se busca un campo de Sexo dentro del sistema
        sexo = Sexo.objects.get(pk=1)
        # Se cambia el campo de nombre
        sexo.nombre = "Masculino"
        # Se guarda el nuevo valor
        sexo.save()
    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('sexo')
        verbose_name_plural = _('sexos')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con nombre.
        """
        return self.nombre


class EstadoCivil(models.Model):
    """
    El modelo EstadoCivil se encarga de guardar todas las variantes al estado civil del :class:`Colaborador`.

    :param nombre: Cadena de texto para el nombre del estado civil (largo máximo: 50 caracteres, único).

    **Ejemplos**

    Para la creación y actualización de EstadoCivil se usan los siguientes pasos:

    *Creación de EstadoCivil*

    Ejemplo:
    ::
        estado_civil = EstadoCivil.objects.create(nombre="Soltero")

    *Actualización de EstadoCivil*

    Ejemplo:
    ::
        # Se busca un campo de EstadoCivil dentro del sistema
        estado_civil = EstadoCivil.objects.get(pk=1)
        # Se cambia el campo de nombre
        estado_civil.nombre = "Casado"
        # Se guarda el nuevo valor
        estado_civil.save()
    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        """
        Clase encargada de la información general para el funcionamiento en Django.

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('estado civil')
        verbose_name_plural = _('estados civiles')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con nombre.
        """
        return self.nombre


class Nacionalidad(models.Model):
    """
    El modelo Nacionalidad se encarga de guardar todas las variantes la nacionalidad del :class:`Colaborador`.

    :param nombre: Cadena de texto para el nombre de la nacionalidad (largo máximo: 50 caracteres, único).

    **Ejemplos**

    Para la creación y actualización de Nacionalidad se usan los siguientes pasos:

    *Creación de Nacionalidad*

    Ejemplo:
    ::
        nacionalidad = Nacionalidad.objects.create(nombre="Chileno")

    *Actualización de Nacionalidad*

    Ejemplo:
    ::
        # Se busca un campo de nacionalidad dentro del sistema
        nacionalidad = Nacionalidad.objects.get(pk=1)
        # Se cambia el campo de nombre
        nacionalidad.nombre = "Masculino"
        # Se guarda el nuevo valor
        nacionalidad.save()
    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        """
        Clase encargada de la información general para el funcionamiento en Django.

        Parámetros
        
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('nacionalidad')
        verbose_name_plural = _('nacionalidades')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con nombre.
        """
        return self.nombre


class Comuna(models.Model):
    """
    El modelo Comuna se encarga de guardar todas las variantes de comuna en Chile para el :class:`Colaborador`. Además
    está asociada a una provincia a través de una clave foránea.

    :param codigo: Cadena de texto que corresponde al código único territorial de la comuna (CUT) (largo máximo: 5
        caracteres).
    :param nombre: Cadena de texto para el nombre de la comuna (largo máximo: 50 caracteres).
    :param provincia: Clave foránea al modelo :class:`Provincia`.

    **Ejemplos**

    Para la creación y actualización de Comuna se necesita :class:`Provincia` existente, y se usan los siguientes
    pasos:

    *Creación de Comuna*

    Ejemplo:
    ::
        # Se obtiene alguna provincia existente
        provincia = Provincia.objects.get(pk=1)
        # Se crea la comuna basándonos en la provincia obtenida
        comuna = Comuna.objects.create(
            codigo="10101",
            nombre="Puerto Montt",
            provincia=provincia
        )

    *Actualización de Comuna*

    Ejemplo:
    ::
        # Se busca un campo de comuna dentro del sistema
        comuna = Comuna.objects.get(pk=1)
        # Se cambia el campo de nombre
        comuna.codigo = "10102"
        comuna.nombre = "Calbuco"
        # Se guarda el nuevo valor
        comuna.save()
    """
    codigo = models.CharField(_('código'), max_length=5, unique=True)
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)
    provincia = models.ForeignKey('Provincia', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('comuna')
        verbose_name_plural = _('comunas')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con código y nombre.
        """
        return f'{self.codigo} - {self.nombre}'


class Provincia(models.Model):
    """
    El modelo Provincia se encarga de guardar todas las variantes de provincia en Chile para el modelo
    :class:`Comuna`. Además está asociada a una :class:`Region` a través de una clave foránea.

    :param codigo: Cadena de texto que corresponde al código único territorial de la provincia (CUT) (largo máximo: 5
        caracteres).
    :param nombre: Cadena de texto para el nombre de la provincia (largo máximo: 50 caracteres).
    :param region: Clave foránea al modelo :class:`Region`.

    **Ejemplos**

    Para la creación y actualización de Provincia se necesita :class:`Region` existente, y se usan los siguientes
    pasos:

    *Creación de Provincia*

    Ejemplo:
    ::
        # Se obtiene alguna región existente
        region = Region.objects.get(pk=1)
        # Se crea la provincia basándonos en la región obtenida
        provincia = Provincia.objects.create(
            codigo="101",
            nombre="Llanquihue",
            region=region
        )

    *Actualización de Provincia*

    Ejemplo:
    ::
        # Se busca un campo de provincia dentro del sistema
        provincia = Provincia.objects.get(pk=1)
        # Se cambia el campo de nombre
        provincia.codigo = "102"
        provincia.nombre = "Chiloé"
        # Se guarda el nuevo valor
        provincia.save()
    """
    codigo = models.CharField(_('código'), max_length=5, unique=True)
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='región')

    class Meta:
        verbose_name = _('provincia')
        verbose_name_plural = _('provincias')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con código y nombre.
        """
        return f'{self.codigo} - {self.nombre}'


class Region(models.Model):
    """
    El modelo Region se encarga de guardar todas las variantes de región en Chile para el modelo :class:`Provincia`.

    :param codigo: Cadena de texto que corresponde al código único territorial de la región (CUT) (largo máximo: 5
        caracteres).
    :param nombre: Cadena de texto para el nombre de la región (largo máximo: 50 caracteres).

    **Ejemplos**

    Para la creación y actualización de Region se usan los siguientes pasos:

    *Creación de Region*

    Ejemplo:
    ::
        region = Region.objects.create(
            codigo="10",
            nombre="Los Lagos",
        )

    *Actualización de Region*

    Ejemplo:
    ::
        # Se busca un campo de region dentro del sistema
        region = Region.objects.get(pk=1)
        # Se cambia el campo de nombre
        region.codigo = "14"
        region.nombre = "Los Rios"
        # Se guarda el nuevo valor
        region.save()
    """
    codigo = models.CharField(_('código'), max_length=5, unique=True)
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        """
        Clase encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('región')
        verbose_name_plural = _('regiones')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con código y nombre.
        """
        return f'{self.codigo} - {self.nombre}'


class Hijo(models.Model):
    """
    El modelo Hijo se encarga de guardar todas las posibles relaciones de hijo con el modelo
    :class:`Colaborador`.

    :param colaborador: Clave foránea al modelo :class:`Colaborador`.
    :param nombres: Cadena de texto con los nombres del hijo (largo máximo: 100 caracteres).
    :param apellido_paterno: Cadena de texto con el apellido paterno del hijo (largo máximo: 100 caracteres).
    :param apellido_materno: Cadena de texto con el apellido materno del hijo (largo máximo: 100 caracteres, opcional).
    :param run: Cadena de texto con el RUN del hijo (Incluye :py:func:`api.validators.validate_run`, largo máximo: 11
        caracteres, opcional).
    :param fecha_nacimiento: Campo de fecha para la fecha de nacimiento del Hijo.

    **Ejemplos**

    Para la creación y actualización de Hijo se necesita :class:`Colaborador` existente y se usan los siguientes
    pasos:

    *Creación de Hijo*

    Ejemplo:
    ::
        # Se carga librería para el formato de fecha
        import datetime
        # Se obtiene algún campo de Colaborador en el sistema
        colaborador = Colaborador.objects.get(pk=1)
        # Se crea el Hijo con el colaborador obtenido
        hijo = Hijo.objects.create(
            colaborador=colaborador,
            nombres='Matías',
            apellido_paterno='Zúñiga',
            run='22222222',
            fecha_nacimiento=datetime.date(2000, 1, 1)
        )

    *Actualización de Hijo*

    Ejemplo:
    ::
        # Se busca un campo de hijo dentro del sistema
        hijo = Hijo.objects.get(pk=1)
        # Se cambia el campo necesario
        hijo.nombres = "Roberto"
        # Se guarda el nuevo valor
        hijo.save()
    """
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    nombres = models.CharField(_('nombres'), max_length=100)
    apellido_paterno = models.CharField(_('apellido paterno'), max_length=100)
    apellido_materno = models.CharField(_('apellido materno'), max_length=100, blank=True, null=False)
    run = models.CharField('RUN', max_length=11, blank=True, null=True, unique=True, validators=[validate_run])
    fecha_nacimiento = models.DateField(_('fecha de nacimiento'))

    class Meta:
        verbose_name = _('hijo')
        verbose_name_plural = _('hijos')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con primer nombre (si posee) y apellido paterno.
        """
        return f'{self.nombres.split(" ", 1)[0]} {self.apellido_paterno}'


class PersonaContacto(models.Model):
    """
    El modelo PersonaContacto se encarga de guardar todas las posibles relaciones de persona de contacto con el modelo
    :class:`Colaborador`.

    :param colaborador: Clave foránea al modelo :class:`Colaborador`.
    :param nombres: Cadena de texto con los nombres de la persona de contacto (largo máximo: 100 caracteres).
    :param apellido_paterno: Cadena de texto con el apellido paterno de la persona de contacto (largo máximo: 100
        caracteres).
    :param apellido_materno: Cadena de texto con el apellido materno de la persona de contacto (largo máximo: 100
        caracteres, opcional).
    :param telefono: Cadena de texto con el teléfono de la persona de contacto (largo máximo: 20 caracteres).

    **Ejemplos**

    Para la creación y actualización de PersonaContacto se necesita :class:`Colaborador` existente y se usan los
    siguientes pasos:

    *Creación de PersonaContacto*

    Ejemplo:
    ::
        # Se obtiene algún campo de Colaborador en el sistema
        colaborador = Colaborador.objects.get(pk=1)
        # Se crea PersonaContacto con el colaborador obtenido
        contacto = PersonaContacto.objects.create(
            colaborador=colaborador,
            nombres='María',
            apellido_paterno='Rosales',
            telefono='98765432'
        )

    *Actualización de PersonaContacto*

    Ejemplo:
    ::
        # Se busca un campo de PersonaContacto dentro del sistema
        contacto = PersonaContacto.objects.get(pk=1)
        # Se cambia el campo necesario
        contacto.nombres = "Juana"
        # Se guarda el nuevo valor
        contacto.save()
    """
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    nombres = models.CharField(_('nombres'), max_length=100)
    apellido_paterno = models.CharField(_('apellido paterno'), max_length=100)
    apellido_materno = models.CharField(_('apellido materno'), max_length=100, blank=True, null=True)
    telefono = models.CharField(_('teléfono'), max_length=20)

    class Meta:
        """
        Clase encargada de la información general para el funcionamiento en Django

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto
        """
        verbose_name = _('persona de contacto')
        verbose_name_plural = _('personas de contacto')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con primer nombre (si posee) y apellido paterno
        """
        return f'{self.nombres.split(" ", 1)[0]} {self.apellido_paterno}'


class ColaboradorSkill(models.Model):
    """
    El modelo ColaboradorSkill se encarga de guardar todas las posibles relaciones entre
    :class:`Colaborador`, :class:`Skill` y :class:`NivelSkill`.

    :param colaborador: Clave foránea al modelo :class:`Colaborador`.
    :param skill: Clave foránea al modelo :class:`Skill`.
    :param nivel_skill: Clave foránea al modelo :class:`NivelSkill`.

    **Ejemplos**

    Para la creación y actualización de ColaboradorSkill se necesitan valores existentes en :class:`Colaborador`,
    :class:`Skill` y :class:`NivelSkill`. Los pasos para esto son los siguientes:

    *Creación de ColaboradorSkill*

    Ejemplo:
    ::
        # Se obtiene algún campo de Colaborador en el sistema
        colaborador = Colaborador.objects.get(pk=1)
        # Se obtiene algún campo de Skill en el sistema
        # Se obtiene algún campo de NivelSkill en el sistema
        nivel_skill = NivelSkill.objects.get(pk=1)
        # Se crea PersonaContacto con el colaborador obtenido
        colaborador_skill = ColaboradorSkill.objects.create(
            colaborador=colaborador,}
            skill=skill,
            nivel_skill=nivel_skill
        )

    *Actualización de ColaboradorSkill*

    Ejemplo:
    ::
        # Se busca el campo necesario a cambiar
        skill = Skill.objects.get(pk=99)
        # Se busca un campo de ColaboradorSkill dentro del sistema
        colaborador_skill = ColaboradorSkill.objects.get(pk=1)
        # Se cambia el campo necesario
        colaborador_skill.skill = skill
        # Se guarda el nuevo valor
        colaborador_skill.save()
    """
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    nivel_skill = models.ForeignKey('NivelSkill', on_delete=models.CASCADE, verbose_name='nivel de skill')

    class Meta:
        """
        Clase encargada de la información general para el funcionamiento en Django
        
        :param verbose_name: Cadena de texto con la version singular del nombre del objeto
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto
        """
        verbose_name = _('skill del colaborador')
        verbose_name_plural = _('skills del colaborador')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con nombre simple del colaborador, nombre de la skill y nombre del nivel de skill
        """
        return '{} - {} - {}'.format(
            self.colaborador.simple_name(),
            self.skill.nombre,
            self.nivel_skill.nombre,
        )


class Skill(models.Model):
    """
    El modelo Skill se encarga de guardar todas las posibles habilidades (también skills) para el modelo
    :class:`Colaborador` a través de :class:`ColaboradorSkill`.

    :param nombre: Cadena de texto para el nombre de la skill (largo máximo: 50, único).

    **Ejemplos**

    Para la creación y actualización de Skill se usan los siguientes pasos:

    *Creación de Skill*

    Ejemplo:
    ::
        skill = Skill.objects.create(
            nombre='Django',
        )

    *Actualización de Skill*

    Ejemplo:
    ::
        # Se busca un campo de Skill dentro del sistema
        skill = Skill.objects.get(pk=1)
        # Se cambia el campo necesario
        skill.nombre = 'Python'
        # Se guarda el nuevo valor
        skill.save()
    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con nombre
        """
        return self.nombre


class NivelSkill(models.Model):
    """
    El modelo NivelSkill se encarga de guardar todos los posibles niveles de habilidad (también skills) para el modelo
    :class:`Skill` a través de :class:`ColaboradorSkill`.

    :param nombre: Cadena de texto para el nombre del nivel de skill (largo máximo: 50, único).

    **Ejemplos**

    Para la creación y actualización de NivelSkill se usan los siguientes pasos:

    *Creación de NivelSkill*

    Ejemplo:
    ::
        nivel_skill = NivelSkill.objects.create(
            nombre='Avanzado',
        )

    *Actualización de NivelSkill*

    Ejemplo:
    ::
        # Se busca un campo de Skill dentro del sistema
        nivel_skill = NivelSkill.objects.get(pk=1)
        # Se cambia el campo necesario
        nivel_skill.nombre = 'Experto'
        # Se guarda el nuevo valor
        nivel_skill.save()
    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        """
        Clase encargada de la información general para el funcionamiento en Django
        
        :param verbose_name: Cadena de texto con la version singular del nombre del objeto
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto
        """
        verbose_name = _('nivel de skill')
        verbose_name_plural = _('niveles de skills')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas
        funciones de Django.
        
        :return: Cadena de texto con nombre
        """
        return self.nombre
