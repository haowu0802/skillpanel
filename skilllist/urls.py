"""skilllist URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from tracker import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^trackers/new$', views.new_tracker, name="new_tracker"),
    # any digits for Tracker id
    url(r'^trackers/(\d+)/$', views.view_tracker, name='view_tracker'),
    url(r'^trackers/(\d+)/add_log$', views.add_log, name='add_log'),
    # url(r'^admin/', admin.site.urls),
]
