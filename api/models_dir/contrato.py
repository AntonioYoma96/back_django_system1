from django.db import models


class DatosContractuales(models.Model):
    """
    El modelo DatosContractuales es una representación de los datos asociados al contrato de un :class:`Colaborador`,
    que se puede usar como complemento de los datos de este colaborador. Además tiene asociaciones con
    :class:`TipoContrato`, :class:`PrevisionAfp`, :class:`PrevisionSalud`, :class:`Banco` y :class:`TipoCuenta`.

    :param colaborador: Clave foránea al modelo :class:`Colaborador`.
    :param fecha_inicio: Campo de fecha para la fecha de inicio del contrato.
    :param fecha_termino: Campo de fecha para la fecha de término del contrato (opcional).
    :param sueldo_base: Campo numérico positivo para el registro del sueldo base en el contrato (opcional).
    :param tipo_contrato: Clave foránea al modelo :class:`TipoContrato`.
    :param fecha_vencimiento: Campo de fecha para la fecha de vencimiento del contrato (no confundir con la fecha de
        término) (opcional).
    :param prevision_afp: Clave foránea al modelo :class:`PrevisionAfp`.
    :param prevision_salud: Clave foránea al modelo :class:`PrevisionSalud`.
    :param banco: Clave foránea al modelo :class:`PrevisionBanco` (opcional).
    :param tipo_cuenta: Clave foránea al modelo :class:`TipoCuenta` (opcional).
    :param numero_cuenta: Campo de texto con el número de cuenta para efectos de pago al colaborador asociado
        (opcional).

    **Ejemplos de uso**

    Para su creación se necesita de los campos :class:`Colaborador`, :class:`TipoContrato`, :class:`PrevisionAfp`,
    :class:`PrevisionSalud`, :class:`Banco` y :class:`TipoCuenta` con datos en el sistema, y se usan los siguientes
    pasos:

    *Creación de DatosContractuales*

    Ejemplo:
    ::
        # Librería para la carga de fechas
        import datetime

        # Valores de claves foráneas
        colaborador_elegido = Colaborador.objects.get(pk=1)
        tipo_contrato_elegido = TipoContrato.objects.get(pk=1)
        prevision_afp_elegida = PrevisionAfp.objects.get(pk=1)
        prevision_salud_elegida = PrevisionSalud.objects.get(pk=1)

        # Creación de la nueva DatosContractuales
        nuevo_datos_contractuales = DatosContractuales.objects.create(
            colaborador=colaborador_elegido,
            fecha_inicio=datetime.date(2020, 1, 1),
            tipo_contrato=tipo_contrato_elegido,
            prevision_afp=prevision_afp_elegida,
            prevision_salud=prevision_salud_elegida
        )

    *Actualización del modelo DatosContractuales*

    Ejemplo:
    ::
        # Obtener DatosContractuales existentes
        datos_contractuales_elegidos = DatosContractuales.objects.get(pk=1)

        # Generar cambios a los datos contractuales obtenidos
        datos_contractuales_elegidos.fecha_termino = datetime.date(2020, 6, 1)

        # Guardando cambios hechos
        datos_contractuales_elegidos.save()

    """
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    fecha_inicio = models.DateField('fecha de inicio')
    fecha_termino = models.DateField('fecha de termino', blank=True, null=True)
    sueldo_base = models.PositiveIntegerField(blank=True, null=True)
    tipo_contrato = models.ForeignKey('TipoContrato', on_delete=models.CASCADE, verbose_name='tipo de contrato')
    fecha_vencimiento = models.DateField('fecha de vencimiento', blank=True, null=True)
    prevision_afp = models.ForeignKey('PrevisionAfp', on_delete=models.CASCADE, verbose_name='previsión de AFP')
    prevision_salud = models.ForeignKey('PrevisionSalud', on_delete=models.CASCADE, verbose_name='previsión de salud')
    banco = models.ForeignKey('Banco', on_delete=models.CASCADE, blank=True, null=True)
    tipo_cuenta = models.ForeignKey(
        'TipoCuenta',
        on_delete=models.CASCADE,
        verbose_name='tipo de cuenta',
        blank=True, null=True
    )
    numero_cuenta = models.CharField('número de cuenta', max_length=20, blank=True, null=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name_plural = 'datos contractuales'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre simple del colaborador, fecha de inicio y término de contrato (si existe) y
            nombre del tipo de contrato.
        """
        return '{} - desde {}{} - {}'.format(
            self.colaborador.simple_name(),
            self.fecha_inicio.isoformat(),
            f' - hasta {self.fecha_termino}' if self.fecha_termino else '',
            self.tipo_contrato.nombre
        )


class TipoContrato(models.Model):
    """
    El modelo TipoContrato es una representación de los tipos de contrato que puede existir en el modelo
    :class:`DatosContractuales`.

    :param nombre: Campo de texto con el nombre del tipo de contrato (largo máximo: 50 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de TipoContrato*

    Ejemplo:
    ::
        # Creación de la nueva TipoContrato
        nuevo_tipo_contrato = TipoContrato.objects.create(
            nombre='Fijo'
        )

    *Actualización del modelo TipoContrato*

    Ejemplo:
    ::
        # Obtener TipoContrato existentes
        tipo_contrato_elegido = TipoContrato.objects.get(pk=1)

        # Generar cambios al tipo de contrato obtenido
        tipo_contrato_elegido.nombre = 'de Honorarios'

        # Guardando cambios hechos
        tipo_contrato_elegido.save()

    """
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = 'tipo de contrato'
        verbose_name_plural = 'tipos de contrato'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del tipo de contrato.
        """
        return self.nombre


class PrevisionAfp(models.Model):
    """
    El modelo PrevisionAfp es una representación de las AFP que se pueden poseer en el modelo
    :class:`DatosContractuales`.

    :param nombre: Campo de texto con el nombre de la AFP (largo máximo: 50 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de PrevisionAfp*

    Ejemplo:
    ::
        # Creación de la nueva PrevisionAfp
        nuevo_prevision_afp = PrevisionAfp.objects.create(
            nombre='ProVida'
        )

    *Actualización del modelo PrevisionAfp*

    Ejemplo:
    ::
        # Obtener PrevisionAfp existente
        prevision_afp_elegida = PrevisionAfp.objects.get(pk=1)

        # Generar cambios a la previsión de afp obtenida
        prevision_afp_elegida.nombre = 'Capital'

        # Guardando cambios hechos
        prevision_afp_elegida.save()

    """
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = 'previsión de AFP'
        verbose_name_plural = 'previsiones de AFP'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre de la previsión de afp.
        """
        return self.nombre


class PrevisionSalud(models.Model):
    """
    El modelo PrevisionSalud es una representación de los nombres de previsión de salud que se pueden poseer en el
    modelo :class:`DatosContractuales`.

    :param nombre: Campo de texto con el nombre de la previsión de salud (largo máximo: 50 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de PrevisionSalud*

    Ejemplo:
    ::
        # Creación de la nueva PrevisionSalud
        nuevo_prevision_salud = PrevisionSalud.objects.create(
            nombre='Fonasa'
        )

    *Actualización del modelo PrevisionSalud*

    Ejemplo:
    ::
        # Obtener PrevisionSalud existente
        prevision_salud_elegida = PrevisionSalud.objects.get(pk=1)

        # Generar cambios a la previsión de salud obtenida
        prevision_salud_elegida.nombre = 'Isapre Banmédica'

        # Guardando cambios hechos
        prevision_salud_elegida.save()

    """
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = 'previsión de salud'
        verbose_name_plural = 'previsiones de salud'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre de la previsión de salud.
        """
        return self.nombre


class Banco(models.Model):
    """
    El modelo Banco es una representación de los nombres de bancos que se pueden poseer en el modelo
    :class:`DatosContractuales`.

    :param nombre: Campo de texto con el nombre del banco (largo máximo: 100 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de Banco*

    Ejemplo:
    ::
        # Creación del nuevo Banco
        nuevo_banco = Banco.objects.create(
            nombre='Banco Estado'
        )

    *Actualización del modelo Banco*

    Ejemplo:
    ::
        # Obtener Banco existente
        banco_elegido = Banco.objects.get(pk=1)

        # Generar cambios al banco obtenido
        banco_elegido.nombre = 'Banco de Chile'

        # Guardando cambios hechos
        banco_elegido.save()

    """
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del banco.
        """
        return self.nombre


class TipoCuenta(models.Model):
    """
    El modelo TipoCuenta es una representación de los tipos de cuenta que se pueden poseer en el modelo
    :class:`DatosContractuales`.

    :param nombre: Campo de texto con el nombre de tipo de cuenta (largo máximo: 100 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de TipoCuenta*

    Ejemplo:
    ::
        # Creación del nuevo TipoCuenta
        nuevo_tipo_cuenta = TipoCuenta.objects.create(
            nombre='Cuenta RUT'
        )

    *Actualización del modelo TipoCuenta*

    Ejemplo:
    ::
        # Obtener TipoCuenta existente
        tipo_cuenta_elegido = TipoCuenta.objects.get(pk=1)

        # Generar cambios al tipo de cuenta obtenido
        tipo_cuenta_elegido.nombre = 'Cuenta corriente'

        # Guardando cambios hechos
        tipo_cuenta_elegido.save()

    """
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = 'tipo de cuenta'
        verbose_name_plural = 'tipos de cuenta'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del tipo de cuenta.
        """
        return self.nombre
