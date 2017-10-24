from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from core.models.identities import ExternalRecord, ExternalRecordLabel

class Migration(SchemaMigration):

    def forwards(self, orm):
        try:
            erl = ExternalRecordLabel.objects.get(pk=1)
        except:
            ExternalRecordLabel(
                id=1,
                label=''
            ).save()
            erl = ExternalRecordLabel.objects.get(pk=1)

        for er in ExternalRecord.objects.all():
            if not hasattr(er, 'label'):
                er.label = erl
                er.save()


    def backwards(self, orm):
        # Deleting model 'ExternalRecordLabel'
        pass
