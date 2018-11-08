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
        # This is tricky. On py2, the bytes type from builtins (from python-future) is
        # a subclass of str. So all of the following are true:
        # isinstance(str(), bytes)
        #   isinstance(bytes(), str)
        # But they don't behave the same in one important aspect: iterating over a
        # bytes instance yields ints, while iterating over a (raw, py2) str yields
        # chars. We want consistent behavior so we force the use of bytes().
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
            if PY2:
                return bytes( value.encode( 'utf8' ), encoding = 'utf8' )
            else:
                return bytes( value, encoding = 'utf8' )

        # This is meant to catch `int` and similar non-string/bytes types.
        return ToBytes( str( value ) )

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

        key = self.ToBytes(key)

        enc = AES.new(key, AES.MODE_CFB)

        data_encode = data.encode('utf-8')
        print (zlib.crc32(data))
        if self.use_checksum:
            data += struct.pack("i", zlib.crc32(data))



        key_encode = key.encode('utf-8')
        data_encode = data.encode('utf-8')
        # key_encode = base64.b64encode(key.encode('utf-8',errors = 'strict'))
        # data_encode = base64.b64encode(data.encode('utf-8',errors = 'strict'))

        enc = AES.new(key_encode, self.mode)
        # data = str.encode(data)

        if self.use_checksum:
            data_encode += struct.pack("i", zlib.crc32(data_encode))
            print (type(data_encode))
            print (data_encode)
        data_encode = data_encode.decode('utf-8', 'ignore')
        # print ("this data decoded")
        # print (type (data))
        # print(data)
        # result = enc.encrypt(str.encode(data))
        # print (result)
        # data = map(ord, data)
        # data = str.encode(data)
        # iv = b64encode(enc.iv).decode('utf-8')
        # data_bytes = enc.encrypt(data)
        # print (data_bytes)
        # print (data_bytes)
        # enc_2 = AES.new(b'1234561111111111', self.mode)
        # enc_secret = enc.encrypt(b'secret')
        # print ("this is encrypted secret")
        # print (enc_secret)
        # dec_secret = enc_secret.decode()
        # print ("this is decoded secret")
        # print (dec_secret)
        return (enc.encrypt(data_encode)).decode('utf-8', 'ignore')

        # return b64encode(data_bytes).decode('utf-8')
        # return enc.encrypt(data)

    def decrypt(self, edata, key, **kwargs):
        if self.auto_correct_key_length:
            key = self._correct_key_length(key)

        enc = AES.new(key.encode("utf8"), self.mode)
        data = enc.decrypt(edata.encode("utf8"))

        if self.use_checksum:
            cs, data = (data[-4:], data[:-4])
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
