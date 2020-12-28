from rest_framework import viewsets

from api import serializers, models


class ActividadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ActividadSerializer
    queryset = models.Actividad.objects.all()


class DatosActividadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DatosActividadSerializer
    queryset = models.DatosActividad.objects.all()


class ProyectoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProyectoSerializer
    queryset = models.Proyecto.objects.all()


class ClienteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ClienteSerializer
    queryset = models.Cliente.objects.all()


class MesaAyudaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MesaAyudaSerializer
    queryset = models.MesaAyuda.objects.all()


class TipoSoporteViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TipoSoporteSerializer
    queryset = models.TipoSoporte.objects.all()


class ModuloViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ModuloSerializer
    queryset = models.Modulo.objects.all()
