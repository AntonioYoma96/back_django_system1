import os
from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


def get_image_ticket_path(instance, filename):
    """
    Método que crea un path con la constante *ticket* y el id de este, y retorna el path para la imagen solicitada,
    cambiando el nombre a uno genérico.

    :param instance: Valor defecto para el contexto actual
    :param filename: Nombre del archivo a guardar
    :return: Cadena de texto con el path final para el guardado de imágenes
    """
    ticket_path = f'ticket_{instance.ticket.id}'
    return new_filename(ticket_path, filename)


def get_image_message_path(instance, filename):
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
    root = 'image'
    filename = '{year}_{month}_{day}_{secs}.{extension}'.format(
        year=today.year,
        month=today.month,
        day=today.day,
        secs=today.microsecond,
        extension=file.split('.')[-1]
    )
    return os.path.join(root, base_path, filename)


class Ticket(models.Model):
    """
    El modelo Ticket representa cualquier tipo de solicitud o incidencia que pueden generarse entre las entidades del
    modelo :class:`Colaborador`. Por lo tanto este modelo está asociado a los modelos :class:`Colaborador` como
    solicitante, receptor y validador, :class:`Origen`, :class:`Modulo`, :class:`Prioridad`, :class:`TipoTicket` y
    :class:`EtapaTicket` para una mejor comprensión.

    Además cuenta con un parámetro especial para el registro de historial del modelo Ticket basado en la aplicación
    **django-field-history**.

    :param asignado: Clave foránea al modelo :class:`Colaborador` como colaborador asignado.
    :param solicitante: Clave foránea al modelo :class:`Colaborador` como colaborador solicitante.
    :param validador: Clave foránea al modelo :class:`Colaborador` como colaborador validador (opcional).
    :param origen: Clave foránea al modelo :class:`Origen`.
    :param modulo: Clave foránea al modelo :class:`Modulo`.
    :param version: Campo de texto para la versión del sistema que originó el ticket (largo máximo: 10 caracteres,
        opcional).
    :param prioridad: Clave foránea al modelo :class:`Prioridad`.
    :param tipo_ticket: Clave foránea al modelo :class:`TipoTicket`.
    :param fecha_limite: Campo de fecha para la fecha límite de revisión del ticket (opcional).
    :param ruta: Campo de texto para la ruta del origen del problema a solucionar en el ticket (con validación
        de enlaces, opcional).
    :param asunto: Campo de texto para el asunto del ticket (largo máximo: 100 caracteres).
    :param descripcion: Campo de texto para la descripcion del ticket.
    :param estado_ticket: Clave foránea al modelo :class:`EtapaTicket`.
    :param created: Campo de fecha y hora de la fecha de creación del colaborador (Auto generado).
    :param modified: Campo de fecha y hora de la última fecha de modificación del colaborador (Auto generado).
    :param historial: Campo especial heredado de la clase :class:`field_history.tracker.FieldHistoryTracker` de la
        aplicación **django-field-history**. Lleva control de los parámetros :py:attr:`asignado` y
        :py:attr:`estado_ticket`

    **Ejemplos de uso**

    Para su creación se necesita de los campos :class:`Colaborador`, :class:`Origen`, :class:`Modulo`,
    :class:`Prioridad`, :class:`TipoTicket` y :class:`EtapaTicket` con datos en el sistema, y se usan los siguientes
    pasos:

    *Creación de Ticket*

    Ejemplo:
    ::
        # Valores de claves foráneas
        asignado_elegido = Colaborador.objects.get(pk=1)
        solicitante_elegido = Colaborador.objects.get(pk=1)
        origen_elegido = Origen.objects.get(pk=1)
        modulo_elegido = Modulo.objects.get(pk=1)
        prioridad_elegida = Prioridad.objects.get(pk=1)
        tipo_ticket_elegido = TipoTicket.objects.get(pk=1)
        etapa_ticket_elegido = EtapaTicket.objects.get(pk=1)

        # Creación de la nueva Ticket
        nuevo_ticket = Ticket.objects.create(
            asignado=asignado_elegido,
            solicitante=solicitante_elegido,
            origen=origen_elegido,
            modulo=modulo_elegido,
            prioridad=prioridad_elegida,
            tipo_ticket=tipo_ticket_elegido,
            asunto='Botón deshabilitado',
            descripcion='El botón se encuentra deshabilitado, y no se puede imprimir reportes',
            etapa_ticket=etapa_ticket_elegido
        )

    *Actualización del modelo Ticket*

    Ejemplo:
    ::
        # Obtener Ticket existente
        ticket_elegido = Ticket.objects.get(pk=1)

        # Generar cambios al ticket obtenido
        ticket_elegido.asunto = 'Botón desaparecido'

        # Guardando cambios hechos
        ticket_elegido.save()

    """
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
    version = models.CharField('versión', max_length=10, blank=True, null=True)
    prioridad = models.ForeignKey('Prioridad', on_delete=models.CASCADE)
    tipo_ticket = models.ForeignKey('TipoTicket', on_delete=models.CASCADE, verbose_name='tipo de ticket')
    fecha_limite = models.DateField('fecha límite', blank=True, null=True)
    ruta = models.URLField(blank=True, null=True)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField('descripción')
    etapa_ticket = models.ForeignKey('EtapaTicket', on_delete=models.CASCADE, verbose_name='etapa del ticket')
    created = models.DateTimeField('creado', auto_now_add=True)
    modified = models.DateTimeField('modificado', auto_now=True)

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con ID y asunto del ticket, y el nombre de la etapa del ticket.
        """
        return f'{self.id} - {self.asunto[:50]} - {self.etapa_ticket.nombre}'


class TicketLog(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    asignado = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='ticket_log_asignado')
    etapa_ticket = models.ForeignKey('EtapaTicket', on_delete=models.CASCADE, verbose_name='etapa del ticket')
    inicio_etapa = models.DateTimeField('inicio de etapa', auto_now_add=True)
    fin_etapa = models.DateTimeField('fin de etapa')

    class Meta:
        verbose_name = 'historial del ticket'
        verbose_name_plural = 'historiales de los tickets'

    def __str__(self):
        return 'Ticket {} - {} -{}{}'.format(
            self.ticket.id,
            self.etapa_ticket.nombre,
            self.inicio_etapa,
            f' - {self.fin_etapa}' if self.fin_etapa else ''
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
    nombre = models.CharField(max_length=50, unique=True)
    valor = models.SmallIntegerField(unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name_plural = 'prioridades'

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
    nombre = models.CharField(max_length=100)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = 'tipo de ticket'
        verbose_name_plural = 'tipos de ticket'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre y tipo del tipo de ticket.
        """
        return self.nombre


