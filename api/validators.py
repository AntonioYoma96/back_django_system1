from itertools import cycle

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_run(valor):
    """
    Método para validar RUN chileno

    Este método está basado en el código de esta `fuente
    <https://www.lawebdelprogramador.com/codigo/Python/3532-Valida-Rut-Chile.html>`_.

    :param valor: El valor de entrada sin formatear
    :raise Error de validación a causa de un RUN mal digitado
    """
    estandarizado = valor.upper()
    if estandarizado.find('-') != -1 or estandarizado.find('.') != -1:
        raise ValidationError(
            _('El valor %(run)s incluye puntos y/o guion'),
            params={'run': estandarizado}
        )

    correlativo = estandarizado[:-1]
    verificador = estandarizado[-1:]
    if not correlativo.isnumeric():
        raise ValidationError(
            _('Los dígitos para el valor %(dig)s están en un formato inválido'),
            params={'dig': correlativo}
        )
    if not (verificador.isnumeric() or verificador == 'K'):
        raise ValidationError(
            _('El valor %(ver)s no corresponde a un dígito verificador'),
            params={'ver': verificador}
        )

    revertido = map(int, reversed(str(correlativo)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factors))
    res = (-s) % 11

    if not (str(res) == verificador or (verificador == 'K' and res == 10)):
        raise ValidationError(
            _('%(run)s no es un identificador válido'),
            params={'run': estandarizado}
        )
