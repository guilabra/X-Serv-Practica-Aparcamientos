"""finalproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve
from django.contrib.auth.views import logout
from myfinalapp import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.start),
    url(r'^aparcamientos$', views.showParkings),
    url(r'^login$', views.tolog),
    url(r'^logout', logout, {'next_page' : '/'}),
    url(r'^filtrarAparcamientos$', views.filtParkings),
    url(r'^incluirComentario/(.+)$', views.includeComment),
    url(r'^seleccionFavorito/(.+)$', views.includeFavorite),
    url(r'^cambiartitulo$', views.changeTitle),
    url(r'^aparcamientos/(.+)$', views.showParkingId),
    url(r'^about$', views.showAbout),    
    url(r'^(.+)/xml$', views.showXML),
    url(r'^(.+)$', views.userPage),
]
