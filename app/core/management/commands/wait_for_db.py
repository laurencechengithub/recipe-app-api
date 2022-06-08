"""django commands to wait for database to be ready"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """wait for db"""

    def handle(self, *args, **options):
        pass