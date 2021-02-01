from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class DatosFormacion(models.Model):
    """
    El modelo DatosFormacion representa la formación de algún :class:`Colaborador`. Sirve para registrar cualquier
    tipo de formación formal, ya sea de pregrado, técnica, entre otras. Por lo tanto este modelo está asociado a los
    modelos :class:`TipoFormacion`, :class:`Carrera`, :class:`EstadoFormacion` y :class:`Institucion` para una mejor
    comprensión.

    :param colaborador: Clave foránea al modelo :class:`Colaborador`.
    :param tipo_formacion: Clave foránea al modelo :class:`TipoFormacion`
    :param carrera: Clave foránea al modelo :class:`Carrera`.
    :param estado_formacion: Clave foránea al modelo :class:`EstadoFormacion`.
    :param fecha_termino: Campo de fecha para la fecha de término de la formacion del colaborador.
    :param institucion: Clave foránea al modelo :class:`Institucion`.

    **Ejemplos de uso**

    Para su creación se necesita de los campos :class:`Colaborador`, :class:`TipoFormacion`, :class:`Carrera`,
    :class:`EstadoFormacion` y :class:`Institucion` con datos en el sistema, y se usan los siguientes
    pasos:

    *Creación de DatosFormacion*

    Ejemplo:
    ::
        # Librería para la carga de fechas
        import datetime

        # Valores de claves foráneas
        colaborador_elegido = Colaborador.objects.get(pk=1)
        tipo_formacion_elegida = TipoFormacion.objects.get(pk=1)
        carrera_elegida = Carrera.objects.get(pk=1)
        estado_formacion_elegida = EstadoFormacion.objects.get(pk=1)
        institucion_elegida = Institucion.objects.get(pk=1)

        # Creación de la nueva DatosFormacion
        nuevo_datos_formacion = DatosFormacion.objects.create(
            colaborador=colaborador_elegido,
            tipo_formacion=tipo_formacion_elegida,
            carrera=carrera_elegida,
            estado_formacion=estado_formacion_elegida,
            fecha_termino=datetime.date(2015, 12, 1),
            institucion=institucion_elegida
        )

    *Actualización del modelo DatosFormacion*

    Ejemplo:
    ::
        # Obtener DatosFormacion existentes
        datos_formacion_elegidos = DatosFormacion.objects.get(pk=1)

        # Generar cambios a los datos de formación obtenidos
        datos_formacion_elegidos.fecha_termino = datetime.date(2016, 12, 1)

        # Guardando cambios hechos
        datos_formacion_elegidos.save()

    """
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    tipo_formacion = models.ForeignKey('TipoFormacion', on_delete=models.CASCADE, verbose_name='tipo de formación')
    carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
    estado_formacion = models.ForeignKey(
        'EstadoFormacion',
        on_delete=models.CASCADE,
        verbose_name='estado de formación'
    )
    fecha_termino = models.DateField(_('fecha de término'))
    institucion = models.ForeignKey('Institucion', on_delete=models.CASCADE, verbose_name='institución')

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('datos de formación')
        verbose_name_plural = _('datos de formaciones')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre de la carrera, y el nombre del estado de formación.
        """
        return f'{self.carrera.nombre} - {self.estado_formacion.nombre}'


class TipoFormacion(models.Model):
    """
    El modelo TipoFormacion es una representación de los tipos de formación que se pueden poseer en el modelo
    :class:`DatosFormacion`.

    :param nombre: Campo de texto con el nombre de tipo de formación (largo máximo: 50 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de TipoFormacion*

    Ejemplo:
    ::
        # Creación del nuevo TipoFormacion
        nuevo_tipo_formacion = TipoFormacion.objects.create(
            nombre='Pregrado'
        )

    *Actualización del modelo TipoFormacion*

    Ejemplo:
    ::
        # Obtener TipoFormacion existente
        tipo_formacion_elegido = TipoFormacion.objects.get(pk=1)

        # Generar cambios al tipo de formación obtenido
        tipo_formacion_elegido.nombre = 'Posgrado'

        # Guardando cambios hechos
        tipo_formacion_elegido.save()

    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('tipo de formación')
        verbose_name_plural = _('tipos de formación')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del tipo de formación.
        """
        return self.nombre


class Carrera(models.Model):
    """
    El modelo Carrera es una representación de las carreras profesionales que se pueden poseer en el modelo
    :class:`DatosFormacion`.

    :param nombre: Campo de texto con el nombre de una carrera profesional (largo máximo: 100 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de Carrera*

    Ejemplo:
    ::
        # Creación de la nueva Carrera
        nueva_carrera = Carrera.objects.create(
            nombre='Ingeniera Informática'
        )

    *Actualización del modelo Carrera*

    Ejemplo:
    ::
        # Obtener Carrera existente
        carrera_elegida = Carrera.objects.get(pk=1)

        # Generar cambios a la carrera obtenida
        carrera_elegida.nombre = 'Ingeniera Civil Informática'

        # Guardando cambios hechos
        carrera_elegida.save()

    """
    nombre = models.CharField(_('nombre'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('carrera')
        verbose_name_plural = _('carreras')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre de la carrera.
        """
        return self.nombre


class EstadoFormacion(models.Model):
    """
    El modelo EstadoFormacion es una representación de los estados de la formación que se pueden poseer en el modelo
    :class:`DatosFormacion`.

    :param nombre: Campo de texto con el nombre de un estado de formación (largo máximo: 100 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de EstadoFormacion*

    Ejemplo:
    ::
        # Creación del nuevo EstadoFormacion
        nuevo_estado_formacion = EstadoFormacion.objects.create(
            nombre='En espera de defensa'
        )

    *Actualización del modelo EstadoFormacion*

    Ejemplo:
    ::
        # Obtener EstadoFormacion existente
        estado_formacion_elegido = EstadoFormacion.objects.get(pk=1)

        # Generar cambios al estado de formación obtenido
        estado_formacion_elegido.nombre = 'Completa'

        # Guardando cambios hechos
        estado_formacion_elegido.save()

    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('estado de formación')
        verbose_name_plural = _('estados de formación')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del estado de formación.
        """
        return self.nombre


class Institucion(models.Model):
    """
    El modelo Institucion es una representación de las instituciones que se pueden poseer en el modelo
    :class:`DatosFormacion`. Además esta relacionada con el modelo :class:`TipoInstitucion` para una mejor
    representación.

    :param tipo_institucion: Clave foránea al modelo :class:`TipoInstitucion`.
    :param nombre: Campo de texto con el nombre de una institución (largo máximo: 100 caracteres, único).

    **Ejemplos de uso**

    Para su creación se necesita del campo :class:`TipoInstitucion` con datos en el sistema y se usan los siguientes
    pasos:

    *Creación de Institucion*

    Ejemplo:
    ::
        # Valores de claves foráneas
        tipo_institucion_elegido = TipoInstitucion.objects.get(pk=1)

        # Creación de la nueva Institucion
        nueva_institucion = Institucion.objects.create(
            tipo_institucion=tipo_institucion_elegido,
            nombre='Universidad San Sebastián'
        )

    *Actualización del modelo Institucion*

    Ejemplo:
    ::
        # Obtener Institucion existente
        institucion_elegida = Institucion.objects.get(pk=1)

        # Generar cambios a la institución obtenida
        institucion_elegida.nombre = 'Universidad de Los Lagos'

        # Guardando cambios hechos
        institucion_elegida.save()

    """
    tipo_institucion = models.ForeignKey(
        'TipoInstitucion',
        on_delete=models.CASCADE,
        verbose_name='tipo de institución'
    )
    nombre = models.CharField(_('nombre'), max_length=100, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('institución')
        verbose_name_plural = _('instituciones')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre de la institución.
        """
        return self.nombre


class TipoInstitucion(models.Model):
    """
    El modelo TipoInstitucion es una representación del tipo de instituciones que se pueden poseer en el modelo
    :class:`Institucion`.

    :param nombre: Campo de texto con el nombre del tipo de institución (largo máximo: 50 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de TipoInstitucion*

    Ejemplo:
    ::
        # Creación del nuevo TipoInstitucion
        nuevo_tipo_institucion = TipoInstitucion.objects.create(
            nombre='Universidad'
        )

    *Actualización del modelo TipoInstitucion*

    Ejemplo:
    ::
        # Obtener TipoInstitucion existente
        tipo_institucion_elegida = TipoInstitucion.objects.get(pk=1)

        # Generar cambios al tipo de institución obtenido
        tipo_institucion_elegida.nombre = 'Centro de Formación Técnica'

        # Guardando cambios hechos
        tipo_institucion_elegida.save()

    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('tipo de institución')
        verbose_name_plural = _('tipos de instituciones')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del tipo de institución.
        """
        return self.nombre


class OtroFormacion(models.Model):
    """
    El modelo OtroFormacion representa la formación no tradicional de algún :class:`Colaborador`. Sirve para
    registrar cualquier tipo de formación atípica, ya sea mediante certificaciones, cursos, entre otras. Por lo tanto
    este modelo está asociado a los modelos :class:`Institucion`, :class:`TipoOtroFormacion`  y :class:`Diploma` para
    una mejor comprensión.

    :param colaborador: Clave foránea al modelo :class:`Colaborador`.
    :param institucion: Clave foránea al modelo :class:`Institucion`
    :param tipo_otra_formacion: Clave foránea al modelo :class:`TipoOtroFormacion`.
    :param diploma: Clave foránea al modelo :class:`Diploma`.
    :param horas: Campo decimal para la cantidad de horas cursadas en la formación (largo máximo: 6 valores, decimales
        máximos: 1 valor, con validación de solo positivos).

    **Ejemplos de uso**

    Para su creación se necesita de los campos :class:`Colaborador`, :class:`Institucion`,
    :class:`TipoOtroFormacion`, y :class:`Diploma` con datos en el sistema, y se usan los siguientes pasos:

    *Creación de OtroFormacion*

    Ejemplo:
    ::
        # Valores de claves foráneas
        colaborador_elegido = Colaborador.objects.get(pk=1)
        institucion_elegida = Institucion.objects.get(pk=1)
        tipo_otra_formacion_elegido = TipoOtroFormacion.objects.get(pk=1)
        diploma_elegido = Diploma.objects.get(pk=1)

        # Creación de la nueva OtroFormacion
        nueva_otro_formacion = OtroFormacion.objects.create(
            colaborador=colaborador_elegido,
            institucion=institucion_elegida,
            tipo_otra_formacion=tipo_otra_formacion_elegido,
            diploma=diploma_elegido,
            horas=205.5,
        )

    *Actualización del modelo OtroFormacion*

    Ejemplo:
    ::
        # Obtener OtroFormacion existente
        otro_formacion_elegida = OtroFormacion.objects.get(pk=1)

        # Generar cambios a otra formación obtenida
        otro_formacion_elegida.horas = 225.5

        # Guardando cambios hechos
        otro_formacion_elegida.save()

    """
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    institucion = models.ForeignKey('Institucion', on_delete=models.CASCADE, verbose_name='institución')
    tipo_otro_formacion = models.ForeignKey(
        'TipoOtroFormacion',
        on_delete=models.CASCADE,
        verbose_name='tipo otro de formación'
    )
    diploma = models.ForeignKey('Diploma', on_delete=models.CASCADE)
    horas = models.DecimalField(_('horas'), max_digits=6, decimal_places=1, validators=[MinValueValidator(0.0)])

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('datos de formación otros')
        verbose_name_plural = _('datos de formaciones otros')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del diploma y la cantidad de horas cursadas.
        """
        return f'{self.diploma.nombre} - {self.horas} hora{"s" if self.horas != 1.0 else ""}'


class TipoOtroFormacion(models.Model):
    """
    El modelo TipoOtroFormacion es una representación de los tipos no tradicionales de formación que pueden poseer en
    el modelo :class:`OtroFormacion`.

    :param nombre: Campo de texto con el nombre del tipo atípico de formación (largo máximo: 50 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de TipoOtroFormacion*

    Ejemplo:
    ::
        # Creación del nuevo TipoOtroFormacion
        nuevo_tipo_otro_formacion = TipoOtroFormacion.objects.create(
            nombre='Certificación'
        )

    *Actualización del modelo TipoOtroFormacion*

    Ejemplo:
    ::
        # Obtener TipoOtroFormacion existente
        tipo_otro_formacion_elegido = TipoOtroFormacion.objects.get(pk=1)

        # Generar cambios al otro tipo de formación obtenido
        tipo_otro_formacion_elegido.nombre = 'Curso'

        # Guardando cambios hechos
        tipo_otro_formacion_elegido.save()

    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('tipo otro de formación')
        verbose_name_plural = _('tipos otros de formación')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del tipo otro de formación.
        """
        return self.nombre


class Diploma(models.Model):
    """
    El modelo Diploma es una representación de los diplomas que pueden poseer en el modelo :class:`OtroFormacion`.

    :param nombre: Campo de texto con el nombre del diploma (largo máximo: 50 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de Diploma*

    Ejemplo:
    ::
        # Creación del nuevo Diploma
        nuevo_diploma = Diploma.objects.create(
            nombre='Python para principiantes'
        )

    *Actualización del modelo Diploma*

    Ejemplo:
    ::
        # Obtener Diploma existente
        diploma_elegido = Diploma.objects.get(pk=1)

        # Generar cambios al diploma obtenido
        diploma_elegido.nombre = 'Docker en ambientes de producción'

        # Guardando cambios hechos
        diploma_elegido.save()

    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('diploma')
        verbose_name_plural = _('diplomas')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del diploma.
        """
        return self.nombre
