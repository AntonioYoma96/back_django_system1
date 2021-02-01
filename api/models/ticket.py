import os
from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


def get_file_ticket_path(instance, filename):
    """
    Método que crea un path con la constante *ticket* y el id de este, y retorna el path para la imagen solicitada,
    cambiando el nombre a uno genérico.

    :param instance: Valor defecto para el contexto actual
    :param filename: Nombre del archivo a guardar
    :return: Cadena de texto con el path final para el guardado de imágenes
    """
    ticket_path = f'ticket_{instance.ticket.id}'
    return new_filename(ticket_path, filename)


def get_file_message_path(instance, filename):
    """
    Método que crea un path con la constante *mensaje* y el id de este, y retorna el path para la imagen solicitada,
    cambiando el nombre a uno genérico.

    :param instance: Valor defecto para el contexto actual
    :param filename: Nombre del archivo a guardar
    :return: Cadena de texto con el path final para el guardado de imágenes
    """
    ticket_path = f'mensaje_{instance.ticket.id}'
    return new_filename(ticket_path, filename)


def new_filename(base_path, file):
    """
    Método que recibe el path relativo, y el nombre del archivo a guardar para generar un nuevo nombre de archivo
    estandarizado con la raíz basada en el path recibido.

    :param base_path: Cadena de texto con el path raíz
    :param file: Cadena de texto con el nombre del archivo a guardar
    :return: Cadena de texto con el path estandarizado
    """
    today = datetime.now()
    root = 'files'
    filename = '{year}_{month}_{day}_{secs}.{extension}'.format(
        year=today.year,
        month=today.month,
        day=today.day,
        secs=today.microsecond,
        extension=file.split('.')[-1]
    )
    return os.path.join(root, base_path, filename)


class Ticket(models.Model):
    asignado = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='ticket_asignado')
    solicitante = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='ticket_solicitante')
    validador = models.ForeignKey(
        'Colaborador',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='ticket_validador'
    )
    origen = models.ForeignKey('Origen', on_delete=models.CASCADE)
    modulo = models.ForeignKey('Modulo', on_delete=models.CASCADE, verbose_name='módulo')
    version = models.CharField(_('versión'), max_length=10, blank=True, null=True)
    prioridad = models.ForeignKey('Prioridad', on_delete=models.CASCADE)
    tipo_ticket = models.ForeignKey('TipoTicket', on_delete=models.CASCADE, verbose_name='tipo de ticket')
    fecha_limite = models.DateField(_('fecha límite'), blank=True, null=True)
    ruta = models.URLField(blank=True, null=True)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField(_('descripción'))
    etapa_ticket = models.ForeignKey('EtapaTicket', on_delete=models.CASCADE, verbose_name='etapa del ticket')
    dificultad_ticket = models.ForeignKey('DificultadTicket', on_delete=models.CASCADE,
                                          verbose_name='dificultad del ticket', blank=True, null=True)
    fecha_solicitud = models.DateTimeField(_('fecha de solicitud'), default=datetime.now)
    created = models.DateTimeField(_('creado'), auto_now_add=True)
    modified = models.DateTimeField(_('modificado'), auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.asunto[:50]} - {self.etapa_ticket.nombre}'


