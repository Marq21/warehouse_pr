"""
URL configuration for warehouse_pr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from catalog import views
from django.contrib import admin
from django.urls import include, path

from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('captcha/', include('captcha.urls')),
    path('', views.index, name='home'),
    path('catalog/', include('catalog.urls')),
    path('store_api/', include('store_api.urls')),
    path('profiles/', include('registration_app.urls')),
    path('logs/', include('actions.urls')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('inventory/', include('inventory.urls')),
    path('exp_date/', include('expiration_dates.urls')),
    path('goods_receipt/', include('goods_receipt.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = views.page_not_found
admin.site.site_header = "Панель администрирования"
