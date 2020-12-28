from rest_framework import serializers

from api import models


class DatosContractualesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DatosContractuales
        fields = '__all__'


class TipoContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoContrato
        fields = '__all__'


class PrevisionAfpSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrevisionAfp
        fields = '__all__'


class PrevisionSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PrevisionSalud
        fields = '__all__'


class BancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banco
        fields = '__all__'


class TipoCuentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TipoCuenta
        fields = '__all__'
