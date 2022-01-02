from django.core.management.base import BaseCommand

from blog.models import Post


class Command(BaseCommand):
    help = 'Delete blogs'

    def add_arguments(self, parser):
        parser.add_argument('ids', nargs='+', type=int, help='Blog ID')

    def handle(self, *args, **kwargs):
        blogs_ids = kwargs['ids']

        blogs = Post.objects.filter(id__in=blogs_ids)
        if blogs:
            blogs.delete()
        self.stdout.write('Deleted with success.')
