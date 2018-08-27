'''
Created on Jun 8, 2011

@author: masinoa
'''
import re

from django.forms import ModelForm
from django.forms.util import ErrorList
from models.identities import Subject, ExternalRecord, ExternalSystem, \
    Organization, Group, ExternalRecordRelation, PedigreeSubjectRelation
<<<<<<< HEAD

=======
>>>>>>> adding functionality to add a subject relationship through the ehb api


class SubjectForm(ModelForm):

    def clean(self):
        # Run subject validation if it exists
        org = self.cleaned_data.get('organization')
        # If there is no org simply return data.
        # Error will be caught downstream
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
        fields = "__all__"
        model = Subject


class ExternalRecordForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = ExternalRecord


class ExternalRecordRelationForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = ExternalRecordRelation


class OrganizationForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Organization


class GroupForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Group


class ExternalSystemForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = ExternalSystem

    def save(self, commit=True):
        '''Currently this method ensures that the save_m2m() form method is skipped.
        May attempt to fix this later.'''
        m = super(ExternalSystemForm, self).save(commit=False)
        if commit:
            m.save()
        return m

    '''This version of save as well as new is_valid and errors methods will be
    needed if the POST method for ExternalSystemResource is going to support
    the addition of ExternalRecords at the time a new ExternalSystem is created
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
                            er = ExternalRecord(
                                subject=s,external_system=m, record_id=rid)
                            er.save()
                        except Exception:
                            pass
            return m
        except Exception as err:
            print err'''


class PedigreeSubjectRelationForm(ModelForm):
    def clean(self):
        validation = {}
        validation['subject_1'] = self.cleaned_data.get('subject_1')
        validation['subject_2'] = self.cleaned_data.get('subject_2')
        validation['subject_1_role'] = self.cleaned_data.get('subject_1_role')
        validation['subject_1_role'] = self.cleaned_data.get('subject_2_role')
        for item in validation:
            if not item:
                self._errors[item] = ErrorList(
                    ["Relationship does not meet validation rules for this organization."]
                )
        # prevent two parents to connect. this connection should be mapped through siblings
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-parent" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-parent"):
            self._errors["both relationhip Roles cannot both be parents"] = ErrorList(
                ["cannot create a relationship between two parents, must be connected through child."]
            )
        # prevent a full sibling and a half sibling to be connected.
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-sibling" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-half-sibling"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between half sibling and whole sibling."]
            )
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-half-sibling" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-sibling"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between half sibling and whole sibling."]
            )
        # prevent half sibling and a parent from being connected
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-half-sibling" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-parent"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between half sibling and parent."]
            )
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-parent" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-half-sibling"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between half sibling and parent."]
            )
        # prevent sibling and parent from being connected
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-parent" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-sibling"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between sibling and Parent."]
            )
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-sibling" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-parent"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between sibling and parent."]
            )
        # prevent sibling and child from being connected
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-sibling" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-child"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between sibling and Child."]
            )
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-child" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-sibling"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between sibling and child."]
            )
        # prevent half sibling and child from being connected
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-half-sibling" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-child"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between half sibling and child."]
            )
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-child" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-half-sibling"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between half sibling and child."]
            )
        # prevent two children from being connected, should be connected through siblings
        if (self.cleaned_data.get('subject_1_role').typ.lower() == "familial-child" and
                self.cleaned_data.get('subject_2_role').typ.lower() == "familial-child"):
            self._errors["Cannot mix sibling types"] = ErrorList(
                ["cannot create a relationship between two children, must be siblings."]
            )

        return self.cleaned_data

    class Meta:
        fields = "__all__"
        model = PedigreeSubjectRelation
