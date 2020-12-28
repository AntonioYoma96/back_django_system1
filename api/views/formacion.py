from rest_framework import viewsets

from api import serializers, models


class DatosFormacionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DatosFormacionSerializer
    queryset = models.DatosFormacion.objects.all()


class TipoFormacionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TipoFormacionSerializer
    queryset = models.TipoFormacion.objects.all()


class CarreraViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CarreraSerializer
    queryset = models.Carrera.objects.all()


class EstadoFormacionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EstadoFormacionSerializer
    queryset = models.EstadoFormacion.objects.all()


class InstitucionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.InstitucionSerializer
    queryset = models.Institucion.objects.all()


class TipoInstitucionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TipoInstitucionSerializer
    queryset = models.TipoInstitucion.objects.all()


class OtroFormacionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OtroFormacionSerializer
    queryset = models.OtroFormacion.objects.all()


class TipoOtroFormacionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TipoOtroFormacionSerializer
    queryset = models.TipoOtroFormacion.objects.all()


class DiplomaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DiplomaSerializer
    queryset = models.Diploma.objects.all()
