import datetime
from django.contrib import admin
from gestione.models import Estructura, Staff, StaffPosicion
from gestione.models import Encuesta, Pregunta, SolicitudTipo, Capturista, ActivaEncuesta
from django.core.urlresolvers import reverse
from django.utils.html import format_html
# from django.utils.safestring import mark_safe

class Preguntas(admin.StackedInline):
    model = Pregunta
    extra = 1

class Capturistas(admin.TabularInline):
    model = Capturista
    extra = 1

class StaffPosiciones(admin.TabularInline):

    model = StaffPosicion
    extra = 1

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (instance._meta.app_label,
                                              instance._meta.module_name),
                      args=(instance.id,))
        return format_html(u'<a href="{}">Edit</a>', url)
        # … or if you want to include other fields:
        return format_html(u'<a href="{}">Edit: {}</a>', url, instance.title)

    fields = ('admin_link','desc', 'staff',)
    readonly_fields = ('admin_link',)

    def save_model(self, request, obj, form, change):
        obj.fecha_creacion = datetime.datetime.now()
        obj.save()

class EncuestaAdmin(admin.ModelAdmin):
    inlines = [Preguntas]

class StaffPosicionAdmin(admin.ModelAdmin):
    inlines = [StaffPosiciones, Capturistas]
    readonly_fields = ('fecha_creacion','padre','get_padre_url')
    list_display  = ['padre','desc','staff','fecha_creacion']
    list_display_links  = ['desc']

    def get_padre_url(self, obj):
        return format_html(u'<a href="{1}">{2}</a>', '', obj.padre.get_admin_url(), obj.padre)
    get_padre_url.allow_tags = True
    get_padre_url.short_description = 'Padre'

    fieldsets = [
        (None, {'fields': ['get_padre_url']}),
        (None, {'fields': ['desc','staff','fecha_creacion']}),
    ]

    def get_queryset(self, request):
        qs = super(StaffPosicionAdmin, self).get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name='GestionAdmin').count():
            return qs
        return qs.filter(staff__user_id=request.user.id) | qs.filter(padre__staff__user_id=request.user.id)
    def save_model(self, request, obj, form, change):
        obj.fecha_creacion = datetime.datetime.now()
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            if isinstance(instance, StaffPosicion): #Check if it is the correct type of inline
                instance.fecha_creacion = datetime.datetime.now()
                instance.save()

admin.site.register(Staff)
admin.site.register(Estructura)
admin.site.register(StaffPosicion, StaffPosicionAdmin)

admin.site.register(SolicitudTipo)
admin.site.register(Encuesta, EncuestaAdmin)

admin.site.register(ActivaEncuesta)
admin.site.register(Capturista)
