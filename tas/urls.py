""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from rest_framework import routers
from myapp import views

admin.autodiscover()

router = routers.DefaultRouter()
router.register('news', views.newsViewSet)
router.register('userData', views.userDataViewSet)
router.register('userTempData', views.userTempDataViewSet)
router.register('ris', views.risViewSet)
urlpatterns = [
    path('favicon.ico', RedirectView.as_view(
                        url=staticfiles_storage.url('favicon.ico'),
                        permanent=False), name="favicon"),
    path('schindler-logo.jpg', RedirectView.as_view(
                        url=staticfiles_storage.url('schindler-logo.jpg'),
                        permanent=False), name="schindler-logo"),
    path('schindler-logo-noletters.png', RedirectView.as_view(
                        url=staticfiles_storage.url('schindler-logo-noletters.png'),
                        permanent=False), name="schindler-logo-noletters"),
    path('nx300_17.png', RedirectView.as_view(
                        url=staticfiles_storage.url('nx300_17.png'),
                        permanent=False), name="nx300_17"),
    path('nx300_25.png', RedirectView.as_view(
                        url=staticfiles_storage.url('nx300_25.png'), 
                        permanent=False), name="nx300_25"),
    path('txr5_1.png', RedirectView.as_view(
                        url=staticfiles_storage.url('txr5_1.png'),
                        permanent=False), name="txr5_1"),
    path('txr5_2.png', RedirectView.as_view(
                        url=staticfiles_storage.url('txr5_2.png'),
                        permanent=False), name="txr5_2"),
    path('txgc2_360.png', RedirectView.as_view(
                        url=staticfiles_storage.url('txgc2_360.png'),
                        permanent=False), name="txgc2_360"),
    path('txgc2_347.png', RedirectView.as_view(
                        url=staticfiles_storage.url('txgc2_347.png'),
                        permanent=False), name="txgc2_347"),
    path('txgc2_362.png', RedirectView.as_view(
                        url=staticfiles_storage.url('txgc2_362.png'),
                        permanent=False), name="txgc2_362"),
    path('hx_1.png', RedirectView.as_view(
                        url=staticfiles_storage.url('hx_1.png'),
                        permanent=False), name="hx_1"),
    path('hx_2.png', RedirectView.as_view(
                        url=staticfiles_storage.url('hx_2.png'),
                        permanent=False), name="hx_2"),
    path('bottomlab.png', RedirectView.as_view(
                        url=staticfiles_storage.url('bottomlab.png'),
                        permanent=False), name="bottomlab"),
    path('labmap.png', RedirectView.as_view(
                        url=staticfiles_storage.url('labmap.png'),
                        permanent=False), name="labmap"),
    path('tims_towerbooking.png', RedirectView.as_view(
	                url=staticfiles_storage.url('tims_towerbooking.png'),
	                permanent=False), name="tims_towerbooking"),
	path('icon_information.png', RedirectView.as_view(
                        url=staticfiles_storage.url('icon_information.png'),
                        permanent=False), name="icon_information"),
	path('icon_warning.png', RedirectView.as_view(
                        url=staticfiles_storage.url('icon_warning.png'),
                        permanent=False), name="icon_warning"),
	path('icon_urgent.png', RedirectView.as_view(
                        url=staticfiles_storage.url('icon_urgent.png'),
                        permanent=False), name="icon_urgent"),
    path('icon_events.png', RedirectView.as_view(
                        url=staticfiles_storage.url('icon_events.png'),
                        permanent=False), name="icon_events"),
    path('icon_building.png', RedirectView.as_view(
                        url=staticfiles_storage.url('icon_building.png'),
                        permanent=False), name="icon_building"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('home2/', views.home2),
    path('home3/',views.home3),
    path('announcements/', views.announcements),
]

