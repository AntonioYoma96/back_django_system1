from rest_framework import serializers

from api import models


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = '__all__'


class TicketLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketLog
        fields = '__all__'


class PrioridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Prioridad
        fields = '__all__'


class TipoTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoTicket
        fields = '__all__'


class EtapaTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EtapaTicket
        fields = '__all__'


class AreaTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AreaTicket
        fields = '__all__'


class DificultadTicketSerializer(serializers.ModelSerializer):
    full_dificultad = serializers.ReadOnlyField()

    class Meta:
        model = models.DificultadTicket
        fields = [
            'id',
            'tipo',
            'nivel',
            'rev_min',
            'rev_max',
            'dev_min',
            'dev_max',
            'area_ticket',
            'full_dificultad',
        ]


class ImagenTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImagenTicket
        fields = '__all__'


class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Mensaje
        fields = '__all__'


class ImagenMensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ImagenMensaje
        fields = '__all__'


class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Etiqueta
        fields = '__all__'


class OrigenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Origen
        fields = '__all__'