class TicketLog(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    historial = models.JSONField(_('historial'), default=dict)
    responsable = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    observaciones = models.TextField(_('observaciones'), blank=True, null=True)
    fecha_modificacion = models.DateTimeField(_('fecha de modificación'), auto_now_add=True)

    class Meta:
        verbose_name = _('historial del ticket')
        verbose_name_plural = _('historiales de los tickets')

    def __str__(self):
        return 'Ticket {} - Fecha de cambio {}'.format(
            self.ticket.id,
            self.fecha_modificacion
        )


class Prioridad(models.Model):
    """
    El modelo Prioridad es una representación de las prioridades puede tener el modelo :class:`Ticket`.

    :param nombre: Campo de texto con el nombre de la prioridad (largo máximo: 50 caracteres, único).
    :param valor: Campo numérico para la valorización de la prioridad (único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de Prioridad*

    Ejemplo:
    ::
        # Creación de la nueva Prioridad
        nueva_prioridad = Prioridad.objects.create(
            nombre='Baja',
            valor=1
        )

    *Actualización del modelo Prioridad*

    Ejemplo:
    ::
        # Obtener Prioridad existente
        prioridad_elegida = Prioridad.objects.get(pk=1)

        # Generar cambios a la prioridad obtenida
        prioridad_elegida.nombre = 'Muy baja'

        # Guardando cambios hechos
        prioridad_elegida.save()

    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)
    valor = models.SmallIntegerField(_('valor'), unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('prioridad')
        verbose_name_plural = _('prioridades')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del área funcional.
        """
        return f'{self.nombre} - {self.valor}'


class TipoTicket(models.Model):
    """
    El modelo TipoTicket es una representación de los tipos de ticket que puede tener el modelo :class:`Ticket`.

    :param nombre: Campo de texto con el nombre del tipo de ticket (largo máximo: 100 caracteres).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de TipoTicket*

    Ejemplo:
    ::
        # Creación del nuevo TipoTicket
        nuevo_tipo_ticket = TipoTicket.objects.create(
            nombre='Incidencia en producción'
        )

    *Actualización del modelo TipoTicket*

    Ejemplo:
    ::
        # Obtener TipoTicket existente
        tipo_ticket_elegido = TipoTicket.objects.get(pk=1)

        # Generar cambios al tipo de ticket obtenido
        tipo_ticket_elegido.nombre = 'Requerimiento BD'

        # Guardando cambios hechos
        tipo_ticket_elegido.save()

    """
    nombre = models.CharField(_('nombre'), max_length=100)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('tipo de ticket')
        verbose_name_plural = _('tipos de ticket')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre y tipo del tipo de ticket.
        """
        return self.nombre


class EtapaTicket(models.Model):
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('etapa del ticket')
        verbose_name_plural = _('etapa de los tickets')

    def __str__(self):
        return self.nombre


class AreaTicket(models.Model):
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        verbose_name = _('área del ticket')
        verbose_name_plural = _('áreas de los tickets')

    def __str__(self):
        return self.nombre


class DificultadTicket(models.Model):
    tipo = models.CharField(_('tipo'), max_length=50)
    nivel = models.CharField(_('nivel'), max_length=50, blank=True, null=True)
    rev_min = models.FloatField(_('tiempo mínimo de revisión'), blank=True, null=True)
    rev_max = models.FloatField(_('tiempo máximo de revisión'), blank=True, null=True)
    dev_min = models.FloatField(_('tiempo mínimo de desarrollo'), blank=True, null=True)
    dev_max = models.FloatField(_('tiempo máximo de desarrollo'), blank=True, null=True)
    area_ticket = models.ForeignKey('AreaTicket', on_delete=models.CASCADE, verbose_name='área del ticket')

    class Meta:
        verbose_name = _('dificultad de ticket')
        verbose_name_plural = _('dificultades de los tickets')

    def __str__(self):
        return '{} - {}{}'.format(
            self.area_ticket.nombre,
            self.tipo,
            f' - {self.nivel}' if self.nivel else ''
        )

    @property
    def full_dificultad(self):
        return '{}{}'.format(
            self.tipo,
            f' - {self.nivel}' if self.nivel else ''
        )


class ArchivoTicket(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    archivo = models.FileField(_('archivo'), upload_to=get_file_ticket_path)

    class Meta:
        verbose_name = _('archivo del ticket')
        verbose_name_plural = _('archivos de los tickets')

    def __str__(self):
        return f'{self.ticket.id} - {self.ticket.asunto[:50]} - {self.slice_path()}'

    def slice_path(self):
        return '..{}{}'.format(
            '\\' if self.archivo[-50:][0] != '\\' else '',
            self.archivo[-50:]
        )


class Mensaje(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    asunto = models.CharField(_('asunto'), max_length=100)
    descripcion = models.TextField(_('descripción'))
    autor = models.ForeignKey('Colaborador', models.CASCADE)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        verbose_name = _('mensaje')
        verbose_name_plural = _('mensajes')

    def __str__(self):
        return f'Ticket: {self.ticket.id} - Mensaje: {self.asunto}'


class ArchivoMensaje(models.Model):
    mensaje = models.ForeignKey('Mensaje', on_delete=models.CASCADE)
    archivo = models.ImageField(_('archivo'), upload_to=get_file_message_path)

    class Meta:
        verbose_name = _('archivo del mensaje')
        verbose_name_plural = _('archivos de los mensajes')

    def __str__(self):
        return f'{self.mensaje.id} - {self.mensaje.asunto[:50]} - {self.slice_path()}'

    def slice_path(self):
        return '..{}{}'.format(
            '\\' if self.archivo[-50:][0] != '\\' else '',
            self.archivo[-50:]
        )


class Etiqueta(models.Model):
    """
    El modelo Etiqueta es una representación que conserva las etiquetas del modelo :class:`Ticket` y :class:`Mensaje`.

    :param nombre: Campo de texto con el nombre de la etiqueta (largo máximo: 50 caracteres, único).
    :param nivel_severidad: Campo de texto con el nivel de severidad de la etiqueta (largo máximo: 50 caracteres, único,
        incluye opciones).
    :param tickets: Clave foránea al modelo :class:`Ticket` (relación muchos a muchos).
    :param mensajes: Clave foránea al modelo :class:`Mensaje` (relación muchos a muchos).

    **Ejemplos de uso**

    Para su creación se necesita del campo :class:`Ticket` o :class:`Mensaje` con entradas y se usan los siguientes
    pasos:

    *Creación de Etiqueta*

    Ejemplo:
    ::
        # Valores de claves foráneas
        mensaje_elegido = Mensaje.objects.get(pk=1)

        # Creación de la nueva Etiqueta
        nueva_etiqueta = Etiqueta.objects.create(
            nombre='Falta información',
            mensaje=mensaje_elegido
        )

    *Actualización del modelo Etiqueta*

    Ejemplo:
    ::
        # Obtener Etiqueta existente
        etiqueta_elegida = Etiqueta.objects.get(pk=1)

        # Generar cambios a la etiqueta obtenida
        etiqueta_elegida.nombre = 'Falta rellenar'

        # Guardando cambios hechos
        etiqueta_elegida.save()

    """

    class NivelSeveridad(models.TextChoices):
        INFO = 'info', _('Informativo')
        SUCCESS = 'success', _('Positivo')
        WARNING = 'warning', _('Precaución')
        DANGER = 'danger', _('Peligro')

    nombre = models.CharField(_('nombre'), max_length=50, unique=True)
    nivel_severidad = models.CharField(_('nivel_severidad'), max_length=50, choices=NivelSeveridad.choices,
                                       default=NivelSeveridad.INFO)
    tickets = models.ManyToManyField('Ticket', blank=True)
    mensajes = models.ManyToManyField('Mensaje', blank=True)

    class Meta:
        verbose_name = _('etiqueta')
        verbose_name_plural = _('etiquetas')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre de la etiqueta.
        """
        return self.nombre


class Origen(models.Model):
    """
    El modelo Origen es una representación que conserva los orígenes del modelo :class:`Ticket`.

    :param nombre: Campo de texto con el nombre del origen (largo máximo: 50 caracteres, único).

    **Ejemplos de uso**

    Para su creación se necesita del campo :class:`Ticket` con entradas y se usan los siguientes
    pasos:

    *Creación de Origen*

    Ejemplo:
    ::
        # Creación del nuevo Origen
        nuevo_origen = Origen.objects.create(
            nombre='MDA'
        )

    *Actualización del modelo Origen*

    Ejemplo:
    ::
        # Obtener Origen existente
        origen_elegido = Origen.objects.get(pk=1)

        # Generar cambios al origen obtenido
        origen_elegido.nombre = 'Interno'

        # Guardando cambios hechos
        origen_elegido.save()

    """
    nombre = models.CharField(_('nombre'), max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = _('origen')
        verbose_name_plural = _('orígenes')

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del origen.
        """
        return self.nombre
