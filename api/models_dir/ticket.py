import os
from datetime import datetime

from django.db import models


def get_image_ticket_path(instance, filename):
    ticket_path = f'ticket_{instance.ticket.id}'
    return new_filename(ticket_path, filename)


def get_image_message_path(instance, filename):
    ticket_path = f'mensaje_{instance.ticket.id}'
    return new_filename(ticket_path, filename)


def new_filename(ticket_path, file):
    today = datetime.now()
    root = 'image'
    filename = '{year}_{month}_{day}_{secs}.{extension}'.format(
        year=today.year,
        month=today.month,
        day=today.day,
        secs=today.microsecond,
        extension=file.split('.')[-1]
    )
    return os.path.join(root, ticket_path, filename)


class Ticket(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    asignado = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='ticket_asignado')
    solicitante = models.ForeignKey('Colaborador', on_delete=models.CASCADE, related_name='ticket_solicitado')
    validador = models.ForeignKey(
        'Colaborador',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='ticket_validar'
    )
    unidad = models.ForeignKey('Unidad', on_delete=models.CASCADE)
    # módulo
    version = models.CharField(max_length=10, blank=True, null=True)
    integracion = models.CharField('integración', max_length=50, blank=True, null=True)
    prioridad = models.ForeignKey('Prioridad', on_delete=models.CASCADE)
    tipo_ticket = models.ForeignKey('TipoTicket', on_delete=models.CASCADE, verbose_name='tipo de ticket')
    fecha_limite = models.DateField('fecha límite', blank=True, null=True)
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
    imagen = models.ImageField(upload_to=get_image_ticket_path)

    class Meta:
        verbose_name = 'imagen del ticket'
        verbose_name_plural = 'imágenes de los tickets'


class Mensaje(models.Model):
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    asunto = models.CharField(max_length=100)
    descripcion = models.TextField('descripción')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class ImagenMensaje(models.Model):
    mensaje = models.ForeignKey('Mensaje', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=get_image_message_path)

    class Meta:
        verbose_name = 'imagen del mensaje'
        verbose_name_plural = 'imágenes de los mensajes'


class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50, unique=50)
    tickets = models.ManyToManyField('Ticket')
    mensajes = models.ManyToManyField('Mensaje')
