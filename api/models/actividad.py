from django.db import models
from django.utils.translation import gettext_lazy as _


class Actividad(models.Model):
    """
    El modelo Actividad es una representación para el registro de las actividades del colaborador. Tiene la estructura
    de una bitácora y que sirve para registrar las tareas diarias del colaborador.

    :param colaborador: Clave foránea al modelo :class:`CustomUser`.
    :param fecha: Campo de fecha para la fecha de registro de la actividad.
    :param hora_inicio: Campo de tiempo para el registro de la hora de inicio de la actividad.
    :param hora_termino: Campo de tiempo para el registro de la hora de término de la actividad (opcional).
    :param datos_actividad: Clave foránea al modelo :class:`DatosActividad`.
    :param proyecto: Clave foránea al modelo :class:`Proyecto`.
    :param observaciones: Campo de texto para las observaciones de la actividad (opcional).
    :param created: Campo de fecha y hora de la fecha de creación de la actividad (Auto generado).
    :param modified: Campo de fecha y hora de la última fecha de modificación de la actividad (Auto generado).

    **Ejemplos de uso**

    Para su creación se necesita de los campos :class:`DatosActividad` y :class:`Proyecto` con datos en el sistema,
    y se usan los siguientes pasos:

    *Creación de una Actividad*

    Ejemplo:
    ::
        # Librería para la carga de fechas
        import datetime

        # Valores de claves foráneas
        colaborador_elegido = Colaborador.objects.get(pk=1)
        datos_actividad_elegido = DatosActividad.objects.get(pk=1)
        proyecto_elegido = Proyecto.objects.get(pk=1)

        # Creación de la nueva Actividad
        nuevo_actividad = Actividad.objects.create(
            colaborador=colaborador_elegido,
            fecha=datetime.date(2020, 01, 01),
            hora_inicio=datetime.time(14, 30, 0),
            datos_actividad=datos_actividad_elegido,
            proyecto=proyecto_elegido
        )

    *Actualización de un Actividad*

    Ejemplo:
    ::
        # Librería para la carga de fechas
        import datetime

        # Obtener alguna Actividad existente
        actividad_elegida = Actividad.objects.get(pk=1)

        # Generar cambios a la actividad obtenida
        actividad_elegida.hora_termino = datetime.time(15, 30, 0)

        # Guardando cambios hechos
        actividad_elegida.save()

    """
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    fecha = models.DateField(_('fecha'))
    hora_inicio = models.TimeField(_('hora de inicio'))
    hora_termino = models.TimeField(_('hora de término'), blank=True, null=True)
    datos_actividad = models.ForeignKey('DatosActividad', on_delete=models.CASCADE, verbose_name='datos de actividad')
    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
    observaciones = models.TextField(_('observaciones'), blank=True, null=True)
    created = models.DateTimeField(_('creado'), auto_now_add=True)
    modified = models.DateTimeField(_('modificado'), auto_now=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('actividad')
        verbose_name_plural = _('actividades')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del dato de actividad, hora de inicio y término (si existe) de la actividad
            y fecha de la actividad
        """
        return '{} - desde {}{} - {}'.format(
            self.datos_actividad.nombre,
            self.hora_inicio.isoformat(),
            f' hasta {self.hora_termino.isoformat()}' if self.hora_termino else '',
            self.fecha.isoformat()
        )


class DatosActividad(models.Model):
    """
    El modelo DatosActividad representa los datos generales de una :class:`Actividad`. Por lo tanto mientras la
    Actividad guarda valores como bitácora, DatosActividad registra valores de descripción de la actividad realizada.
    Estos datos de actividad corresponden a las posibles actividades de un :class:`Cargo`.

    :param nombre: Campo de texto con el nombre de actividades (largo máximo: 50 caracteres, único).
    :param descripcion: Campo de texto con la descripción de actividades (opcional).
    :param tiempo_maximo: Campo numérico positivo que describe el estimado tiempo máximo de una actividad en minutos
        (opcional).
    :param tiempo_minimo: Campo numérico positivo que describe el estimado tiempo mínimo de una actividad en minutos
        (opcional).
    :param cargo: Clave foránea al modelo :class:`Cargo`.

    **Ejemplos de uso**

    Para su creación se necesita que al menos exista un campo de :class:`Cargo` y se usan los siguientes pasos:

    *Creación de una DatosActividad*

    Ejemplo:
    ::
        # Valores de claves foráneas
        cargo_elegido = Cargo.objects.get(pk=1)

        # Creación de la nueva Actividad
        nuevo_datos_actividad = Actividad.objects.create(
            nombre='Resolver ticket simple',
            tiempo_maximo=60,
            tiempo_minimo=5,
            cargo=cargo_elegido
        )

    *Actualización de un DatosActividad*

    Ejemplo:
    ::
        # Obtener algún DatosActividad existente
        datos_actividad_elegida = DatosActividad.objects.get(pk=1)

        # Generar cambios a los datos de actividad obtenido
        datos_actividad_elegida.tiempo_minimo = 10

        # Guardando cambios hechos
        datos_actividad_elegida.save()
    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)
    descripcion = models.TextField(_('descripcion'), blank=True, null=True)
    tiempo_maximo = models.SmallIntegerField(_('tiempo_maximo'), blank=True, null=True)
    tiempo_minimo = models.SmallIntegerField(_('tiempo_minimo'), blank=True, null=True)
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('datos de actividad')
        verbose_name_plural = _('datos de actividades')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre y cargo del dato de actividad.
        """
        return f'{self.nombre} - {self.cargo.nombre}'


class Proyecto(models.Model):
    """
    El modelo Proyecto se encarga de representar los proyectos asociados al modelo :class:`Actividad`, para una mejor
    comprensión de esta y una mejor agrupación para reportes. Además este modelo esta asociado al modelo
    :class:`Cliente`.

    :param nombre: Campo de texto con el nombre del proyecto (largo máximo: 100 caracteres).
    :param cliente: Clave foránea al modelo :class:`Cliente`.
    :param repositorio: Campo de texto con el enlace al repositorio que contiene el codigo del proyecto (Con validación
        de URL, opcional).

    **Ejemplos de uso**

    Para su creación se necesita que al menos exista un campo de :class:`Cliente` y se usan los siguientes pasos:

    *Creación de una Proyecto*

    Ejemplo:
    ::
        # Valores de claves foráneas
        cliente_elegido = Cliente.objects.get(pk=1)

        # Creación del nuevo Proyecto
        nuevo_proyecto = Proyecto.objects.create(
            nombre='Mapa de derivación',
            cliente=cliente_elegido
        )

    *Actualización de un Proyecto*

    Ejemplo:
    ::
        # Obtener algún Proyecto existente
        proyecto_elegido = Proyecto.objects.get(pk=1)

        # Generar cambios al proyecto obtenido
        proyecto_elegido.repositorio = 'https://repositorio.del.proyecto.com'

        # Guardando cambios hechos
        proyecto_elegido.save()
    """
    nombre = models.CharField(_('nombre'), max_length=100)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    repositorio = models.URLField(_('repositorio'), blank=True, null=True)

    class Meta:
        verbose_name = _('proyecto')
        verbose_name_plural = _('proyectos')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del proyecto y el nombre del cliente.
        """
        return f'{self.nombre} - {self.cliente.nombre}'


