from rest_framework import serializers

from api import models


class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Actividad
        fields = '__all__'


class DatosActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatosActividad
        fields = '__all__'


class ProyectoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Proyecto
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cliente
        fields = '__all__'


class MesaAyudaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MesaAyuda
        fields = '__all__'


class TipoSoporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoSoporte
        fields = '__all__'


class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Modulo
        fields = '__all__'
