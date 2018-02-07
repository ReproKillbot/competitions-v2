import uuid

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from competitions.models import Competition, CompetitionParticipant
from leaderboards.models import Leaderboard
from datasets.models import Data, DataGroup
from profile.models import User

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        my_title = "Competition {}".format(uuid.uiid4())
        # my_logo =  ""
        # my_created_by = timezone.now()
        my_created_by = User.objects.get(username='tthomas63')
        my_created_when  = timezone.now()
        # my_collaborators
        try:
            temp_comp = Competition.objects.create(title=my_title, created_by=my_created_by, created_when=my_created_when)
            self.stdout.write(self.style.SUCCESS('Successfully created competition "%s"' % temp_comp.id))
        except:
            self.stdout.write(self.style.FAILURE('Failed to create competition'))
        # for poll_id in options['poll_id']:
        #     try:
        #         poll = Poll.objects.get(pk=poll_id)
        #     except Poll.DoesNotExist:
        #         raise CommandError('Poll "%s" does not exist' % poll_id)
        #
        #     poll.opened = False
        #     poll.save()
        #
        #     self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
