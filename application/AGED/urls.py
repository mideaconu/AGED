#
# AGED/urls.py
#
# Author: Mihai Ionut Deaconu
#

from . import views
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls), # Admin interface
    path('accounts/', include('allauth.urls')), # Necessary for login, logout, signup etc.
    path('', include('core.urls')),
    path('media/count_data/<pk>/<name>', login_required(views.download)),
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'