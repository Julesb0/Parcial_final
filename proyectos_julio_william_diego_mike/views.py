import csv

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .forms import ComentarioForm, ProyectoForm, RevisionProyectoForm
from .models import Comentario, Proyecto
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


class ComentarioCreateView(LoginRequiredMixin, CreateView):
    model = Comentario
    form_class = ComentarioForm

    def dispatch(self, request, *args, **kwargs):
        self.proyecto = get_object_or_404(Proyecto, pk=kwargs['pk'])

        usuario_autorizado = (
            request.user.is_superuser
            or es_docente(request.user)
            or self.proyecto.estudiante_id == request.user.id
        )

        if not usuario_autorizado:
            messages.error(request, 'No tiene permiso para comentar este proyecto.')
            return redirect('proyectos_julio_william_diego_mike:proyecto_list')

        if self.proyecto.bloquea_comentarios:
            messages.warning(
                request,
                'Este proyecto ya fue aprobado. No se permiten nuevos comentarios.'
            )
            return redirect(
                'proyectos_julio_william_diego_mike:proyecto_detail',
                pk=self.proyecto.pk
            )

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        comentario = form.save(commit=False)
        comentario.proyecto = self.proyecto
        comentario.usuario = self.request.user
        comentario.save()

        self.enviar_notificacion(comentario)

        messages.success(self.request, 'El comentario fue publicado correctamente.')
        return redirect(
            'proyectos_julio_william_diego_mike:proyecto_detail',
            pk=self.proyecto.pk
        )

    def enviar_notificacion(self, comentario):
        correo_estudiante = self.proyecto.estudiante.email

        if correo_estudiante:
            send_mail(
                subject='Nuevo comentario en su proyecto académico',
                message=(
                    f'Hola {self.proyecto.estudiante.get_full_name() or self.proyecto.estudiante.username},\n\n'
                    f'Se ha registrado un nuevo comentario en el proyecto: {self.proyecto.titulo}.\n\n'
                    f'Comentario:\n{comentario.texto}\n\n'
                    f'Ingrese al sistema para revisar el seguimiento académico.'
                ),
                from_email=None,
                recipient_list=[correo_estudiante],
                fail_silently=True,
            )


class ProyectoExportCSVView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'proyectos_julio_william_diego_mike.exportar_proyecto'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        proyectos = proyectos_filtrados_para_usuario(request)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="proyectos_academicos.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Título',
            'Estudiante',
            'Estado',
            'Fecha de envío',
            'Fecha de revisión',
            'Calificación',
        ])

        for proyecto in proyectos:
            writer.writerow([
                proyecto.titulo,
                proyecto.estudiante.username,
                proyecto.get_estado_display(),
                proyecto.fecha_envio.strftime('%Y-%m-%d %H:%M'),
                proyecto.fecha_revision.strftime('%Y-%m-%d %H:%M') if proyecto.fecha_revision else '',
                proyecto.calificacion if proyecto.calificacion is not None else '',
            ])

        return response


class ProyectoExportPDFView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'proyectos_julio_william_diego_mike.exportar_proyecto'
    raise_exception = True

    def get(self, request, *args, **kwargs):
        proyectos = proyectos_filtrados_para_usuario(request)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="proyectos_academicos.pdf"'

        pdf = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        y = height - 50

        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawString(50, y, 'Reporte de Proyectos Académicos')
        y -= 25

        pdf.setFont('Helvetica', 10)
        pdf.drawString(50, y, 'Sistema desarrollado por Julio, William, Diego y Mike')
        y -= 30

        for proyecto in proyectos:
            if y < 100:
                pdf.showPage()
                y = height - 50
                pdf.setFont('Helvetica', 10)

            pdf.setFont('Helvetica-Bold', 11)
            pdf.drawString(50, y, f'Título: {proyecto.titulo}')
            y -= 15

            pdf.setFont('Helvetica', 10)
            pdf.drawString(50, y, f'Estudiante: {proyecto.estudiante.username}')
            y -= 15
            pdf.drawString(50, y, f'Estado: {proyecto.get_estado_display()}')
            y -= 15
            pdf.drawString(
                50,
                y,
                f'Calificación: {proyecto.calificacion if proyecto.calificacion is not None else "Sin asignar"}'
            )
            y -= 25

        pdf.save()

        return response