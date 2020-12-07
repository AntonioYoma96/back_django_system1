from django.core.validators import MinValueValidator
from django.db import models


class DatosFormacion(models.Model):
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    tipo_formacion = models.ForeignKey('TipoFormacion', on_delete=models.CASCADE, verbose_name='tipo de formación')
    carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)
    estado_formacion = models.ForeignKey(
        'EstadoFormacion',
        on_delete=models.CASCADE,
        verbose_name='estado de formación'
    )
    fecha_termino = models.DateField('fecha de término')
    institucion = models.ForeignKey('Institucion', on_delete=models.CASCADE, verbose_name='institución')

    class Meta:
        verbose_name = 'datos de formación'
        verbose_name_plural = 'datos de formaciones'

    def __str__(self):
        return f'{self.carrera.nombre} - {self.estado_formacion.nombre}'


class TipoFormacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tipo de formación'
        verbose_name_plural = 'tipos de formación'

    def __str__(self):
        return self.nombre


class Carrera(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class EstadoFormacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'estado de formación'
        verbose_name_plural = 'estados de formación'

    def __str__(self):
        return self.nombre


class Institucion(models.Model):
    tipo_institucion = models.ForeignKey(
        'TipoInstitucion',
        on_delete=models.CASCADE,
        verbose_name='tipo de institución'
    )
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'institución'
        verbose_name_plural = 'instituciones'

    def __str__(self):
        return self.nombre


class TipoInstitucion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tipo de institución'
        verbose_name_plural = 'tipos de instituciones'

    def __str__(self):
        return self.nombre


class OtroFormacion(models.Model):
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    institucion = models.ForeignKey('Institucion', on_delete=models.CASCADE, verbose_name='institución')
    tipo_otra_formacion = models.ForeignKey(
        'TipoOtroFormacion',
        on_delete=models.CASCADE,
        verbose_name='tipo otro de formación'
    )
    diploma = models.ForeignKey('Diploma', on_delete=models.CASCADE)
    horas = models.DecimalField(max_digits=6, decimal_places=1, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f'{self.diploma.nombre} - {self.horas} hora{"s" if self.horas != 1.0 else ""}'


class TipoOtroFormacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tipo otro de formación'
        verbose_name_plural = 'tipos otros de formación'

    def __str__(self):
        return self.nombre


class Diploma(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
