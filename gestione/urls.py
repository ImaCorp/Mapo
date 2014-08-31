from django.conf.urls import patterns, url, include

from gestione import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^encuesta/(?P<aenc_id>\d+)/$', views.encuesta, name='encuesta'),
    url(r'^doencuesta/(?P<encproc_id>\d+)/(?P<idcapt>\d+)/(?P<idaenc>\d+)/$', views.doencuesta, name='doencuesta'),
    # url(r'^(?P<enc_id>\d+)/guarda_encuesta/$', views.guarda_encuesta, name='guarda_encuesta'),
    url(r'^accounts/', include('accounts.urls')),
)