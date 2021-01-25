from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from api import serializers, models


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TicketSerializer
    queryset = models.Ticket.objects.all()


class TicketLogViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TicketLogSerializer
    queryset = models.TicketLog.objects.all()


class PrioridadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PrioridadSerializer
    queryset = models.Prioridad.objects.all()


class TipoTicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TipoTicketSerializer
    queryset = models.TipoTicket.objects.all()


class EtapaTicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EtapaTicketSerializer
    queryset = models.EtapaTicket.objects.all()


class AreaTicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AreaTicketSerializer
    queryset = models.AreaTicket.objects.all()


class DificultadTicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DificultadTicketSerializer
    queryset = models.DificultadTicket.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['area_ticket']


class ImagenTicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImagenTicketSerializer
    queryset = models.ImagenTicket.objects.all()


class MensajeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MensajeSerializer
    queryset = models.Mensaje.objects.all()


class ImagenMensajeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImagenMensajeSerializer
    queryset = models.ImagenMensaje.objects.all()


class EtiquetaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EtiquetaSerializer
    queryset = models.Etiqueta.objects.all()


class OrigenViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrigenSerializer
    queryset = models.Origen.objects.all()
