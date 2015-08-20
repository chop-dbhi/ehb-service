from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from datetime import datetime
from core.encryption.encryptionFields import EncryptCharField, EncryptDateField
import random
import string
import hashlib

__all__ = ('Subject', 'ExternalSystem', 'ExternalRecord', 'ExternalRecordRelation', 'SubjectValidation')

date_help_text = "Please use date format: <em>YYYY-MM-DD</em>"


class CreatedModified(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Record Creation DateTime',
        help_text=date_help_text
    )
    modified = models.DateTimeField(
        auto_now_add=True,
        auto_now=True,
        verbose_name='Record Last Modified DateTime',
        help_text=date_help_text
    )

    class Meta(object):
        abstract = True
        app_label = u'core'

    def save(self, force_insert=False, force_update=False, using=None):
        now = datetime.now()

        if not self.created:
            self.created = now

        self.modified = now

        super(CreatedModified, self).save()

    def responseFieldDict(self):
        response = {}

        for k in self.__dict__.keys():
            if not k.startswith('_'):
                response[k] = (str(self.__dict__.get(k)))

        return response


class Organization(CreatedModified):
    # The name of the organization, e.g. CHOP
    name = models.CharField(max_length=255, unique=True)
    # The name of the unique subject identifier used by the organization, e.g. MRN
    subject_id_label = models.CharField(
        max_length=50,
        verbose_name='Unique Subject Record ID Label',
        default='Record ID'
    )

    class Meta(CreatedModified.Meta):
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Subject(CreatedModified):
    '''
    This class represents a master patient index for the eHB system. It serves as the
    primary key for linking a given subject stored in the eHB to all other records stored in
    external systems
    '''
    first_name = EncryptCharField(max_length=50, verbose_name='First Name')
    last_name = EncryptCharField(max_length=70, verbose_name='Last Name')
    # This is the organization that created the subject record, e.g. CHOP
    organization = models.ForeignKey(Organization)
    # This is the organization's id for this subject, e.g. MRN value
    organization_subject_id = EncryptCharField(max_length=120, verbose_name='Organization Subject Record ID')
    dob = EncryptDateField(verbose_name='Date Of Birth', help_text=date_help_text)
    cleanmsg = 'There is already a Subject for this Organization and Subject ID'

    class Meta(CreatedModified.Meta):
        ordering = ['organization', 'organization_subject_id']

    # class Meta(CreatedModified.Meta):
    #    unique_together=('organization','organization_subject_id')
    # I WOULD LIKE TO USE THE META ABOVE BUT RIGHT NOW THAT BREAKS THE ehb-client WHEN TRYING UPDATE AN EXTERNAL_RECORD

    def clean(self):
        try:
            subs = Subject.objects.filter(
                organization_subject_id=self.organization_subject_id).filter(
                organization=self.organization)

            for sub in subs:
                if sub.pk != self.pk:  # if they are equal then we are modifying this record
                    raise ValidationError(self.cleanmsg)

        except Organization.DoesNotExist:
            pass  # The Organization field validation will handle this

    def __unicode__(self):
        return "{0}, {1} : {2} : {3}".format(
            self.last_name,
            self.first_name,
            self.organization.name,
            self.organization_subject_id
        )


class GroupPropsKey(CreatedModified):

    class Meta(object):
        abstract = True
        app_label = u'core'

    def ehb_prop(self, GROUP, KEY, default=None):
        EHB_PROPS = settings.EHB_PROPS
        if EHB_PROPS:
            GROUP_SETTINGS = EHB_PROPS.get(GROUP)
            if GROUP_SETTINGS:
                return GROUP_SETTINGS.get(KEY, default)


class GroupEhbKey(GroupPropsKey):

    key = EncryptCharField(max_length=255, unique=True, verbose_name='EHB KEY', editable=False, blank=True)

    def _make_random_key(self, seed, ja, l, chars=string.ascii_uppercase + string.digits):
        random.seed(seed)
        random.jumpahead(ja * 50)
        return ''.join(random.choice(chars) for idx in range(l))

    def _set_key(self):
        '''Generate a unique key'''
        if not self.pk:
            ehb_key_length = self._ehb_key_length()
            seed = self._ehb_key_seed()
            jump = GroupEhbKey.objects.count()
            # Generate a new key, overriding any key that was used to create this object
            uk = ''
            idx = 0
            max_idx = 1e6
            while idx < max_idx:
                uk = self._make_random_key(seed=seed, ja=jump + idx, l=ehb_key_length)
                if not GroupEhbKey.objects.all():
                    idx = max_idx
                else:
                    grps_using_uk = GroupEhbKey.objects.filter(key=uk)
                    if grps_using_uk.count() == 0:
                        idx = max_idx
                    else:
                        idx += 1
            self.key = uk

    def _ehb_key_seed(self, default=123456789):
        return self.ehb_prop('EHB_GROUP_EHB_KEYS', 'seed', default)

    def _ehb_key_length(self, default=15):
        return self.ehb_prop('EHB_GROUP_EHB_KEYS', 'length', default)

    def save(self, force_insert=False, force_update=False, using=None):
        self._set_key()
        super(GroupEhbKey, self).save()


