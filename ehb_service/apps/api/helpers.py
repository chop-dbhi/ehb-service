import logging
import xml.dom.minidom as xml
from resources.constants import ErrorConstants
from core.models.identities import ExternalRecord, Subject

log = logging.getLogger(__name__)


class FormHelpers(object):

    @staticmethod
    def errorDict(formerrors):
        """Given the object formerrors of type django.forms.util.ErrorDict with assumed form
       <ul class="errorlist><li>MODEL_FIELD_NAME<ul class="errorlist"><li>ERROR TEXT</li></ul></li></ul>
       this returns a dictionary with entries of the form "MODEL_FIELD_NAME":[ERROR TEXT,..]"""
        x = str(formerrors)
        d = xml.parseString(x)
        ul = d.documentElement.childNodes
        errors = {}
        for li in ul:
            for c in li.childNodes:
                el = []
                n = c.nodeName
                if(n == '#text'):
                    fld = c.nodeValue
                elif(n == 'ul'):
                    for cli in c.getElementsByTagName('li'):
                        el.append(cli.firstChild.nodeValue)
                    errors[fld] = el
        return errors

    @staticmethod
    def jsonErrors(formerrors):
        """Given the object formerrors of type django.forms.util.ErrorDict with assumed form
       <ul class="errorlist><li>MODEL_FIELD_NAME<ul class="errorlist"><li>ERROR TEXT</li></ul></li></ul>
       this returns a list with json formated errors"""
        errdict = FormHelpers.errorDict(formerrors)
        errl = []
        for k in errdict.keys():
            v = errdict.get(k)
            e = v[0]

            if e == Subject.cleanmsg:
                v = ErrorConstants.ERROR_SUBJECT_ORG_ID_EXISTS
            elif e == 'This field is required.':
                v = ErrorConstants.ERROR_FIELD_REQUIRED
            elif e == 'Enter a valid date.':
                v = ErrorConstants.ERROR_INVALID_DATE_FORMAT
            elif e == 'External system with this External System Name already exists.':
                v = ErrorConstants.ERROR_EXTERNAL_SYSTEM_NAME_EXISTS
            elif e == ExternalRecord.cleanmsg:
                v = ErrorConstants.ERROR_RECORD_ID_ALREADY_IN_EXTERNAL_SYSTEM
            elif e == 'Select a valid choice. That choice is not one of the available choices.':
                v = ErrorConstants.ERROR_INVALID_CHOICE
            elif e == 'External system with this External System URL already exists.':
                v = ErrorConstants.ERROR_EXTERNAL_SYSTEM_URL_EXISTS
            elif e == 'Organization with this Name already exists.':
                v = ErrorConstants.ERROR_ORGANIZATION_NAME_EXISTS
            elif e == 'Group with this Group Name already exists.':
                log.error("Subject with this Group Name already exists in the EHB.")
                v = ErrorConstants.ERROR_GROUP_NAME_EXISTS
            elif e == 'Subject identifier does not meet validation rules for this organization.':
                log.error("Subject identifier does not meet validation rules for this organization.")
                v = ErrorConstants.ERROR_SUBJECT_ID_NOT_VALID
                log.error("Subject id not valid")
            else:
                v = ErrorConstants.ERROR_UNKNOWN

            errl.append({k: v})

        return errl

    @staticmethod
    def processFormJsonResponse(form, response, valid_dict=None, invalid_dict=None, keys_from_response_dict=None):

        if form.is_valid():
            m = form.save()
            created = None
            modified = None
            isCreatedModified = False

            for c in type(m).__bases__:
                if c.__name__ == 'CreatedModified':
                    isCreatedModified = True

            if isCreatedModified:
                md = m.created

                created = "{0}-{1}-{2} {3}:{4}:{5}".format(
                    str(md.year),
                    str(md.month),
                    str(md.day),
                    str(md.hour),
                    str(md.minute),
                    str(md.second)
                )
                md = m.modified
                modified = "{0}-{1}-{2} {3}:{4}:{5}".format(
                    str(md.year),
                    str(md.month),
                    str(md.day),
                    str(md.hour),
                    str(md.minute),
                    str(md.second)
                )
            if created and modified:
                response_dict = {
                    "id": str(m.pk),
                    "success": True,
                    "modified": modified,
                    "created":
                    created
                }
            else:
                response_dict = {"id": str(m.pk), "success": True}

            if valid_dict:
                for key in valid_dict.keys():
                    response_dict[key] = valid_dict.get(key)

            if keys_from_response_dict:
                for key in keys_from_response_dict:
                    response_dict[key] = m.__dict__.get(key)
        else:

            log.error('Error in form validation')
            response_dict = {"success": False, "errors": FormHelpers.jsonErrors(form.errors)}
            if invalid_dict:
                for key in invalid_dict.keys():
                    response_dict[key] = invalid_dict.get(key)
        response.append(response_dict)

        return response_dict
