from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import ComentarioForm, ProyectoForm, RevisionProyectoForm
from .models import Proyecto
from .roles import (
    DocenteOPropietarioMixin,
    DocenteRequiredMixin,
    EstudianteRequiredMixin,
    PropietarioEstudianteMixin,
    es_docente,
)


class InicioView(TemplateView):
    template_name = 'inicio.html'


def proyectos_filtrados_para_usuario(request):
    proyectos = Proyecto.objects.select_related('estudiante')

    if not (request.user.is_superuser or es_docente(request.user)):
        proyectos = proyectos.filter(estudiante=request.user)

    estado = request.GET.get('estado')
    estudiante_id = request.GET.get('estudiante')

    if estado:
        proyectos = proyectos.filter(estado=estado)

    if estudiante_id and (request.user.is_superuser or es_docente(request.user)):
        proyectos = proyectos.filter(estudiante_id=estudiante_id)

    return proyectos


class ProyectoListView(LoginRequiredMixin, ListView):
    model = Proyecto
    template_name = 'proyectos_julio_william_diego_mike/proyecto_list.html'
    context_object_name = 'proyectos'
    paginate_by = 8

    def get_queryset(self):
        return proyectos_filtrados_para_usuario(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['estados'] = Proyecto.ESTADOS
        context['estudiantes'] = User.objects.filter(
            proyectos__isnull=False
        ).distinct().order_by('username')

        context['estado_actual'] = self.request.GET.get('estado', '')
        context['estudiante_actual'] = self.request.GET.get('estudiante', '')
        context['es_docente'] = es_docente(self.request.user) or self.request.user.is_superuser
        context['comentario_form'] = ComentarioForm()

        return context


class ProyectoDetailView(LoginRequiredMixin, DocenteOPropietarioMixin, DetailView):
    model = Proyecto
    template_name = 'proyectos_julio_william_diego_mike/proyecto_detail.html'
    context_object_name = 'proyecto'

    def get_queryset(self):
        return Proyecto.objects.select_related(
            'estudiante'
        ).prefetch_related(
            'comentarios__usuario'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['comentario_form'] = ComentarioForm()
        context['es_docente'] = es_docente(self.request.user) or self.request.user.is_superuser

        return context


class ProyectoCreateView(LoginRequiredMixin, EstudianteRequiredMixin, CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos_julio_william_diego_mike/proyecto_form.html'

    def form_valid(self, form):
        form.instance.estudiante = self.request.user
        messages.success(self.request, 'El proyecto fue registrado correctamente.')
        return super().form_valid(form)


class ProyectoUpdateView(LoginRequiredMixin, PropietarioEstudianteMixin, UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos_julio_william_diego_mike/proyecto_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'El proyecto fue actualizado correctamente.')
        return super().form_valid(form)


class ProyectoDeleteView(LoginRequiredMixin, PropietarioEstudianteMixin, DeleteView):
    model = Proyecto
    template_name = 'proyectos_julio_william_diego_mike/proyecto_confirm_delete.html'
    success_url = reverse_lazy('proyectos_julio_william_diego_mike:proyecto_list')

    def form_valid(self, form):
        messages.success(self.request, 'El proyecto fue eliminado correctamente.')
        return super().form_valid(form)


class ProyectoRevisionView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DocenteRequiredMixin,
    UpdateView
):
    model = Proyecto
    form_class = RevisionProyectoForm
    template_name = 'proyectos_julio_william_diego_mike/proyecto_revision.html'
    permission_required = 'proyectos_julio_william_diego_mike.revisar_proyecto'
    raise_exception = True

    def form_valid(self, form):
        form.instance.fecha_revision = timezone.now()
        messages.success(self.request, 'La revisión del proyecto fue guardada correctamente.')
        return super().form_valid(form)