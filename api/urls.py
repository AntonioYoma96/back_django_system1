from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()
# Actividad
router.register(r'actividad/actividades', views.ActividadViewSet)
router.register(r'actividad/datos-actividades', views.DatosActividadViewSet)
router.register(r'actividad/proyectos', views.ProyectoViewSet)
router.register(r'actividad/clientes', views.ClienteViewSet)
router.register(r'actividad/mesas-ayuda', views.MesaAyudaViewSet)
router.register(r'actividad/tipos-soporte', views.TipoSoporteViewSet)
router.register(r'actividad/modulos', views.ModuloViewSet)
# Colaborador
router.register(r'colaborador/colaboradores', views.ColaboradorViewSet)
router.register(r'colaborador/sexos', views.SexoViewSet)
router.register(r'colaborador/estados-civiles', views.EstadoCivilViewSet)
router.register(r'colaborador/nacionalidades', views.NacionalidadViewSet)
router.register(r'colaborador/comunas', views.ComunaViewSet)
router.register(r'colaborador/provincias', views.ProvinciaViewSet)
router.register(r'colaborador/regiones', views.RegionViewSet)
router.register(r'colaborador/hijos', views.HijoViewSet)
router.register(r'colaborador/personas-contacto', views.PersonaContactoViewSet)
router.register(r'colaborador/colaboradores-skills', views.ColaboradorSkillViewSet)
router.register(r'colaborador/skills', views.SkillViewSet)
router.register(r'colaborador/niveles-skill', views.NivelSkillViewSet)
# Contrato
router.register(r'contrato/datos-contractuales', views.DatosContractualesViewSet)
router.register(r'contrato/tipos-contrato', views.TipoContratoViewSet)
router.register(r'contrato/previsiones-afp', views.PrevisionAfpViewSet)
router.register(r'contrato/previsiones-salud', views.PrevisionSaludViewSet)
router.register(r'contrato/bancos', views.BancoViewSet)
router.register(r'contrato/tipos-cuenta', views.TipoCuentaViewSet)
# Formación
router.register(r'formacion/datos-formacion', views.DatosFormacionViewSet)
router.register(r'formacion/tipos-formacion', views.TipoFormacionViewSet)
router.register(r'formacion/carreras', views.CarreraViewSet)
router.register(r'formacion/estados-formacion', views.EstadoFormacionViewSet)
router.register(r'formacion/instituciones', views.InstitucionViewSet)
router.register(r'formacion/tipos-institucion', views.TipoInstitucionViewSet)
router.register(r'formacion/otros-formacion', views.OtroFormacionViewSet)
router.register(r'formacion/tipos-otro-formacion', views.TipoOtroFormacionViewSet)
router.register(r'formacion/diplomas', views.DiplomaViewSet)
# Organización
router.register(r'organizacion/datos-organizacionales', views.DatosOrganizacionalesViewSet)
router.register(r'organizacion/cargos', views.CargoViewSet)
router.register(r'organizacion/unidades', views.UnidadViewSet)
router.register(r'organizacion/areas-funcionales', views.AreaFuncionalViewSet)
router.register(r'organizacion/niveles-responsabilidad', views.NivelResponsabilidadViewSet)
router.register(r'organizacion/centros-costo', views.CentroCostoViewSet)
# Ticket
router.register(r'ticket/tickets', views.TicketViewSet)
router.register(r'ticket/tickets-logs', views.TicketLogViewSet)
router.register(r'ticket/prioridades', views.PrioridadViewSet)
router.register(r'ticket/tipos-ticket', views.TipoTicketViewSet)
router.register(r'ticket/etapas-ticket', views.EtapaTicketViewSet)
router.register(r'ticket/areas-ticket', views.AreaTicketViewSet)
router.register(r'ticket/dificultad-ticket', views.DificultadTicketViewSet)
router.register(r'ticket/imagenes-ticket', views.ImagenTicketViewSet)
router.register(r'ticket/mensajes', views.MensajeViewSet)
router.register(r'ticket/imagenes-mensaje', views.ImagenMensajeViewSet)
router.register(r'ticket/etiquetas', views.EtiquetaViewSet)
router.register(r'ticket/origenes', views.OrigenViewSet)

urlpatterns = [
    path('', include(router.urls))
]
