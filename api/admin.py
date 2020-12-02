from django.contrib import admin

from api.models_dir import *

lista_modelos = [
    # Colaborador
    Colaborador,
    Sexo,
    EstadoCivil,
    Nacionalidad,
    Comuna,
    Provincia,
    Region,
    Hijo,
    PersonaContacto,
    ColaboradorSkill,
    Skill,
    NivelSkill,
    # Contrato
    DatosContractuales,
    TipoContrato,
    PrevisionAfp,
    PrevisionSalud,
    Banco,
    TipoCuenta,
    # Formación
    DatosFormacion,
    TipoFormacion,
    Carrera,
    EstadoFormacion,
    Institucion,
    TipoInstitucion,
    OtroFormacion,
    TipoOtroFormacion,
    Diploma,
    # Organización
    DatosOrganizacionales,
    Empleador,
    Cargo,
    Unidad,
    AreaFuncional,
    NivelResponsabilidad,
    CentroCosto,
    # Actividad
    Actividad,
    DatosActividad,
    Proyecto,
    Cliente,
]

for modelo in lista_modelos:
    admin.site.register(modelo)
