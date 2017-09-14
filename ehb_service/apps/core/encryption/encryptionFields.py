import datetime
import re
import binascii
import random
import string
import logging

from django import forms
from django.db import models
from django.forms import fields
from django.utils.encoding import force_unicode, smart_str
from south.modelsinspector import add_introspection_rules

from core.encryption.Factories import FactoryEncryptionServices as efac

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
            max_length, usl = self._max_db_length(unique, user_specified_length)
            self.user_specified_max_length = usl
            kwargs['max_length'] = max_length

        models.Field.__init__(self, *args, **kwargs)

    def _max_db_length(self, unique, user_specified_length):

        def encrypted_length(usl):
            ml = usl + 2
            modulus = ml % self.block_size
            if modulus > 0:
                ml += self.block_size - modulus
            return (ml + self.aes.check_sum_length()) * 2

        if unique:
            l = encrypted_length(user_specified_length)
            while(l > 255):
                user_specified_length -= 1
                l = encrypted_length(user_specified_length)
            return (l, user_specified_length)

        else:
            return (encrypted_length(user_specified_length), user_specified_length)

    def _padding_length(self, value):
        # The total length of the encrypted value including zero byte must be even in order
        # to convert to hex
        return self.block_size - ((len(value)+2) % self.block_size) + 2

    def _semi_random_padding_string(self, length):
        '''
        Would like to add some random padding, but it needs to be reproducable
        for values of the same length to ensure uniqueness requirements are satisfied,
        ie two values of the same length need to have the same padding so that
        IF the field is required to be unique it can be compared to other values in the db
        '''
        mod = max(length % 10, 1)
        seed = 0
        temp = length
        for i in range(7):
            seed += (10**i)*mod
            temp += 1
            mod = max(temp % 10, 1)
        random.seed(seed)
        return ''.join([random.choice(string.printable) for i in range(length)])

    def _split_byte(self):
        return '\0'

    def _is_encrypted(self, value, key):
        '''
        If value contains any non hex symbols or its length is odd, then it was
        not encrypted because the encrypted values are all converted to ascii hex
        before storing in db using the binascii.a2b_hex method which only operates
        on even length values
        '''

        if re.search('[^0-9a-f]', value) or (len(value) % 2) != 0:
            return False
        # Have the encryption service verify if this is encrypted
        else:
            return self.aes.is_encrypted(binascii.a2b_hex(value), key)

    def to_python(self, value):
        """Converts the input value into the expected Python data type, raising
        django.core.exceptions.ValidationError if the data can't be converted.
        Returns the converted value. Subclasses should override this."""
        log.debug('in BaseField.to_python - input value: {0}'.format(value))
        length = len(value.strip())
        log.debug('in BaseField.to_python - len(value.strip()) = {0}'.format(length))
        if len(value.strip()) == 0:
            return value
        log.debug('in BaseField.to_python - self.use_encryption: {0}'.format(self.use_encryption))
        if self.use_encryption:
            key = self.akms.get_key()
            encrypted = self._is_encrypted(value, key)
            log.debug('in BaseField.to_python - self._is_encrypted: {0}'.format(encrypted))
            if self._is_encrypted(value, key):
                return force_unicode(self.aes.decrypt(binascii.a2b_hex(value), key).split(self._split_byte())[0])
            else:
                log.debug('in BaseField.to_python - value if use_encrypted and _is_encrypted is true: {0}'.format(value))
                return value
        else:
            log.debug('in BaseField.to_python - value if use_encryption is false: {0}'.format(value))
            return value

    def get_db_prep_value(self, value, connection=None, prepared=False):
        '''
        Perform preliminary non-db specific value checks and conversions:
        convert value from unicode to full byte string, otherwise encryption
        service may fail according to django docs this is different than str(value)
        and necessary to django internals

        https://docs.djangoproject.com/en/dev/ref/unicode/
        '''
        log.debug('BaseField.get_db_prep_value - input value: {0}'.format(value))
        log.debug('BaseField.get_db_prep_value - input connection: {0}'.format(connection))
        log.debug('BaseField.get_db_prep_value - input prepared: {0}'.format(prepared))
        length = len(value.strip())
        log.debug('BaseField.get_db_prep_value - len(value.strip()) : {0}'.format(length))
        if len(value.strip()) == 0:
            return value

        value = smart_str(value, encoding='utf-8', strings_only=False, errors='strict')
        if self.use_encryption:

            key = self.akms.get_key()

            if value and not self._is_encrypted(value, key):
                log.debug("BaseField.get_db_prep_value - input value is not encrypted")
                pad_length = self._padding_length(value)
                if pad_length > 0:
                    value += self._split_byte() + self._semi_random_padding_string(pad_length-1)
            value = self.aes.encrypt(value, key)

            if len(value) % 2 != 0:
                # Some encryption services add a checksum byte which throws off the pad_length
                log.debug("BaseField.get_db_prep_value - input value is encrypted using checksum")
                value += self._split_byte()
            value = binascii.b2a_hex(value)
        log.debug('BaseField.get_db_prep_value - return value: {0}'.format(value))
        return value


