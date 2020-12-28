from rest_framework import viewsets

from api import serializers, models


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TicketSerializer
    queryset = models.Ticket.objects.all()


class PrioridadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PrioridadSerializer
    queryset = models.Prioridad.objects.all()


class TipoTicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TipoTicketSerializer
    queryset = models.TipoTicket.objects.all()


class EtapaTicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EtapaTicketSerializer
    queryset = models.EtapaTicket.objects.all()


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