class EtapaTicket(models.Model):
    """
    El modelo EtapaTicket es una representación de los estados de ticket que se pueden poseer en el modelo
    :class:`Ticket`.

    :param nombre: Campo de texto con el nombre de la etapa del ticket (largo máximo: 50 caracteres, único).
    :param tipo: Campo de texto con la sub categorización de la etapa del ticket (largo máximo: 50 caracteres,
        opcional).
    :param rev_min: Campo numérico para la estimación mínima de revision del tipo de etapa (opcional).
    :param rev_max: Campo numérico para la estimación máxima de revision del tipo de etapa (opcional).
    :param dev_min: Campo numérico para la estimación mínima de desarrollo del tipo de etapa (opcional).
    :param dev_mx: Campo numérico para la estimación máxima de desarrollo del tipo de etapa (opcional).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de EtapaTicket*

    Ejemplo:
    ::
        # Creación de la nueva EtapaTicket
        nuevo_etapa_ticket = EtapaTicket.objects.create(
            nombre='Revisión'
        )

    *Actualización del modelo EtapaTicket*

    Ejemplo:
    ::
        # Obtener EtapaTicket existente
        etapa_ticket_elegido = EtapaTicket.objects.get(pk=1)

        # Generar cambios al estado de ticket obtenido
        etapa_ticket_elegido.nombre = 'Desarrollo'

        # Guardando cambios hechos
        etapa_ticket_elegido.save()

    """
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50, blank=True, null=True)
    dificultad = models.CharField(max_length=50, blank=True, null=True)
    rev_min = models.PositiveSmallIntegerField('tiempo mínimo de revisión', blank=True, null=True)
    rev_max = models.PositiveSmallIntegerField('tiempo máximo de revisión', blank=True, null=True)
    dev_min = models.PositiveSmallIntegerField('tiempo mínimo de desarrollo', blank=True, null=True)
    dev_max = models.PositiveSmallIntegerField('tiempo máximo de desarrollo', blank=True, null=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        :param constraints: Lista de restricciones de clase :class:`django.models.UniqueConstraint` para restricciones
            del modelo.
        """
        verbose_name = 'etapa del ticket'
        verbose_name_plural = 'etapas de los tickets'
        constraints = [
            models.UniqueConstraint(fields=['nombre', 'tipo', 'dificultad'], name='unique_etapa_tipo')
        ]

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre de la etapa del ticket, y su tipo si lo incluye.
        """
        return '{}{}{}'.format(
            self.nombre,
            f' - {self.tipo}' if self.tipo else "",
            f' - {self.dificultad}' if self.tipo else ""
        )


class ImagenTicket(models.Model):
    """
    El modelo ImagenTicket es una representación que conserva las imágenes adjuntas al modelo :class:`Ticket`.

    :param ticket: Clave foránea al modelo :class:`Ticket`.
    :param imagen: Campo especial para el guardado de imágenes. Incluye el detalle de usar el método
        :func:`get_image_ticket_path` para generar la ruta al archivo guardado.

    **Ejemplos de uso**

    Para su creación se necesita del campo :class:`Ticket` con entradas y se usan los siguientes pasos:

    *Creación de ImagenTicket*

    Ejemplo:
    ::
        # Valores de claves foráneas
        ticket_elegido = Ticket.objects.get(pk=1)

        # Creación de la nueva ImagenTicket
        nuevo_imagen_ticket = ImagenTicket.objects.create(
            ticket=ticket_elegido,
            imagen='pantalla1.jpg'
        )

    *Actualización del modelo ImagenTicket*

    Ejemplo:
    ::
        # Obtener ImagenTicket existente
        imagen_ticket_elegida = ImagenTicket.objects.get(pk=1)

        # Generar cambios a la imagen de ticket obtenida
        imagen_ticket_elegida.imagen = 'pantalla2.jpg'

        # Guardando cambios hechos
        imagen_ticket_elegida.save()

    """
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=get_image_ticket_path)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = 'imagen del ticket'
        verbose_name_plural = 'imágenes de los tickets'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con el ID y asunto del ticket, y la ruta de la imagen del ticket.
        """
        return f'{self.ticket.id} - {self.ticket.asunto[:50]} - {self.slice_path()}'

    def slice_path(self):
        return '..{}{}'.format(
            '\\' if self.imagen[-50:][0] != '\\' else '',
            self.imagen[-50:]
        )


class Mensaje(models.Model):
    """
    El modelo Mensaje es una representación de los mensajes que se asocian al :class:`Ticket`.

    :param ticket: Clave foránea al modelo :class:`Ticket`.
    :param asunto: Campo de texto con el asunto del mensaje (largo máximo: 100 caracteres).
    :param descripcion: Campo de texto con la descripción del mensaje.
    :param created: Campo de fecha y hora de la fecha de creación del colaborador (Auto generado).
    :param modified: Campo de fecha y hora de la última fecha de modificación del colaborador (Auto generado).

    **Ejemplos de uso**

    Para su creación se necesita del campo :class:`Ticket` con entradas y se usan los siguientes pasos:

    *Creación de Mensaje*

    Ejemplo:
    ::
        # Valores de claves foráneas
        ticket_elegido = Ticket.objects.get(pk=1)

        # Creación de la nueva Mensaje
        nuevo_mensaje = Mensaje.objects.create(
            ticket=ticket_elegido,
            asunto='Falta información'
            descripcion='Por favor llenar el error reportado'
        )

    *Actualización del modelo Mensaje*

    Ejemplo:
    ::
        # Obtener Mensaje existente
        mensaje_elegido = Mensaje.objects.get(pk=1)

        # Generar cambios al mensaje obtenido
        mensaje_elegido.asunto = 'Falta completar'

        # Guardando cambios hechos
        mensaje_elegido.save()

    """
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField('descripción')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con el ID del ticket y el asunto del mensaje.
        """
        return f'Ticket: {self.ticket.id} - Mensaje: {self.asunto}'


