from django.contrib import admin

from api.models import *

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
    MesaAyuda,
    TipoSoporte,
    Modulo,
    # Ticket
    Ticket,
    TicketLog,
    Prioridad,
    TipoTicket,
    EtapaTicket,
    ImagenTicket,
    Mensaje,
    ImagenMensaje,
    Etiqueta,
    Origen,
]

for modelo in lista_modelos:
    admin.site.register(modelo)
