from django.utils import timezone
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

class AdminURLMixin(object):
    def get_admin_url(self):
        content_type = ContentType \
            .objects \
            .get_for_model(self.__class__)
        return reverse("admin:%s_%s_change" % (
            content_type.app_label,
            content_type.model),
            args=(self.id,))

class Staff(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField('date published')
    user = models.ForeignKey(User)
    def __str__(self):
        return self.nombre

# class StaffPosicionManager(models.Manager):
#     def get_queryset(self):
#         current_user = request.user
#         if current_user.groups.filter(name='GestionAdmin').count():
#             return super(StaffPosicion, self).get_queryset()
#         return super(StaffPosicion, self).get_queryset().filter(staff__user_id=current_user.id)

class StaffPosicion(models.Model, AdminURLMixin):
    desc = models.CharField(max_length=100)
    padre = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    staff = models.ForeignKey(Staff, blank=True, null=True, on_delete=models.SET_NULL)
    fecha_creacion = models.DateTimeField('date published')
#    objects = StaffPosicionManager()
    def liga(self):
        return format_html('<a href="{0}/{1}">{2}</a>',
                           '/admin/gestione/staffposicion/',
                           self.id,
                           self.id)
    liga.allow_tags = True
    def __str__(self):
        return self.desc

class Estructura(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField('date published')
    cabeza = models.ForeignKey(StaffPosicion, blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.nombre

class SolicitudTipo(models.Model):
    nombre = models.CharField(max_length=100)
    desc = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre

class Encuesta(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField('date published')
    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    tipo = models.ForeignKey(SolicitudTipo, blank=True, null=True, on_delete=models.SET_NULL)
    texto = models.CharField(max_length=255)
    def __str__(self):
        return self.texto

class Capturista(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField('date published')
    user = models.ForeignKey(User)
    posicion_padre = models.ForeignKey(StaffPosicion, related_name='capturistas', related_query_name='capturista')
    def __str__(self):
        return self.nombre

class ActivaEncuesta(models.Model):
    encuesta = models.ForeignKey(Encuesta)
    asignada_a = models.ForeignKey(StaffPosicion)
    fecha_creacion = models.DateTimeField('date published')
    fecha_desde = models.DateTimeField('desde')
    fecha_hasta = models.DateTimeField('hasta')
    def __str__(self):
        return self.encuesta.nombre + "-" + self.asignada_a.desc + "-" + self.fecha_desde.strftime("%x")

class Persona(models.Model):
     IFE = models.CharField(max_length=100)
     CURP = models.CharField(max_length=100)
     nombre = models.CharField(max_length=100)
     fecha_creacion = models.DateTimeField('date published')
     def __str__(self):
         return self.nombre

class EncuestaProcManager(models.Manager):
    def ElQueSigue(self, capt, aenc):
        ps_in_aenc = aenc.persona_set.values_list('id', flat=True)
        ps = Persona.objects.exclude(id__in = ps_in_aenc)
        if ps.count() == 0:
            return None;
        ep = EncuestaProc(aencuesta=aenc, capturista=capt, persona=ps[0], fecha_creacion=timezone.now(), completa=False)
        return ep;

class EncuestaProc(models.Model):
    aencuesta = models.ForeignKey(ActivaEncuesta)
    capturista = models.ForeignKey(Capturista)
    persona = models.ForeignKey(Persona)
    fecha_creacion = models.DateTimeField('date published')
    completa = models.BooleanField(null=True)
    objects = EncuestaProcManager()
    def __str__(self):
        return self.aencuesta.encuesta.nombre + "-" + self.capturista.nombre + "-" + self.persona.nombre


class EncuestaProcForm(ModelForm):
    class Meta:
        model = EncuestaProc
        fields = ['fecha_creacion', 'completa']

