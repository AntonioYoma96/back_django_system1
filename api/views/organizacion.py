from rest_framework import viewsets

from api import serializers, models


class DatosOrganizacionalesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DatosOrganizacionalesSerializer
    queryset = models.DatosOrganizacionales.objects.all()


class CargoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CargoSerializer
    queryset = models.Cargo.objects.all()


class UnidadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UnidadSerializer
    queryset = models.Unidad.objects.all()


class AreaFuncionalViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AreaFuncionalSerializer
    queryset = models.AreaFuncional.objects.all()


class NivelResponsabilidadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NivelResponsabilidadSerializer
    queryset = models.NivelResponsabilidad.objects.all()


class CentroCostoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CentroCostoSerializer
    queryset = models.CentroCosto.objects.all()
