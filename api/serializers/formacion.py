from rest_framework import serializers

from api import models


class DatosFormacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatosFormacion
        fields = '__all__'


class TipoFormacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoFormacion
        fields = '__all__'


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Carrera
        fields = '__all__'


class EstadoFormacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EstadoFormacion
        fields = '__all__'


class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Institucion
        fields = '__all__'


class TipoInstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoInstitucion
        fields = '__all__'


class OtroFormacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OtroFormacion
        fields = '__all__'


class TipoOtroFormacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoOtroFormacion
        fields = '__all__'


class DiplomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Diploma
        fields = '__all__'
