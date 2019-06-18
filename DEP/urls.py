"""DEP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
removed no need for send post script command
    re_path('^run-sh/$', views.api_command_method, name='run_sh'),
"""
from django.contrib import admin
from django.urls import re_path
from . import views

urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^logout/?$', views.logout_method, name='logout_method'),
    re_path('^login/?$', views.login_method, name='login_method'),
    re_path('^add/?$', views.add_method, name='add_method'),
    re_path('^remove/?$', views.remove_method, name='remove_method'),
    re_path('^modular/?$', views.modular_method, name='modular_method'),
    re_path('^apply/?$', views.apply_method, name='apply_method'),
    re_path('^get_json/?$', views.get_json_method, name='get_json_method'),
    re_path('^$', views.main_method, name='main_method'),
    re_path('^add_device/?$', views.add_device_method, name='add_device_method'),
    re_path('^remove_device/?$', views.remove_device_method, name='remove_device_method'),
    re_path('^show_devices/?$', views.show_devices_method, name='show_devices_method'),
    re_path('^api_command/?$', views.api_command_method, name='api_command_method'),
    re_path('^service_status/?$', views.service_status_method, name='service_status_method'),
    re_path('^system_journal/?$', views.system_journal_method, name='system_journal_method'),
    re_path('^manifest/?$', views.manifest_method, name='manifest_method'),

    re_path('.*', views.not_present_method, name='not_present_method'),

]

