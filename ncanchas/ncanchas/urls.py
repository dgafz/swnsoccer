from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #urls para home
    url(r'^', include('applications.home.urls')),
    #urls para cancha
    url(r'^', include('applications.cancha.urls')),
    #urls para zona
    url(r'^', include('applications.zona.urls')),
    #urls para museo
    url(r'^', include('applications.museo.urls')),

    #url para editor de texto
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
