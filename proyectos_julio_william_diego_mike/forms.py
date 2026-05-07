from django import forms

from .models import Comentario, Proyecto


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['titulo', 'descripcion', 'documento']
        labels = {
            'titulo': 'Título del proyecto',
            'descripcion': 'Descripción del proyecto',
            'documento': 'Documento del proyecto',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Ejemplo: Sistema de seguimiento académico'
            }),
            'descripcion': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Describa el objetivo, alcance y características principales del proyecto.'
            }),
        }


class RevisionProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['estado', 'calificacion']
        labels = {
            'estado': 'Estado del proyecto',
            'calificacion': 'Calificación asignada',
        }

    def clean_calificacion(self):
        calificacion = self.cleaned_data.get('calificacion')

        if calificacion is not None and (calificacion < 0 or calificacion > 5):
            raise forms.ValidationError(
                'La calificación debe estar entre 0.00 y 5.00.'
            )

        return calificacion


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        labels = {
            'texto': 'Comentario',
        }
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escriba una observación académica clara y respetuosa.'
            }),
        }
