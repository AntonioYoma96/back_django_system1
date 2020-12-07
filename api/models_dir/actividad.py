from django.db import models


class Actividad(models.Model):
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField('hora de inicio')
    hora_termino = models.TimeField('hora de término', blank=True, null=True)
    datos_actividad = models.ForeignKey('DatosActividad', on_delete=models.CASCADE, verbose_name='datos de actividad')
    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    created = models.DateTimeField('creado', auto_now_add=True)
    modified = models.DateTimeField('modificado', auto_now=True)

    class Meta:
        verbose_name_plural = 'actividades'

    def __str__(self):
        return '{} - desde {}{} - {}'.format(
            self.datos_actividad.nombre,
            self.hora_inicio.isoformat(),
            f' hasta {self.hora_termino.isoformat()}' if self.hora_termino else '',
            self.fecha.isoformat()
        )


class DatosActividad(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField('descripción', blank=True, null=True)
    tiempo_maximo = models.SmallIntegerField('tiempo máximo', blank=True, null=True)
    tiempo_minimo = models.SmallIntegerField('tiempo mínimo', blank=True, null=True)
    cargo = models.ForeignKey('Cargo', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'datos de actividad'
        verbose_name_plural = 'datos de actividades'

    def __str__(self):
        return f'{self.nombre} - {self.cargo.nombre}'


class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    repositorio = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.nombre} - {self.cliente.nombre}'


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class MesaAyuda(models.Model):
    actividad = models.ForeignKey('Actividad', on_delete=models.CASCADE)
    tipo_soporte = models.ForeignKey('TipoSoporte', on_delete=models.CASCADE)
    modulo = models.ForeignKey('Modulo', on_delete=models.CASCADE, verbose_name='módulo')
    funcionario = models.CharField(max_length=200)
    telefono = models.CharField('teléfono', max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_habil = models.BooleanField('horario hábil')
    created = models.DateTimeField('creado', auto_now_add=True)
    modified = models.DateTimeField('modificado', auto_now=True)

    class Meta:
        verbose_name = 'atención de mesa de ayuda'
        verbose_name_plural = 'atenciones de mesa de ayuda'

    def __str__(self):
        return f'{self.tipo_soporte.nombre} - {self.modulo.nombre} - ¿hábil?: {"Si" if self.is_habil else "No"}'


class TipoSoporte(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tipo de soporte'
        verbose_name_plural = 'tipos de soportes'

    def __str__(self):
        return self.nombre


class Modulo(models.Model):
    nombre = models.CharField(max_length=100)
    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'módulo'

    def __str__(self):
        return f'{self.nombre} - {self.proyecto.nombre} - {self.proyecto.cliente.nombre}'
