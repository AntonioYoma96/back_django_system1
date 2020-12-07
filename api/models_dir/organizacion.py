from django.db import models


class DatosOrganizacionales(models.Model):
    datos_contractuales = models.OneToOneField('DatosContractuales', on_delete=models.CASCADE)
    # empleador = models.ForeignKey('Empleador', on_delete=models.CASCADE)
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    unidad = models.ForeignKey('Unidad', on_delete=models.CASCADE)
    nivel_responsabilidad = models.ForeignKey(
        'NivelResponsabilidad',
        on_delete=models.CASCADE,
        verbose_name='nivel de responsabilidad'
    )
    jefe_directo = models.ForeignKey(
        'Colaborador',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='datos_subordinado'
    )
    centro_costo = models.ForeignKey(
        'CentroCosto',
        on_delete=models.CASCADE,
        verbose_name='centro de costo'
    )

    class Meta:
        verbose_name_plural = 'datos organizacionales'

    def __str__(self):
        return '{} - {} - {}'.format(
            self.datos_contractuales.colaborador.full_name(),
            self.cargo.nombre,
            self.unidad.nombre
        )


# class Empleador(models.Model):
#     rut = models.CharField('RUT', max_length=11, unique=True, validators=[validate_run])
#     razon_social = models.CharField('razón social', max_length=100)
#
#     class Meta:
#         verbose_name_plural = 'empleadores'
#
#     def __str__(self):
#         return self.razon_social


class Cargo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Unidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    area_funcional = models.ForeignKey('AreaFuncional', on_delete=models.CASCADE, verbose_name='área funcional')

    class Meta:
        verbose_name_plural = 'unidades'

    def __str__(self):
        return self.nombre


class AreaFuncional(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'área funcional'
        verbose_name_plural = 'áreas funcionales'

    def __str__(self):
        return self.nombre


class NivelResponsabilidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'nivel de responsabilidad'
        verbose_name_plural = 'niveles de responsabilidad'

    def __str__(self):
        return self.nombre


class CentroCosto(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'centro de costo'
        verbose_name_plural = 'centros de costos'

    def __str__(self):
        return self.nombre
