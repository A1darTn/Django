from django.core.management.base import BaseCommand
from books.models import Book
import json

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('fixtures/books.json', 'r', encoding="utf8") as file:
            books = json.load(file)
            for item in books:
                fields = item['fields']

                Book.objects.create(
                    name = fields['name'],
                    author = fields['author'],
                    pub_date = fields['pub_date'])