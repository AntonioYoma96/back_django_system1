from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers, models


class ColaboradorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ColaboradorSerializer
    queryset = models.Colaborador.objects.all()


class SexoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SexoSerializer
    queryset = models.Sexo.objects.all()


class EstadoCivilViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EstadoCivilSerializer
    queryset = models.EstadoCivil.objects.all()


class NacionalidadViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NacionalidadSerializer
    queryset = models.Nacionalidad.objects.all()


class ComunaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ComunaSerializer
    queryset = models.Comuna.objects.all()


class ProvinciaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProvinciaSerializer
    queryset = models.Provincia.objects.all()


class RegionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RegionSerializer
    queryset = models.Region.objects.all()


class HijoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HijoSerializer
    queryset = models.Hijo.objects.all()


class PersonaContactoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PersonaContactoSerializer
    queryset = models.PersonaContacto.objects.all()


class ColaboradorSkillViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ColaboradorSkillSerializer
    queryset = models.ColaboradorSkill.objects.all()


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SkillSerializer
    queryset = models.Skill.objects.all()


class NivelSkillViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NivelSkillSerializer
    queryset = models.NivelSkill.objects.all()
