import struct
import zlib
import logging
import base64

from Crypto.Cipher import AES, DES

from core.encryption.EncryptionServiceBase import EncryptionService
from core.encryption.Exceptions import CheckSumFailure

log = logging.getLogger(__name__)


class AESEncryption(EncryptionService):

    # Consistently returns the new bytes() type from python-future. Assumes incoming
    # strings are either UTF-8 or unicode (which is converted to UTF-8).
    def ToBytes(self, value ):
        if not value:
            return bytes()
        if type( value ) == bytes:
            return value
        # This is meant to catch Python 2's native str type.
        if isinstance( value, bytes ):
            return bytes( value, encoding = 'utf8' )

        if isinstance( value, str ):
        # On py2, with `from builtins import *` imported, the following is true:
        #
        #   bytes(str(u'abc'), 'utf8') == b"b'abc'"
        #
        # Obviously this is a bug in python-future. So we work around it. Also filed
        # upstream at: https://github.com/PythonCharmers/python-future/issues/193
        # We can't just return value.encode( 'utf8' ) on both py2 & py3 because on
        # py2 that *sometimes* returns the built-in str type instead of the newbytes
        # type from python-future.
            # if PY2:
            #     return bytes( value.encode( 'utf8' ), encoding = 'utf8' )
            # else:
            return bytes( value, encoding = 'latin-1' )

        # This is meant to catch `int` and similar non-string/bytes types.
        return ToBytes( str( value ) )

    # Returns a unicode type; either the new python-future str type or the real
    # unicode type. The difference shouldn't matter.
    def ToUnicode(self, value, encryption=False ):
        if not value:
            return str()
        if isinstance( value, str ):
            return value
        if isinstance( value, bytes ):
            # All incoming text should be utf8
            try:
                unicode_value = str( value, 'utf8' )
            except UnicodeDecodeError:

                if encryption==True:
                    return_value = []
                    for b in value:
                        try:
                            print ("thisis b")
                            print (b)
                            print ("this is char b")
                            print (chr(b))
                            # char_s= (map(chr, bytes))
                            # char_s = str((), 'utf8')
                            # return_value.append(char_s)
                        except UnicodeDecodeError:
                            return_value.append(s)
                    print ("this is return value")
                    print (return_value)
                    return return_value
            return unicode_value
        return str(value)

    def configure(self, **kwargs):
        self.mode = kwargs.get('mode', AES.MODE_CFB)
        self.auto_correct_key_length = kwargs.get('auto_correct_key_length', True)
        self.use_checksum = kwargs.get('use_checksum', True)
        self.padding = kwargs.get('padding', '}')

    def block_size(self, **kwargs):
        return AES.block_size

    def _correct_key_length(self, key):
        l = len(key)
        if l > AES.block_size:
            return key[0:AES.block_size]
        elif l < AES.block_size:
            return key + (AES.block_size-l)*self.padding
        else:
            return key

    def encrypt(self, data, key, **kwargs):
        if self.auto_correct_key_length:
            key = self._correct_key_length(key)

        testenc = AES.new(b'key}}}}}}}}}}}}}', self.mode)
        testencryptionbytes = testenc.encrypt(b'testdata')
        iv = base64.b64encode(testenc.iv).decode('utf8')
        testencryption=base64.b64encode(testencryptionbytes).decode("utf8")

        print ("this is test encryption")
        print (testencryption)

        # convert string to bytes
        key = key.encode("utf8")
        data = data.encode("utf8")

        enc = AES.new(key, AES.MODE_CFB)

        if self.use_checksum:
            data += struct.pack("i", zlib.crc32(data))

        encrypted_data_bytes = enc.encrypt(data)
        iv = base64.b64encode(enc.iv).decode("utf8")
        encrypted_data = b64encode(encrypted_data_bytes).decode('utf-8')
        
        return encrypted_data


    def decrypt(self, edata, key, **kwargs):
        print ("this is edata")
        print (edata)
        print ("this is edata encoded")
        print (edata.encode("latin1"))
        if self.auto_correct_key_length:
            key = self._correct_key_length(key)

        enc = AES.new(key.encode("utf8"), self.mode)
        data = enc.decrypt(edata.encode("utf8"))

        if self.use_checksum:
            cs, data = (data[-4:], data[:-4])
            print ("this is cs")
            print (cs.decode("latin1"))
            print ("this is data")
            print (data.decode("latin1"))
            if not cs == struct.pack("i", zlib.crc32(data)):
                raise CheckSumFailure('Checksum failed in decrypt')
        return data

    def is_encrypted(self, edata, key, **kwargs):
        # if checksum is not used, there is in general no way to know if edata is encrypted
        if self.use_checksum:
            try:
                self.decrypt(edata, key)
                return True
            except CheckSumFailure:
                log.error("Checksum failure. Unable to decrypt")
                return False

    def check_sum_length(self, **kwargs):
        if self.use_checksum:
            return 4
        else:
            return 0
