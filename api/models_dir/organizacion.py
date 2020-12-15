from django.db import models


class DatosOrganizacionales(models.Model):
    """
    El modelo DatosOrganizacionales representa los datos en cuanto a organizacion de un :class:`Colaborador` a través
    del modelo :class:`DatosContractuales`. Por lo tanto este modelo está asociado a los modelos :class:`Cargo`,
    :class:`Unidad`, :class:`NivelResponsabilidad`, :class:`Colaborador` como jefe directo del colaborador y
    :class:`CentroCosto` para una mejor comprensión.

    :param datos_contractuales: Clave foránea al modelo :class:`DatosContractuales` (relación uno a uno).
    :param cargo: Clave foránea al modelo :class:`Cargo`
    :param unidad: Clave foránea al modelo :class:`Unidad`.
    :param nivel_responsabilidad: Clave foránea al modelo :class:`NivelResponsabilidad`.
    :param jefe_directo: Clave foránea al modelo :class:`Colaborador` (opcional).
    :param centro_costo: Clave foránea al modelo :class:`CentroCosto`.

    **Ejemplos de uso**

    Para su creación se necesita de los campos :class:`DatosContractuales`, :class:`Cargo`, :class:`Unidad`,
    :class:`NivelResponsabilidad` y :class:`CentroCosto` con datos en el sistema, y se usan los siguientes
    pasos:

    *Creación de DatosOrganizacionales*

    Ejemplo:
    ::
        # Valores de claves foráneas
        datos_contractuales_elegidos = DatosContractuales.objects.get(pk=1)
        cargo_elegido = Cargo.objects.get(pk=1)
        unidad_elegida = Unidad.objects.get(pk=1)
        nivel_responsabilidad_elegido = NivelResponsabilidad.objects.get(pk=1)
        centro_costo_elegido = CentroCosto.objects.get(pk=1)

        # Creación de la nueva DatosOrganizacionales
        nuevo_datos_organizacionales = DatosOrganizacionales.objects.create(
            datos_contractuales=datos_contractuales_elegidos,
            cargo=cargo_elegido,
            unidad=unidad_elegida,
            nivel_responsabilidad=nivel_responsabilidad_elegido,
            centro_costo=centro_costo_elegido
        )

    *Actualización del modelo DatosOrganizacionales*

    Ejemplo:
    ::
        # Obtener DatosOrganizacionales existentes
        datos_organizacionales_elegidos = DatosOrganizacionales.objects.get(pk=1)

        # Valores de claves foráneas a cambiar
        nueva_unidad = Unidad.objects.get(pk=999)

        # Generar cambios a los datos organizacionales obtenidos
        datos_organizacionales_elegidos.unidad = nueva_unidad

        # Guardando cambios hechos
        datos_organizacionales_elegidos.save()

    """
    datos_contractuales = models.OneToOneField('DatosContractuales', on_delete=models.CASCADE)
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
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name_plural = 'datos organizacionales'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre simple del colaborador, el nombre de su cargo, y el nombre de su unidad.
        """
        return '{} - {} - {}'.format(
            self.datos_contractuales.colaborador.simple_name(),
            self.cargo.nombre,
            self.unidad.nombre
        )


class Cargo(models.Model):
    """
    El modelo Cargo es una representación de los cargos que se pueden poseer en el modelo
    :class:`DatosOrganizacionales`, y también sirven como referencia para el modelo :class:`DatosActividad`.

    :param nombre: Campo de texto con el nombre del cargo (largo máximo: 50 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de Cargo*

    Ejemplo:
    ::
        # Creación del nuevo Cargo
        nuevo_cargo = Cargo.objects.create(
            nombre='Desarrollador'
        )

    *Actualización del modelo Cargo*

    Ejemplo:
    ::
        # Obtener Cargo existente
        cargo_elegido = Cargo.objects.get(pk=1)

        # Generar cambios al cargo obtenido
        cargo_elegido.nombre = 'Desarrollador senior'

        # Guardando cambios hechos
        cargo_elegido.save()

    """
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del cargo.
        """
        return self.nombre


class Unidad(models.Model):
    """
    El modelo Unidad es una representación de las unidades que se pueden poseer en el modelo
    :class:`DatosOrganizacionales`. Además esta relacionada con el modelo :class:`AreaFuncional` para una mejor
    representación.

    :param nombre: Campo de texto con el nombre de la unidad (largo máximo: 100 caracteres, único).
    :param area_funcional: Clave foránea al modelo :class:`AreaFuncional`.

    **Ejemplos de uso**

    Para su creación se necesita del campo :class:`AreaFuncional` con datos en el sistema y se usan los siguientes
    pasos:

    *Creación de Unidad*

    Ejemplo:
    ::
        # Valores de claves foráneas
        area_funcional_elegida = AreaFuncional.objects.get(pk=1)

        # Creación del nuevo Unidad
        nueva_unidad = Unidad.objects.create(
            nombre='Proyectos',
            area_funcional=area_funcional_elegida
        )

    *Actualización del modelo Unidad*

    Ejemplo:
    ::
        # Obtener Unidad existente
        unidad_elegido = Unidad.objects.get(pk=1)

        # Generar cambios a la unidad obtenida
        unidad_elegido.nombre = 'Desarrollo'

        # Guardando cambios hechos
        unidad_elegido.save()

    """
    nombre = models.CharField(max_length=100, unique=True)
    area_funcional = models.ForeignKey('AreaFuncional', on_delete=models.CASCADE, verbose_name='área funcional')

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name_plural = 'unidades'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre de la unidad.
        """
        return self.nombre


class AreaFuncional(models.Model):
    """
    El modelo AreaFuncional es una representación de las areas funcionales que se pueden poseer en el modelo
    :class:`Unidad`.

    :param nombre: Campo de texto con el nombre del área funcional (largo máximo: 100 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de AreaFuncional*

    Ejemplo:
    ::
        # Creación de la nueva AreaFuncional
        nueva_area_funcional = AreaFuncional.objects.create(
            nombre='Gerencia de operaciones'
        )

    *Actualización del modelo AreaFuncional*

    Ejemplo:
    ::
        # Obtener AreaFuncional existente
        area_funcional_elegida = AreaFuncional.objects.get(pk=1)

        # Generar cambios a el área funcional obtenido
        area_funcional_elegida.nombre = 'Gerencia General'

        # Guardando cambios hechos
        area_funcional_elegida.save()

    """
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = 'área funcional'
        verbose_name_plural = 'áreas funcionales'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del área funcional.
        """
        return self.nombre


class NivelResponsabilidad(models.Model):
    """
    El modelo NivelResponsabilidad es una representación de los niveles de responsabilidad que se pueden poseer en el
    modelo :class:`DatosOrganizacionales`.

    :param nombre: Campo de texto con el nombre del nivel de responsabilidad (largo máximo: 100 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de NivelResponsabilidad*

    Ejemplo:
    ::
        # Creación de la nueva NivelResponsabilidad
        nuevo_nivel_responsabilidad = NivelResponsabilidad.objects.create(
            nombre='Jefe'
        )

    *Actualización del modelo NivelResponsabilidad*

    Ejemplo:
    ::
        # Obtener NivelResponsabilidad existente
        nivel_responsabilidad_elegido = NivelResponsabilidad.objects.get(pk=1)

        # Generar cambios al nivel de responsabilidad obtenido
        nivel_responsabilidad_elegido.nombre = 'Gerente'

        # Guardando cambios hechos
        nivel_responsabilidad_elegido.save()

    """
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = 'nivel de responsabilidad'
        verbose_name_plural = 'niveles de responsabilidad'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del nivel de responsabilidad.
        """
        return self.nombre


class CentroCosto(models.Model):
    """
    El modelo CentroCosto es una representación de los centros de costo que se pueden poseer en el
    modelo :class:`DatosOrganizacionales`.

    :param nombre: Campo de texto con el nombre del centro de costo (largo máximo: 100 caracteres, único).

    **Ejemplos de uso**

    Para su creación se usan los siguientes pasos:

    *Creación de CentroCosto*

    Ejemplo:
    ::
        # Creación de la nueva CentroCosto
        nuevo_centro_costo = CentroCosto.objects.create(
            nombre='Oficina Recreo'
        )

    *Actualización del modelo CentroCosto*

    Ejemplo:
    ::
        # Obtener CentroCosto existente
        centro_costo_elegido = CentroCosto.objects.get(pk=1)

        # Generar cambios al centro de costo obtenido
        centro_costo_elegido.nombre = 'Casa Matriz'

        # Guardando cambios hechos
        centro_costo_elegido.save()

    """
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        """
        Clase meta encargada de la información general para el funcionamiento en Django.

        :param verbose_name: Cadena de texto con la version singular del nombre del objeto.
        :param verbose_name_plural: Cadena de texto con la versión en plural del nombre del objeto.
        """
        verbose_name = 'centro de costo'
        verbose_name_plural = 'centros de costos'

    def __str__(self):
        """
        Función que retorna una representación visual en cadena de texto para la llamada del modelo por algunas.
        funciones de Django.

        :return: Cadena de texto con nombre del centro de costo.
        """
        return self.nombre
