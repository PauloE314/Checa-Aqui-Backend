from django.core.management.base import BaseCommand, CommandError
from products.product_update import load

class Command(BaseCommand):
    help = "Atualizar banco de dados dos produtos"

    def handle(self, *args, **options):
        load()