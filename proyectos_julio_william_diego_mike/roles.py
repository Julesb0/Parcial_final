from functools import wraps

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


GRUPO_ESTUDIANTE = 'Estudiante'
GRUPO_DOCENTE = 'Docente'


def pertenece_a_grupo(user, nombre_grupo):
    return user.is_authenticated and user.groups.filter(name=nombre_grupo).exists()


def es_estudiante(user):
    return pertenece_a_grupo(user, GRUPO_ESTUDIANTE)


def es_docente(user):
    return pertenece_a_grupo(user, GRUPO_DOCENTE)


def grupo_requerido(*nombres_grupo):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            if any(pertenece_a_grupo(request.user, grupo) for grupo in nombres_grupo):
                return view_func(request, *args, **kwargs)

            raise PermissionDenied

        return _wrapped_view

    return decorador


class EstudianteRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or es_estudiante(self.request.user)


class DocenteRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or es_docente(self.request.user)


class DocenteOPropietarioMixin(UserPassesTestMixin):
    def test_func(self):
        proyecto = self.get_object()
        usuario = self.request.user

        return (
            usuario.is_superuser
            or es_docente(usuario)
            or proyecto.estudiante_id == usuario.id
        )


class PropietarioEstudianteMixin(UserPassesTestMixin):
    def test_func(self):
        proyecto = self.get_object()
        usuario = self.request.user

        return usuario.is_superuser or (
            es_estudiante(usuario)
            and proyecto.estudiante_id == usuario.id
        )