from django.contrib.auth.models import Group, Permission, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Crea grupos, permisos y usuarios de prueba para el sistema.'

    def handle(self, *args, **options):
        grupo_estudiante, _ = Group.objects.get_or_create(name='Estudiante')
        grupo_docente, _ = Group.objects.get_or_create(name='Docente')

        permisos_docente = Permission.objects.filter(
            codename__in=[
                'revisar_proyecto',
                'exportar_proyecto',
                'view_proyecto',
                'view_comentario',
                'add_comentario',
            ]
        )
        grupo_docente.permissions.set(permisos_docente)

        permisos_estudiante = Permission.objects.filter(
            codename__in=[
                'add_proyecto',
                'change_proyecto',
                'delete_proyecto',
                'view_proyecto',
                'add_comentario',
                'view_comentario',
            ]
        )
        grupo_estudiante.permissions.set(permisos_estudiante)

        estudiantes = [
            ('julio', 'julio@universidad.edu.co', 'Julio'),
            ('william', 'william@universidad.edu.co', 'William'),
            ('diego', 'diego@universidad.edu.co', 'Diego'),
            ('mike', 'mike@universidad.edu.co', 'Mike'),
        ]

        for username, email, first_name in estudiantes:
            usuario, creado = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': first_name,
                }
            )

            if creado:
                usuario.set_password('Estudiante123')
                usuario.save()

            usuario.groups.add(grupo_estudiante)

        docente, creado = User.objects.get_or_create(
            username='docente',
            defaults={
                'email': 'docente@universidad.edu.co',
                'first_name': 'Docente',
            }
        )

        if creado:
            docente.set_password('Docente123')
            docente.save()

        docente.groups.add(grupo_docente)

        admin, creado = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@universidad.edu.co',
                'first_name': 'Administrador',
                'is_staff': True,
                'is_superuser': True,
            }
        )

        if creado:
            admin.set_password('Admin12345')
            admin.save()

        self.stdout.write(
            self.style.SUCCESS('Roles, permisos y usuarios creados correctamente.')
        )