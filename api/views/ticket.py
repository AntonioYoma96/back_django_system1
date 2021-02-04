from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

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


class ArchivoTicketViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ArchivoTicketSerializer
    queryset = models.ArchivoTicket.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MensajeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MensajeSerializer
    queryset = models.Mensaje.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['ticket']
    ordering_fields = ['created']

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'autor' in data:
            if not data['autor']:
                data['autor'] = request.user.colaborador.id
        else:
            data['autor'] = request.user.colaborador.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArchivoMensajeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ArchivoMensajeSerializer
    queryset = models.ArchivoMensaje.objects.all()


class EtiquetaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EtiquetaSerializer
    queryset = models.Etiqueta.objects.all()


class OrigenViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrigenSerializer
    queryset = models.Origen.objects.all()