class ImagenMensaje(models.Model):
    """
    El modelo ImagenMensaje es una representación que conserva las imágenes adjuntas al modelo :class:`Mensaje`.

    :param mensaje: Clave foránea al modelo :class:`Mensaje`.
    :param imagen: Campo especial para el guardado de imágenes. Incluye el detalle de usar el método
        :func:`get_image_message_path` para generar la ruta al archivo guardado.

    **Ejemplos de uso**

    Para su creación se necesita del campo :class:`Mensaje` con entradas y se usan los siguientes pasos:

    *Creación de ImagenMensaje*

    Ejemplo:
    ::
        # Valores de claves foráneas
        mensaje_elegido = Mensaje.objects.get(pk=1)

        # Creación de la nueva ImagenMensaje
        nuevo_imagen_mensaje = ImagenMensaje.objects.create(
            mensaje=mensaje_elegido,
            imagen='pantalla1.jpg'
        )

    *Actualización del modelo ImagenMensaje*

    Ejemplo:
    ::
        # Obtener ImagenMensaje existente
        imagen_mensaje_elegida = ImagenMensaje.objects.get(pk=1)

        # Generar cambios a la imagen del mensaje obtenida
        imagen_mensaje_elegida.imagen = 'pantalla2.jpg'

        # Guardando cambios hechos
        imagen_mensaje_elegida.save()

    """
    mensaje = models.ForeignKey('Mensaje', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=get_image_message_path)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = 'imagen del mensaje'
        verbose_name_plural = 'imágenes de los mensajes'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con ID y asunto del mensaje, y la ruta de la imagen del mensaje.
        """
        return f'{self.mensaje.id} - {self.mensaje.asunto[:50]} - {self.slice_path()}'

    def slice_path(self):
        return '..{}{}'.format(
            '\\' if self.imagen[-50:][0] != '\\' else '',
            self.imagen[-50:]
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

    nombre = models.CharField(max_length=50, unique=True)
    nivel_severidad = models.CharField(max_length=50, choices=NivelSeveridad.choices, default=NivelSeveridad.INFO)
    tickets = models.ManyToManyField('Ticket', blank=True)
    mensajes = models.ManyToManyField('Mensaje', blank=True)

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
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name_plural = 'orígenes'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del origen.
        """
        return self.nombre
