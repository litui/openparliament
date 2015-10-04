from functools32 import lru_cache

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import mail_admins

from parliament.core.models import ElectedMember, Party, Politician
from parliament.elections.models import Election, ElectedMember
from parliament.wordpress.models import Option, Post, POST_TYPE_CHOICES

REQUIRED_POST_TYPES = ['party', 'riding', 'candidate_elxn42']
POST_TYPE_CHOICES.extend([(t, t) for t in REQUIRED_POST_TYPES])
REQUIRED_CUSTOM_FIELD_GROUPS = ['acf_candidate-info', 'acf_open-parliament-meta', 'acf_party-info']

class Command(BaseCommand):
    help = "Does something with wordpress."
    args = '[task]'

    # For wordpress commands
    valid_arguments = ['check', 'populate']

    def __init__(self):
        super(Command, self).__init__()

    @lru_cache()
    def _op_current_parties(self):
        return [m.party for m in self._op_elected_members().distinct('party')]

    @lru_cache()
    def _op_elected_members(self):
        return ElectedMember.objects.filter(end_date=None).select_related('politician', 'riding', 'party')

    @lru_cache()
    def _op_ridings(self):
        return [m.riding for m in self._op_elected_members().distinct('riding')]

    @lru_cache()
    def _ow_custom_field_groups(self):
        return Post.objects.filter(status='publish',
                                   post_type='acf',
                                   slug__in=REQUIRED_CUSTOM_FIELD_GROUPS).select_related('meta')
    #
    # @lru_cache()
    # def _ow_custom_fields(self):
    #

    def _wp_check(self):
        """ Checks Wordpress schema and data."""
        print('\nChecking OpenParliament Data...')
        print('Found {} current members of parliament.'.format(len(self._op_elected_members())))
        print('Found {} current electoral districts'.format(len(self._op_ridings())))
        print('Found {} current political parties'.format(len(self._op_current_parties())))

        print('Checking WordPress Data...')

        db_version = Option.objects.get_value('db_version')
        if not db_version or int(db_version) < 33056:
            raise CommandError('Cannot install to database with version below 33056.')
        print('Found WordPress database version: {}'.format(db_version))

        active_plugins = Option.objects.get_value('active_plugins').values()
        if 'advanced-custom-fields/acf.php' not in active_plugins:
            raise CommandError('Advanced Custom Fields plugin must be installed.')
        print('Found Advanced Custom Fields plugin.')

        if 'custom-post-type-ui/custom-post-type-ui.php' not in active_plugins:
            raise CommandError('Custom Post Type UI plugin must be installed.')
        print('Found Custom Post Type UI plugin.')
        cptui = Option.objects.get_value('cptui_post_types')
        if not cptui:
            raise CommandError('Wordpress Custom Post Type UI plugin is not configured.')

        for reqtype in REQUIRED_POST_TYPES:
            if reqtype not in cptui.keys():
                raise CommandError('Required custom post type "{}" not found.'.format(reqtype))
        print('Found all required post types defined.')

        cf_groups = self._ow_custom_field_groups()
        if not cf_groups:
            raise CommandError('Could not find custom field groups.')

        for grptype in REQUIRED_CUSTOM_FIELD_GROUPS:
            if grptype not in [g.slug for g in cf_groups]:
                raise CommandError('Custom field group "{}" not found.'.format(grptype))
        print('Found all required custom field groups.')
        print('Warning: This assumes specific fields have already been created.')

    def handle(self, *args, **options):
        if not args:
            raise CommandError('No subcommands given for wordpress task.')
        if not args[0] in self.valid_arguments:
            raise CommandError('"{}" is not a valid subcommand.'.format(args[0]))

        getattr(self, '_wp_{}'.format(args[0]))()