class Cliente(models.Model):
    """
    El modelo Cliente se encarga de representar todos los clientes del sistema.

    :param nombre: Campo de texto con el nombre del cliente (largo máximo: 100 caracteres).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de una Cliente*

    Ejemplo:
    ::
        # Creación del nuevo Cliente
        nuevo_cliente = Cliente.objects.create(
            nombre='Sistemas Expertos'
        )

    *Actualización de un Cliente*

    Ejemplo:
    ::
        # Obtener algún Cliente existente
        cliente_elegido = Cliente.objects.get(pk=1)

        # Generar cambios al cliente obtenido
        cliente_elegido.nombre = 'Sistemas Expertos e Ingeniería de Software'

        # Guardando cambios hechos
        cliente_elegido.save()
    """
    nombre = models.CharField(_('nombre'), max_length=100, unique=True)

    class Meta:
        verbose_name = _('cliente')
        verbose_name_plural = _('clientes')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del cliente.
        """
        return self.nombre


class MesaAyuda(models.Model):
    """
    El modelo MesaAyuda se encarga de expandir las actividades con campos propios de la atención de mesa de ayuda.
    Por lo tanto está asociado con el modelo :class:`Actividad` y otros modelos como :class:`TipoSoporte` y
    :class:`Modulo`.

    :param actividad: Clave foránea al modelo :class:`Actividad` (relación uno a uno).
    :param tipo_soporte: Clave foránea al modelo :class:`TipoSoporte`.
    :param modulo: Clave foránea al modelo :class:`Modulo`.
    :param funcionario: Campo de texto para el nombre del funcionario atendido en mesa de ayuda (largo máximo:
        200 caracteres).
    :param telefono: Campo de texto para el telefono de funcionario atendido en mesa de ayuda (largo máximo: 20
        caracteres, opcional).
    :param email: Campo de texto con el email del funcionario atendido en mesa de ayuda (con validación de email,
        opcional).
    :param is_habil: Campo booleano para la representar si la mesa de ayuda se ejecutó en horario habil o no.
    :param created: Campo de fecha y hora de la fecha de creación del colaborador (Auto generado).
    :param modified: Campo de fecha y hora de la última fecha de modificación del colaborador (Auto generado).

    **Ejemplos de uso**

    Para su creación es necesario que existan campos en :class:`Actividad`, :class:`TipoSoporte` y :class:`Modulo`,
    y se usan los siguientes pasos:

    *Creación de una MesaAyuda*

    Ejemplo:
    ::
        # Valores de claves foráneas
        actividad_elegida = Actividad.objects.get(pk=1)
        tipo_soporte_elegido = TipoSoporte.objects.get(pk=1)
        modulo_elegido = Modulo.objects.get(pk=1)

        # Creación de la nueva MesaAyuda
        nueva_mesa_ayuda = MesaAyuda.objects.create(
            actividad=actividad_elegida,
            tipo_soporte=tipo_soporte_elegido,
            modulo=modulo_elegido,
            funcionario='Juan Soto',
            telefono='+56998765432',
            email='juan.soto@email.com',
            is_habil=false
        )

    *Actualización de MesaAyuda*

    Ejemplo:
    ::
        # Obtener alguna MesaAyuda existente
        mesa_ayuda_elegida = MesaAyuda.objects.get(pk=1)

        # Generar cambios a la mesa de ayuda obtenida
        mesa_ayuda_elegida.funcionario = 'Juan Perez'

        # Guardando cambios hechos
        mesa_ayuda_elegida.save()
    """
    actividad = models.OneToOneField('Actividad', on_delete=models.CASCADE)
    tipo_soporte = models.ForeignKey('TipoSoporte', on_delete=models.CASCADE)
    modulo = models.ForeignKey('Modulo', on_delete=models.CASCADE, verbose_name='módulo')
    funcionario = models.CharField(_('funcionario'), max_length=200)
    telefono = models.CharField(_('teléfono'), max_length=20, blank=True, null=True)
    correo_electronico = models.EmailField(_('correo electrónico'), blank=True, null=True)
    is_habil = models.BooleanField(_('horario hábil'))
    created = models.DateTimeField(_('creado'), auto_now_add=True)
    modified = models.DateTimeField(_('modificado'), auto_now=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('atención de mesa de ayuda')
        verbose_name_plural = _('atenciones de mesa de ayuda')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del tipo de soporte, nombre del módulo, y si fue atendido en horario hábil.
        """
        return f'{self.tipo_soporte.nombre} - {self.modulo.nombre} - ¿hábil?: {"Si" if self.is_habil else "No"}'


