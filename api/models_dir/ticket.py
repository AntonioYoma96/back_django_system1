from django.db import models


class Ticket(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    asignado = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    solicitante = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    unidad = models.ForeignKey('Unidad', on_delete=models.CASCADE)
    validador = models.ForeignKey('Colaborador', on_delete=models.CASCADE, blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    # módulo
    integracion = models.CharField('integración', max_length=50, blank=True, null=True)
    prioridad = models.ForeignKey('Prioridad', on_delete=models.CASCADE)
    tipo_ticket = models.ForeignKey('TipoTicket', on_delete=models.CASCADE, verbose_name='tipo de ticket')
    fecha_limite = models.DateField('fecha límite', blank=True, null=True)
    puntos = models.PositiveSmallIntegerField(blank=True, null=True)
    esperar_definicion_referencia = models.BooleanField('esperar definición de referencia', blank=True, null=True)
    is_errror_usuario = models.BooleanField('error de usuario')
    is_tarea_bloque = models.BooleanField('tarea de bloque')
    ruta = models.URLField(blank=True, null=True)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField('descripción')
    estado_ticket = models.ForeignKey('EstadoTicket', on_delete=models.CASCADE, verbose_name='estado del ticket')
    created = models.DateTimeField('creado', auto_now_add=True)
    modified = models.DateTimeField('modificado', auto_now=True)


class Prioridad(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    valor = models.SmallIntegerField(unique=True)

    class Meta:
        verbose_name_plural = 'prioridades'


class TipoTicket(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'tipo de ticket'
        verbose_name_plural = 'tipos de ticket'


class EstadoTicket(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'estado del ticket'
        verbose_name_plural = 'estados del ticket'


class ImagenTicket(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=f'tickets/{ticket.id}/%Y%m%d/')

    class Meta:
        verbose_name = 'imagen del ticket'
        verbose_name_plural = 'imágenes de los tickets'


class Mensaje(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField('descripción')
    is_error_usuario = models.BooleanField('error de usuario')
    is_tarea_bloque = models.BooleanField('tarea de bloque')
    is_falta_informacion = models.BooleanField('falta de información')
    is_mejorar_redaccion = models.BooleanField('mejorar redacción')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class ImagenMensaje(models.Model):
    mensaje = models.ForeignKey('Mensaje', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=f'tickets/{mensaje.id}/%Y%m%d/')

    class Meta:
        verbose_name = 'imagen del mensaje'
        verbose_name_plural = 'imágenes de los mensajes'