class EncryptCharField(BaseField):

    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return 'CharField'

    def formfield(self, **kwargs):
        "Returns a django.forms.Field instance for this database Field."
        defaults = {'max_length': self.max_length}
        defaults.update(kwargs)

        return super(EncryptCharField, self).formfield(**defaults)

    def get_db_prep_value(self, value, connection=None, prepared=False):
        log.debug('EncryptCharField.get_db_prep_value - input value: {0}'.format(value))
        log.debug('EncryptCharField.get_db_prep_value - input connection: {0}'.format(connection))
        log.debug('EncryptCharField.get_db_prep_value - input prepared: {0}'.format(prepared))
        log.debug('EncryptCharField.get_db_prep_value - self.use_encryption: {0}'.format(self.use_encryption))
        if self.use_encryption:
            key = self.akms.get_key()
            encrypted = self._is_encrypted(value, key)
            log.debug('EncryptCharField.get_db_prep_value - self._is_encrypted(value, key): {0}'.format(encrypted))
            if value and not self._is_encrypted(value, key):
                if len(value) > self.user_specified_max_length:
                    raise ValueError(
                        "Field value longer than max allowed: {0} > {1}".format(
                            str(len(value)),
                            self.user_specified_max_length
                        )
                    )

        return super(EncryptCharField, self).get_db_prep_value(value, connection=connection, prepared=prepared)


class EncryptDateField(BaseField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10  # YYYY:MM:DD format
        super(EncryptDateField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def formfield(self, **kwargs):
        defaults = {'widget': forms.DateInput, 'form_class': forms.DateField}
        defaults.update(kwargs)

        return super(EncryptDateField, self).formfield(**defaults)

    def to_python(self, value):
        log.debug('in EncryptDateField.to_python - input value: {0}'.format(value))
        dv = None

        if value in fields.EMPTY_VALUES:
            dv = value
        elif isinstance(value, datetime.date):
            dv = value
        else:
            input_text = super(EncryptDateField, self).to_python(value)
            dv = datetime.date(*[int(x) for x in input_text.split(':')])
        log.debug('in EncryptDateField.to_python - return value dv: {0}'.format(dv))
        return dv

    def get_db_prep_value(self, value, connection=None, prepared=False):
        log.debug('EncryptDateField.get_db_prep_value - input value: {0}'.format(value))
        log.debug('EncryptDateField.get_db_prep_value - input connection: {0}'.format(connection))
        log.debug('EncryptDateField.get_db_prep_value - input prepared: {0}'.format(prepared))
        dt = value.strftime('%Y:%m:%d') if value else None
        log.debug('EncryptDateField.get_db_prep_value - dt: {0}'.format(dt))
        return super(EncryptDateField, self).get_db_prep_value(dt, connection=connection, prepared=prepared)

# Basic Introspection rules so South plays nice
rule_char = [
    (
        (models.CharField,),
        [],
        {},
    )
]
rule_date = [
    (
        (models.DateField,),
        [],
        {},
    )
]

add_introspection_rules(rule_char, ["^core\.encryption\.encryptionFields\.EncryptCharField"])
add_introspection_rules(rule_date, ["^core\.encryption\.encryptionFields\.EncryptDateField"])
