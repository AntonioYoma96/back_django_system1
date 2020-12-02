from django.db import models


class Actividad(models.Model):
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField('hora de inicio')
    hora_termino = models.TimeField('hora de término')
    datos_actividad = models.ForeignKey('DatosActividad', on_delete=models.CASCADE, verbose_name='datos de actividad')
    proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    created = models.DateTimeField('creado', auto_now_add=True)
    modified = models.DateTimeField('modificado', auto_now=True)

    class Meta:
        verbose_name_plural = 'actividades'

    def __str__(self):
        return '{} - desde {} hasta {} - {}'.format(
            self.datos_actividad.nombre,
            self.hora_inicio.isoformat(),
            self.hora_termino.isoformat(),
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

    def __str__(self):
        return f'{self.nombre} - {self.cliente.nombre}'


class Cliente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre
