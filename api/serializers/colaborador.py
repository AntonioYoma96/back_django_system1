from rest_framework import serializers

from api import models


class ColaboradorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = models.Colaborador
        fields = [
            "id",
            "run",
            "nombre",
            "segundo_nombre",
            "apellido_paterno",
            "apellido_materno",
            "fecha_nacimiento",
            "fecha_defuncion",
            "direccion",
            "telefono_fijo",
            "telefono_movil",
            "email_personal",
            "fecha_ingreso",
            "created",
            "modified",
            "usuario",
            "sexo",
            "estado_civil",
            "nacionalidad",
            "comuna",
            "full_name"
        ]


class SexoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sexo
        fields = '__all__'


class EstadoCivilSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EstadoCivil
        fields = '__all__'


class NacionalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nacionalidad
        fields = '__all__'


class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comuna
        fields = '__all__'


class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Provincia
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = '__all__'


class HijoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hijo
        fields = '__all__'


class PersonaContactoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PersonaContacto
        fields = '__all__'


class ColaboradorSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ColaboradorSkill
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Skill
        fields = '__all__'


class NivelSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NivelSkill
        fields = '__all__'
