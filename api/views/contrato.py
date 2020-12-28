from rest_framework import viewsets

from api import serializers, models


class DatosContractualesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DatosContractualesSerializer
    queryset = models.DatosContractuales.objects.all()


class TipoContratoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TipoContratoSerializer
    queryset = models.TipoContrato.objects.all()


class PrevisionAfpViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PrevisionAfpSerializer
    queryset = models.PrevisionAfp.objects.all()


class PrevisionSaludViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PrevisionSaludSerializer
    queryset = models.PrevisionSalud.objects.all()


class BancoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BancoSerializer
    queryset = models.Banco.objects.all()


class TipoCuentaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TipoCuentaSerializer
    queryset = models.TipoCuenta.objects.all()