class TipoSoporte(models.Model):
    """
    El modelo TipoSoporte representa los tipos de soporte que se pueden dar al modelo :class:`MesaAyuda`.

    :param nombre: Campo de texto con el nombre del tipo de soporte (largo máximo: 50 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de una TipoSoporte*

    Ejemplo:
    ::
        # Creación del nuevo TipoSoporte
        nuevo_tipo_soporte = TipoSoporte.objects.create(
            nombre='Cambio de contraseña'
        )

    *Actualización de TipoSoporte*

    Ejemplo:
    ::
        # Obtener algún TipoSoporte existente
        tipo_soporte_elegido = TipoSoporte.objects.get(pk=1)

        # Generar cambios en el tipo de soporte obtenido
        tipo_soporte_elegido.nombre = 'Recuperación de contraseña'

        # Guardando cambios hechos
        tipo_soporte_elegido.save()
    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('tipo de soporte')
        verbose_name_plural = _('tipos de soportes')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre.
        """
        return self.nombre


class Modulo(models.Model):
    """
    El modelo Modulo representa los módulos que se pueden asignar al modelo :class:`MesaAyuda`. Además este módulo se
    encuentra asociado a los modelos :class:`Proyecto` y :class:`Ticket`.

    :param nombre: Campo de texto con el nombre del módulo (largo máximo: 100 caracteres).
    :param proyecto: Clave foránea al modelo :class:`Proyecto`.

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de un Modulo*

    Ejemplo:
    ::
        # Valores de claves foráneas
        proyecto_elegido = Proyecto.objects.get(pk=1)

        # Creación del nuevo Modulo
        nuevo_modulo = Modulo.objects.create(
            nombre='Odontología',
            proyecto=proyecto_elegido
        )

    *Actualización de Modulo*

    Ejemplo:
    ::
        # Obtener algún Modulo existente
        modulo_elegido = Modulo.objects.get(pk=1)

        # Generar cambios en el tipo de soporte obtenido
        modulo_elegido.nombre = 'Cardiología'

        # Guardando cambios hechos
        modulo_elegido.save()
    """
    nombre = models.CharField(_('nombre'), max_length=100)
    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        """
        verbose_name = _('módulo')
        verbose_name_plural = _('modulos')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del módulo, nombre del proyecto asociado, y nombre del cliente asociado.
        """
        return f'{self.nombre} - {self.proyecto.nombre} - {self.proyecto.cliente.nombre}'
