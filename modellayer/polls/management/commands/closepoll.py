from django.core.management.base import BaseCommand, CommandError
from polls.models import Question

class Command(BaseCommand):
    help = 'Close or delete specified polls'

    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)
        parser.add_argument('--delete', action='store_true', help='Delete poll instead of closing it')

    def handle(self, *args, **options):
        for poll_id in options['poll_ids']:
            try:
                poll = Question.objects.get(pk=poll_id)
                if options['delete']:
                    poll.delete()
                    self.stdout.write(self.style.SUCCESS(f'Successfully deleted poll "{poll_id}"'))
                else:
                    poll.opened = False
                    poll.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully closed poll "{poll_id}"'))
            except Question.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Poll "{poll_id}" does not exist'))

