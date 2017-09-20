"""event_placement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LoginView
from django.views.generic import RedirectView
from events.views import EventsPlacementListView, EventsPlacemenOrmView
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='admin/report/'), name="home"),
    url(r'^admin/login/$', LoginView.as_view(), name='login'),
    url(r'^admin/report/', EventsPlacementListView.as_view(
        template_name='events/export.html'), name='report'),
    url(r'^admin/report-orm/', EventsPlacemenOrmView.as_view(
        template_name='events/export.html'), name='report-orm'),
]
