from django.urls import path
from web.views import *
from social.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',index,name="inicio"),
    path('buscador/', buscador, name="buscador"),
    path('comentarios/', formulariosComentarios, name="comentarios"),
    path('borrar_comentarios/<int:id_titulo>', borrar_comentarios, name="borrar_comentarios"),
    path('editar_comentarios/<int:id_titulo>', editar_comentarios, name="editar_comentarios")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
