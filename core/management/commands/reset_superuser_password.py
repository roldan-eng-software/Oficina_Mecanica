"""
Comando de gerenciamento para resetar senha do superusuário.
Útil quando a senha foi esquecida ou precisa ser alterada.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Reseta a senha de um superusuário existente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
            help='Username do superusuário',
        )
        parser.add_argument(
            '--password',
            type=str,
            default=os.environ.get('DJANGO_SUPERUSER_PASSWORD', None),
            help='Nova senha (ou use variável DJANGO_SUPERUSER_PASSWORD)',
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        try:
            user = User.objects.get(username=username, is_superuser=True)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Superusuário "{username}" não encontrado.')
            )
            return

        # Se não há senha, cria uma senha padrão e avisa
        if not password:
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
            self.stdout.write(
                self.style.WARNING(
                    f'ATENÇÃO: Usando senha padrão. Configure DJANGO_SUPERUSER_PASSWORD '
                    f'nas variáveis de ambiente para segurança.'
                )
            )

        # Reseta a senha
        try:
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Senha do superusuário "{username}" resetada com sucesso!'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'IMPORTANTE: Altere a senha após o primeiro login!'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao resetar senha: {e}')
            )




