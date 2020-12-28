from rest_framework import serializers

from api import models


class DatosOrganizacionalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatosOrganizacionales
        fields = '__all__'


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cargo
        fields = '__all__'


class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unidad
        fields = '__all__'


class AreaFuncionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AreaFuncional
        fields = '__all__'


class NivelResponsabilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NivelResponsabilidad
        fields = '__all__'


class CentroCostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CentroCosto
        fields = '__all__'
