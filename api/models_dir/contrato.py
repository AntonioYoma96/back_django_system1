from django.db import models


class DatosContractuales(models.Model):
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    fecha_inicio = models.DateField('fecha de inicio')
    fecha_termino = models.DateField('fecha de termino', blank=True, null=True)
    sueldo_base = models.PositiveIntegerField()
    tipo_contrato = models.ForeignKey('TipoContrato', on_delete=models.CASCADE, verbose_name='tipo de contrato')
    fecha_vencimiento = models.DateField('fecha de vencimiento', blank=True, null=True)
    prevision_afp = models.ForeignKey('PrevisionAfp', on_delete=models.CASCADE, verbose_name='previsión de AFP')
    prevision_salud = models.ForeignKey('PrevisionSalud', on_delete=models.CASCADE, verbose_name='previsión de salud')
    banco = models.ForeignKey('Banco', on_delete=models.CASCADE)
    tipo_cuenta = models.ForeignKey('TipoCuenta', on_delete=models.CASCADE, verbose_name='tipo de cuenta')
    numero_cuenta = models.CharField('número de cuenta', max_length=20)

    class Meta:
        verbose_name_plural = 'datos contractuales'

    def __str__(self):
        return '{} - desde {}{} - {}'.format(
            self.colaborador.full_name(),
            self.fecha_inicio.isoformat(),
            f' - hasta {self.fecha_termino}' if self.fecha_termino else '',
            self.tipo_contrato.nombre
        )


class TipoContrato(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tipo de contrato'
        verbose_name_plural = 'tipos de contrato'

    def __str__(self):
        return self.nombre


class PrevisionAfp(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'previsión de AFP'
        verbose_name_plural = 'previsiones de AFP'

    def __str__(self):
        return self.nombre


class PrevisionSalud(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'previsión de salud'
        verbose_name_plural = 'previsiones de salud'

    def __str__(self):
        return self.nombre


class Banco(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class TipoCuenta(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tipo de cuenta'
        verbose_name_plural = 'tipos de cuenta'

    def __str__(self):
        return self.nombre
