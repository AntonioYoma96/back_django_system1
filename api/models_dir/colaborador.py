from django.contrib.auth import get_user_model
from django.db import models

from api.validators import validate_run


class Colaborador(models.Model):
    usuario = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    run = models.CharField('RUN', max_length=11, unique=True, validators=[validate_run])
    nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField('fecha de nacimiento')
    fecha_defuncion = models.DateField('fecha de defunción', blank=True, null=True)
    sexo = models.ForeignKey('Sexo', on_delete=models.CASCADE)
    estado_civil = models.ForeignKey('EstadoCivil', on_delete=models.CASCADE)
    nacionalidad = models.ForeignKey('Nacionalidad', on_delete=models.CASCADE)
    direccion = models.CharField('dirección', max_length=200, blank=True, null=True)
    comuna = models.ForeignKey('Comuna', on_delete=models.CASCADE)
    telefono_fijo = models.CharField('teléfono fijo', max_length=20, blank=True, null=True)
    telefono_movil = models.CharField('teléfono móvil', max_length=20, blank=True, null=True)
    email_personal = models.EmailField()

    class Meta:
        verbose_name_plural = 'colaboradores'

    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'

    def full_name(self):
        return f'{self.nombre} {self.apellido_paterno}'


class Sexo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class EstadoCivil(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'estados civiles'

    def __str__(self):
        return self.nombre


class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'nacionalidades'

    def __str__(self):
        return self.nombre


class Comuna(models.Model):
    codigo = models.CharField('código', max_length=5, unique=True)
    nombre = models.CharField(max_length=50, unique=True)
    provincia = models.ForeignKey('Provincia', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Provincia(models.Model):
    codigo = models.CharField('código', max_length=5, unique=True)
    nombre = models.CharField(max_length=50, unique=True)
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name='región')

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Region(models.Model):
    codigo = models.CharField('código', max_length=5, unique=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'región'
        verbose_name_plural = 'regiones'

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Hijo(models.Model):
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True, null=False)
    RUN = models.CharField('RUN', max_length=100, unique=True, validators=[validate_run])
    fecha_nacimiento = models.DateField('fecha de nacimiento')

    def __str__(self):
        return f'{self.nombres.split(" ", 1)[0]} {self.apellido_paterno}'


class PersonaContacto(models.Model):
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField('teléfono', max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'persona de contacto'
        verbose_name_plural = 'personas de contacto'

    def __str__(self):
        return f'{self.nombres.split(" ", 1)[0]} {self.apellido_paterno}'


class ColaboradorSkill(models.Model):
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    nivel_skill = models.ForeignKey('NivelSkill', on_delete=models.CASCADE, verbose_name='nivel de skill')

    class Meta:
        verbose_name = 'skill del colaborador'
        verbose_name_plural = 'skills del colaborador'

    def __str__(self):
        return '{} {} - {} - {}'.format(
            self.colaborador.nombre,
            self.colaborador.apellido_paterno,
            self.skill.nombre,
            self.nivel_skill.nombre,
        )


class Skill(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class NivelSkill(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'nivel de skill'
        verbose_name_plural = 'niveles de skill'

    def __str__(self):
        return self.nombre
