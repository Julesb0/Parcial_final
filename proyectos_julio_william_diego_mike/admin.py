from django.contrib import admin

from .models import Comentario, Proyecto


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'estudiante',
        'estado',
        'calificacion',
        'fecha_envio',
        'fecha_revision',
    )
    list_filter = ('estado', 'fecha_envio')
    search_fields = (
        'titulo',
        'descripcion',
        'estudiante__username',
        'estudiante__first_name',
        'estudiante__last_name',
    )


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('proyecto', 'usuario', 'fecha')
    list_filter = ('fecha',)
    search_fields = (
        'texto',
        'usuario__username',
        'proyecto__titulo',
    ) 
    