class Group(CreatedModified):
    '''
    This class is used as a unique identifier to group related model objects
    such as Subjects and External Records.

    The ehb_key field is randomly generated by the eHB and is guaranteed to be
    unique. Values for ehb_key submitted to
    the API or in a form are ignored.
    '''

    name = EncryptCharField(max_length=255, unique=True, verbose_name='Group Name')
    client_key = models.CharField(max_length=255, verbose_name='Client KEY', editable=True)
    is_locking = models.BooleanField(default=False, verbose_name='Lock Group')
    # this cannot use onetoone because I don't want the ehb_keys to EVER be deleted
    ehb_key = models.ForeignKey(GroupEhbKey, editable=False, blank=True, unique=True)
    desc_help = 'Please briefly describe this Group.'
    description = models.TextField(verbose_name='Group Description', help_text=desc_help)

    def _create_ehb_key(self):
        '''generate an ehb_key for this Group'''
        # if the key already exists then this model is being edited but this key should not change
        try:
            if self.ehb_key:
                return
        except Exception:
            group_ehb_key = GroupEhbKey()
            group_ehb_key.save()
            self.ehb_key = group_ehb_key

    def ehb_prop(self, GROUP, KEY, default=None):
        EHB_PROPS = settings.EHB_PROPS
        if EHB_PROPS:
            GROUP_SETTINGS = EHB_PROPS.get(GROUP)
            if GROUP_SETTINGS:
                return GROUP_SETTINGS.get(KEY, default)

    def _salt_length(self, default=12):
        return self.ehb_prop('EHB_GROUP_CLIENT_KEYS', 'salt_length', default)

    def _salt_seed(self, default=987654321):
        return self.ehb_prop('EHB_GROUP_CLIENT_KEYS', 'seed', default)

    def _make_salt(self, jump):
        salt_length = self._salt_length()
        seed = self._salt_seed()
        chars = string.ascii_uppercase + string.digits
        random.seed(seed)
        random.jumpahead(jump)

        return ''.join(random.choice(chars) for idx in range(salt_length))

    def _hash_value(self, value):
        h = hashlib.sha256()
        h.update(value)
        return h.hexdigest()

    def verify_client_key(self, other_key):
        if not other_key:
            return False

        b, alg, salt, shpw = self.client_key.split('$')

        return self._hash_value(salt + other_key) == shpw

    def save(self, force_insert=False, force_update=False, using=None):
        self._create_ehb_key()
        jump = self.pk

        if not jump:
            jump = Group.objects.count()
        salt = self._make_salt(jump=jump)
        prefix = '$sha256$' + salt + '$'
        if self.client_key and not self.client_key.startswith(prefix):
            self.client_key = '$sha256$'+salt+'$'+self._hash_value(salt + self.client_key)
        super(Group, self).save()

    class Meta(CreatedModified.Meta):
        ordering = ['name']

    def __unicode__(self):
        return self.name


class SubjectGroup(CreatedModified):

    subjects = models.ManyToManyField(Subject)

    group = models.ForeignKey(Group, unique=True)

    class Meta(CreatedModified.Meta):
        ordering = ['group']


# class ExternalRecordRelation(CreatedModified):
#    id = models.IntegerField(primary_key=True)
#    desc = models.CharField(max_length=50)
#
#    class Meta(CreatedModified.Meta):
#        ordering = ['id']
#
#    def __unicode__(self):
#        return self.desc


