from rest_framework import serializers

from api import models
from api.serializers import ColaboradorSerializer, ModuloSerializer


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

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['area_ticket'] = AreaTicketSerializer(instance.area_ticket).data
        return response


class ArchivoTicketSerializer(serializers.ModelSerializer):
    archivo = serializers.FileField()

    class Meta:
        model = models.ArchivoTicket
        fields = '__all__'


class MensajeSerializer(serializers.ModelSerializer):
    autor = serializers.PrimaryKeyRelatedField(queryset=models.Colaborador.objects.all(), required=False,
                                               allow_null=True)

    class Meta:
        model = models.Mensaje
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['autor'] = ColaboradorSerializer(instance.autor).data
        return response


class ArchivoMensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArchivoMensaje
        fields = '__all__'


class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Etiqueta
        fields = '__all__'


class OrigenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Origen
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['asignado'] = ColaboradorSerializer(instance.asignado).data
        response['solicitante'] = ColaboradorSerializer(instance.solicitante).data
        if instance.validador:
            response['validador'] = ColaboradorSerializer(instance.validador).data
        response['origen'] = OrigenSerializer(instance.origen).data
        response['modulo'] = ModuloSerializer(instance.modulo).data
        response['prioridad'] = PrioridadSerializer(instance.prioridad).data
        response['tipo_ticket'] = TipoTicketSerializer(instance.tipo_ticket).data
        response['etapa_ticket'] = EtapaTicketSerializer(instance.etapa_ticket).data
        if instance.dificultad_ticket:
            response['dificultad_ticket'] = DificultadTicketSerializer(instance.dificultad_ticket).data
        return response
