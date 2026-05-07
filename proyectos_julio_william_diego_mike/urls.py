from django.urls import path

from .views import (
    ProyectoCreateView,
    ProyectoDeleteView,
    ProyectoDetailView,
    ProyectoListView,
    ProyectoRevisionView,
    ProyectoUpdateView,
)

app_name = 'proyectos_julio_william_diego_mike'

urlpatterns = [
    path('', ProyectoListView.as_view(), name='proyecto_list'),
    path('crear/', ProyectoCreateView.as_view(), name='proyecto_create'),
    path('<int:pk>/', ProyectoDetailView.as_view(), name='proyecto_detail'),
    path('<int:pk>/editar/', ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('<int:pk>/eliminar/', ProyectoDeleteView.as_view(), name='proyecto_delete'),
    path('<int:pk>/revisar/', ProyectoRevisionView.as_view(), name='proyecto_revision'),
]