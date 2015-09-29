import phpserialize
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import mail_admins

from parliament.wordpress.models import Option, Post, POST_TYPE_CHOICES

REQUIRED_POST_TYPES = ['party', 'candidate_elxn42']
POST_TYPE_CHOICES.extend([(t, t) for t in REQUIRED_POST_TYPES])

class Command(BaseCommand):
    help = "Does something with wordpress."
    args = '[task]'

    def _wp_check(self):
        """ Checks Wordpress schema and data."""
        db_version = Option.objects.get_value('db_version')
        active_plugins = phpserialize.loads(Option.objects.get_value('active_plugins')).values()
        cptui = phpserialize.loads(Option.objects.get_value('cptui_post_types'))

        if not db_version or int(db_version) < 33056:
            raise CommandError('Cannot install to database with version below 33056.')
        if 'advanced-custom-fields/acf.php' not in active_plugins:
            raise CommandError('Advanced Custom Fields plugin must be installed.')
        if 'custom-post-type-ui/custom-post-type-ui.php' not in active_plugins:
            raise CommandError('Custom Post Type UI plugin must be installed.')
        if not cptui:
            raise CommandError('Wordpress Custom Post Type UI plugin is not configured.')

        required_types = ['party', 'candidate_elxn42']
        for reqtype in required_types:
            if reqtype not in cptui.keys():
                raise CommandError('Required custom post type "{}" not found.'.format(reqtype))

        cf_groups = Post.objects.filter(status='publish', post_type='acf').select_related('meta')

        # TODO: Continue check function

    def handle(self, *args, **options):
        if not args:
            raise CommandError('No subcommands given for wordpress task.')

        if args[0] == 'check':
            self._wp_check()