"""Blacklist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as sys_views
from app.forms import LoginForm
from app import views as app_views

urlpatterns = [
    ###########
    # Edit page
    ##########
    url(r'^edit/$', app_views.editBlackList, name='edit'),
    ###########
    # Edit process page
    ##########
    url(r'^edit_process/$', app_views.editProcess, name='editProcess'),
    ###########
    # Ajax search page
    ##########
    url(r'^ajax_search/$', app_views.ajaxSearch, name='ajaxSearch'),
    ###########
    # Ajax delete db page
    ##########
    url(r'^delete_db/$', app_views.deleteDbByAjax, name='deleteDbByAjax'),
    ############
    # Admin page
    ############
    url(r'^admin/', admin.site.urls),
    ############
    # Login page
    ############
    url(r'^$',
        sys_views.login,
        {
            'template_name': 'login.html',
            'authentication_form': LoginForm,
        },
        name='login'),
    ###############
    # Logout action
    ###############
    url(r'^logout$',
        sys_views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
]
