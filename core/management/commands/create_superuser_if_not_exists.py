"""
Comando de gerenciamento para criar superusuário se não existir.
Útil para deploy em produção quando o shell não está disponível.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Cria um superusuário se não existir nenhum'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default=os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'),
            help='Username do superusuário',
        )
        parser.add_argument(
            '--email',
            type=str,
            default=os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
            help='Email do superusuário',
        )
        parser.add_argument(
            '--password',
            type=str,
            default=os.environ.get('DJANGO_SUPERUSER_PASSWORD', None),
            help='Senha do superusuário (ou use variável DJANGO_SUPERUSER_PASSWORD)',
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Verifica se já existe um superusuário
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Superusuário já existe. Pulando criação.')
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

        # Cria o superusuário
        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superusuário "{username}" criado com sucesso!'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    'IMPORTANTE: Altere a senha após o primeiro login!'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao criar superusuário: {e}')
            )