class ExternalSystem(CreatedModified):
    '''This class is the base class for defining an arbitrary external system for which the eHB is going
    to maintain information. It holds only the name, description, date_created, last_modified and subjects
    fields. The subjects field returns all the subjects in the eHB that have records in the external system
    as tracked by the eHB (i.e. records could exist in the external system for a subject that the eHB doesn't
    know about.)'''

    # Arbitrary name of the external system, e.g. CHOP TiU REDCap
    name = models.CharField(max_length=200, unique=True, verbose_name='External System Name')
    # Path to this external system
    url = models.URLField(max_length=255, unique=True, verbose_name='External System URL')
    desc_help = 'Please briefly describe this external system.'
    description = models.TextField(verbose_name='System Description', help_text=desc_help)
    subjects = models.ManyToManyField(Subject, through='ExternalRecord', blank=True)

    class Meta(CreatedModified.Meta):
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ExternalRecordLabel(CreatedModified):
    '''
    ExternalRecordLabel objects can be associated with an ExternalRecord to provide
    further clarity to end-users of the eHB service as to additional metadata associated
    with the ExternalRecord
    '''

    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=100, verbose_name="Label")

    def __unicode__(self):
        return self.label


class ExternalRecord(CreatedModified):
    '''
    This is the base level join table for matching an eHB tracked subject to a record in
    an external system record tracked by the eHB
    '''

    subject = models.ForeignKey(Subject)
    # ExternalSystem where the external records exist
    external_system = models.ForeignKey(ExternalSystem, verbose_name="External System")
    # Path to the table, directory, other where a collection of record ids exist on the external_system
    path = models.CharField(max_length=255, blank=True, verbose_name='Path to record collection')
    # This is the record id for this subject in the the external system
    rec_verb = "Record ID in External System"
    # The unique record identifier for the external_system + path
    record_id = models.CharField(max_length=50, verbose_name=rec_verb)
    # To track pedigree
    # relation = models.ForeignKey(ExternalRecordRelation, verbose_name="Record Relationship (Pedigree)", null=True)
    label = models.ForeignKey(ExternalRecordLabel, verbose_name="Label", default=1, blank=True)
    cleanmsg = 'There is already an entry with this path & record id for this external system'

    # class Meta(CreatedModified.Meta):
    #    unique_together=('external_system','record_id', 'path')
    # WOULD LIKE TO USE THE META ABOVE BUT RIGHT NOW THAT BREAKS THE ehb-client WHEN TRYING UPDATE AN EXTERNAL_RECORD

    def clean(self):
            try:
                ers = ExternalRecord.objects.filter(
                    external_system=self.external_system).filter(
                    record_id=self.record_id).filter(
                    path=self.path
                )

                for er in ers:
                    if er.pk != self.pk:  # if they are equal then we are modifying this record
                        raise ValidationError(self.cleanmsg)

            except ExternalSystem.DoesNotExist:
                pass  # The exteranlSystem field validation will handle this

    def responseFieldDict(self):
        response = {}

        for k in self.__dict__.keys():
            if not k.startswith('_'):
                response[k] = (str(self.__dict__.get(k)))

        try:
            response['relation_id'] = self.relation.desc
        except:
            response['relation_id'] = 'Proband'

        return response

    def __unicode__(self):
        return "{0}, {1} IN {2}".format(
            self.subject.last_name,
            self.subject.first_name,
            self.external_system.name
        )


class Relation(CreatedModified):

    id = models.AutoField(primary_key=True)
    typ = models.CharField(
        max_length=255,
        verbose_name="Relation Type",
        choices=[
            ('label', 'Label'),
            ('file', 'File'),
            ('familial', 'Familial'),
            ('diagnosis', 'Diagnosis')
        ],
        default='Label'
    )
    desc = models.CharField(max_length=255, verbose_name="Descriptor", null=True, blank=True)

    def __unicode__(self):
        return "<{0}> {1}".format(self.typ, self.desc)


class ExternalRecordRelation(CreatedModified):
    id = models.AutoField(primary_key=True)
    external_record = models.OneToOneField(ExternalRecord, related_name='external_record', default=None, null=True)
    related_record = models.OneToOneField(ExternalRecord, related_name='related_record', default=None, null=True)
    relation_type = models.ForeignKey(Relation)

    def __unicode__(self):
        return "{0}, {1} ({5}) related to {2}, {3} ({6}) -- Type: {4}".format(
            self.external_record.subject.last_name,
            self.external_record.subject.first_name,
            self.related_record.subject.last_name,
            self.related_record.subject.first_name,
            self.relation_type,
            self.external_record.external_system.name,
            self.related_record.external_system.name
        )

class ExternalRecordGroup(CreatedModified):

    external_records = models.ManyToManyField(ExternalRecord)
    group = models.ForeignKey(Group, unique=True)

    class Meta(CreatedModified.Meta):
        ordering = ['group']

class SubjectValidation(models.Model):

    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization)
    regex = models.CharField(max_length=70)

    def __unicode__(self):
        return "{0} Subject validation".format(self.organization.name)

    class Meta:
        app_label = u'core'
