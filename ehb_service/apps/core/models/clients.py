'''
Created on Jun 13, 2011

@author: masinoa
'''

from django.db import models

__all__ = ('MachineClient',)

class MachineClient(models.Model):

    class Meta(object):
        app_label = u'core'
        unique_together=('ip_address', 'host_name')

    ip_address = models.GenericIPAddressField(verbose_name = 'Remote Host IP Address')
    host_name= models.CharField(max_length=255, verbose_name = 'Name', blank=True, default = '')

    def __unicode__(self):
        return self.ip_address
