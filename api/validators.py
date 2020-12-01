from itertools import cycle

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_run(value):
    value = value.upper()
    value = value.replace('-', '')
    value = value.replace('.', '')
    cuerpo = value[:-1]
    dv = value[-1:]

    revertido = map(int, reversed(str(cuerpo)))
    factores = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(revertido, factores))
    res = (-s) % 11

    if not (str(res) == dv or (dv == 'K' and res == 10)):
        raise ValidationError(_('%(value)s is not valid'), params={'value': value})
