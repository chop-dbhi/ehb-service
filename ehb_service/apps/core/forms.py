'''
Created on Jun 8, 2011

@author: masinoa
'''
import re

from django.forms import ModelForm
from django.forms.util import ErrorList
from models.identities import Subject, ExternalRecord, ExternalSystem, Organization, Group

class SubjectForm(ModelForm):

    def clean(self):
        # Run subject validation if it exists
        org = self.cleaned_data.get('organization')
        # If there is no org simply return data. Error will be caught downstream
        if not org:
            return self.cleaned_data
        validations = org.subjectvalidation_set.all()
        if validations:
            for check in validations:
                sid = self.cleaned_data.get('organization_subject_id')
                valid = re.match(check.regex, sid)
                if not valid:
                    self._errors["subject"] = ErrorList(["Subject identifier does not meet validation rules for this organization."])
        return self.cleaned_data
    class Meta:
        model = Subject

class ExternalRecordForm(ModelForm):
    class Meta:
        model = ExternalRecord

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization

class GroupForm(ModelForm):
    class Meta:
        model = Group

class ExternalSystemForm(ModelForm):
    class Meta:
        model = ExternalSystem

    def save(self, commit=True):
        '''Currently this method ensures that the save_m2m() form method is skipped.
        May attempt to fix this later.'''
        m = super(ExternalSystemForm, self).save(commit=False)
        if commit:
            m.save()
        return m

    '''This version of save as well as new is_valid and errors methods will be needed
     if the POST method for ExternalSystemResource is going to support the
     addition of ExternalRecords at the time a new ExternalSystem is created
     def save(self,commit=True):

        try:
            m = super(ExternalSystemForm,self).save(commit=False)
            if not commit:
                return m
            #m.save()
            print self.data
            if(self.data.has_key('subjects')):
                for tpl in self.data.get('subjects'):
                    sid = tpl.get('id',None)
                    rid = tpl.get('record_id',None)
                    if sid != None and rid !=None:
                        try:
                            s=Subject.objects.get(pk=sid)
                            er = ExternalRecord(subject=s,external_system=m, record_id=rid)
                            er.save()
                        except Exception:
                            pass
            return m
        except Exception as err:
            print err'''
