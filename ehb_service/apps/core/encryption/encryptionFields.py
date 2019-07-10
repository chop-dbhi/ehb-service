import datetime
import re
import binascii
import random
import string
import logging

from django import forms
from django.db import models
from django.forms import fields
from django.utils.encoding import force_text, smart_bytes
import sys

from core.encryption.Factories import FactoryEncryptionServices as efac
from core.encryption.encryptionFieldsBase import encryptionBaseMethods as ebm
log = logging.getLogger(__name__)


class BaseField(models.Field):

    def __init__(self, *args, **kwargs):

        # Get the active encryption and key management services, if any
        self.use_encryption = efac.use_encryption()
        self.aes = efac.active_encryption_service() if self.use_encryption else None
        self.akms = efac.active_key_management_service() if self.use_encryption else None
        self.block_size = self.aes.block_size() if self.use_encryption else None

        # Need to adjust the max length supplied in the user's field args to account for
        # cipher block size and padding

        if self.use_encryption:
            user_specified_length = kwargs.get('max_length', 20)
            unique = kwargs.get('unique', False)
            max_length, usl = ebm._max_db_length (unique, user_specified_length, self.block_size, self.aes)
            self.user_specified_max_length = usl
            kwargs['max_length'] = max_length

        models.Field.__init__(self, *args, **kwargs)


    def _is_encrypted(self, value, key, iv):
        '''
        If value contains any non hex symbols or its length is odd, then it was
        not encrypted because the encrypted values are all converted to ascii hex
        before storing in db using the binascii.a2b_hex method which only operates
        on even length values
        '''
        hexValues = True
        # test to see if value is a hexadecimal
        # get rid of extra spaces
        value = value.strip()
        try:
            int(value, 16)
        except ValueError:
            hexValues = False

        if hexValues == False or (len(value) % 2) != 0 :
            return False
        else:
            # Have the encryption service verify if this is encrypted
            return self.aes.is_encrypted(binascii.a2b_hex(value), key, iv)


    def get_decrypted_value (self, value):
        """Converts the input value into the expected Python data type by
        dehexifying and decrypting the value. It raises
        django.core.exceptions.ValidationError if the data can't be converted.
        Returns the converted value. """

        if len(value.strip()) == 0:
            return value

        if self.use_encryption:
            key = self.akms.get_key()
            iv = self.akms.get_iv()
            if self._is_encrypted(value, key, iv):
                # dehexify and decrypt
                decrypted_value = self.aes.decrypt(binascii.a2b_hex(value), key, iv)
                # get rid of extra bytes
                decrypted_value = decrypted_value.split(ebm._split_byte())
                # forcing to string text
                decrypted_value = force_text(decrypted_value[0])
                return decrypted_value
            else:
                return value
        else:
            return value

    def get_encrypted_value (self, value, connection=None, prepared=False):
        '''
        Perform preliminary non-db specific value checks and conversions:
        convert value from unicode to full byte, encrypted string, otherwise encryption
        service may fail according to django docs this is different than str(value)
        and necessary to django internals

        https://docs.djangoproject.com/en/dev/ref/unicode/
        '''

        if value is None:
            return value

        if len(value.strip()) == 0:
            return value

        # convert string value to bytes
        value = smart_bytes(value, encoding='utf-8', strings_only=False, errors='strict')

        if self.use_encryption:
            key = self.akms.get_key()
            iv = self.akms.get_iv()
            if value and not self._is_encrypted(value, key, iv):
                if len(value) > self.user_specified_max_length:
                    raise ValueError(
                        "Field value longer than max allowed: {0} > {1}".format(
                            str(len(value)),
                            self.user_specified_max_length
                        )
                    )

                pad_length = ebm._padding_length(value, self.block_size)
                if pad_length > 0:
                    value += ebm._split_byte() + ebm._semi_random_padding_string(pad_length-1)

            value = self.aes.encrypt(value, key, iv)

            if len(value) % 2 != 0:
                # Some encryption services add a checksum byte which throws off the pad_length
                value += ebm._split_byte()
            value = binascii.b2a_hex(value)

            # need to decode to string to store in database
            value = value.decode("utf8")
        return value


class EncryptCharField(BaseField):

    # from_db_value is called in all circumstances when
    # the data is loaded from the database
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return self.get_decrypted_value(value)

    def get_internal_type(self):
        return 'CharField'

    def deconstruct(self):
        name, path, args, kwargs = super(EncryptCharField, self).deconstruct()
        kwargs["max_length"] = 255
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        "Returns a django.forms.Field instance for this database Field."
        defaults = {'max_length': self.max_length}
        defaults.update(kwargs)

        return super(EncryptCharField, self).formfield(**defaults)

    # method to convert data to encrypted format before they are stored in database
    def get_db_prep_value(self, value, connection=None, prepared=False):

        if self.use_encryption:
            key = self.akms.get_key()
            iv = self.akms.get_iv()
            if value and not self._is_encrypted(value, key, iv):
                if len(value) > self.user_specified_max_length:
                    raise ValueError(
                        "Field value longer than max allowed: {0} > {1}".format(
                            str(len(value)),
                            self.user_specified_max_length
                        )
                    )
        return self.get_encrypted_value(value, connection=connection, prepared=prepared)


class EncryptDateField(BaseField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10  # YYYY:MM:DD format
        super(EncryptDateField, self).__init__(*args, **kwargs)

    #  from_db_value is called in all circumstances
    # when the data is loaded from the database
    def from_db_value(self, value, expression, connection, context):
        dv = None
        if value in fields.EMPTY_VALUES:
            dv = value
        elif isinstance(value, datetime.date):
            dv = value
        else:
            input_text = self.get_decrypted_value(value)
            try:
                dv = datetime.date(*[int(x) for x in input_text.split(':')])
            except ValueError:
                log.error("Decryption failed - old ehb values need to be updated")
        return dv

    def deconstruct(self):
        name, path, args, kwargs = super(EncryptDateField, self).deconstruct()
        kwargs["max_length"] = 10
        return name, path, args, kwargs

    def get_internal_type(self):
        return 'CharField'

    def formfield(self, **kwargs):
        defaults = {'widget': forms.DateInput, 'form_class': forms.DateField}
        defaults.update(kwargs)
        return super(EncryptDateField, self).formfield(**defaults)

    # for django custom fields, to_python() is called by deserialization
    # and during the clean() method used from forms
    def to_python(self, value):
        dv = None

        if value in fields.EMPTY_VALUES:
            dv = value
        elif isinstance(value, datetime.date):
            dv = value
        else:
            input_text = self.get_decrypted_value(value)
            try:
                dv = datetime.date(*[int(x) for x in input_text.split('-')])
            except:
                dv = datetime.date(*[int(x) for x in input_text.split(':')])

        return dv

    # method to convert data to encrypted format before they are stored in database
    def get_db_prep_value(self, value, connection=None, prepared=False):
        if isinstance(value, datetime.date):
            value = value.strftime('%Y:%m:%d')
        return self.get_encrypted_value(value, connection=connection, prepared=prepared)
