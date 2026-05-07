from django.conf import settings
from django.db import models
from django.urls import reverse


class Proyecto(models.Model):
    ENVIADO = 'enviado'
    REVISION = 'revision'
    APROBADO = 'aprobado'

    ESTADOS = [
        (ENVIADO, 'Enviado'),
        (REVISION, 'En Revisión'),
        (APROBADO, 'Aprobado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='proyectos',
        on_delete=models.CASCADE
    )
    documento = models.FileField(upload_to='proyectos/')
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default=ENVIADO
    )
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    calificacion = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-fecha_envio']
        verbose_name = 'Proyecto académico'
        verbose_name_plural = 'Proyectos académicos'
        permissions = [
            ('revisar_proyecto', 'Puede revisar proyectos académicos'),
            ('exportar_proyecto', 'Puede exportar proyectos académicos'),
        ]

    def _str_(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse(
            'proyectos_julio_william_diego_mike:proyecto_detail',
            kwargs={'pk': self.pk}
        )

    @property
    def bloquea_comentarios(self):
        return self.estado == self.APROBADO


class Comentario(models.Model):
    proyecto = models.ForeignKey(
        Proyecto,
        related_name='comentarios',
        on_delete=models.CASCADE
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='comentarios_proyecto',
        on_delete=models.CASCADE
    )
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha']
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'

    def _str_(self):
        return f'Comentario de {self.usuario} en {self.proyecto}' 
        