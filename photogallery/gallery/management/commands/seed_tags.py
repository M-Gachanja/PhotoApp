from django.core.management.base import BaseCommand
from gallery.models import Tag

class Command(BaseCommand):
    help = 'Seed the database with sample tags'

    def handle(self, *args, **options):
        tags = [
            'Nature', 'Portrait', 'Landscape', 'Urban', 'Abstract',
            'Wildlife', 'Travel', 'Food', 'Architecture', 'Sports',
            'Night', 'Black & White', 'Colorful', 'Minimal', 'Macro'
        ]
        
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created tag: {tag_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Tag already exists: {tag_name}'))