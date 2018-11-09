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
            return bytes( value, encoding = 'latin-1' )

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


        #
        #
        #         unicode_value = str( value, 'utf8', 'replace')
        #         print ("this is unicode value")
        #         print (unicode_value)
        #         ord_value= []
        #         [ord_value.append(ord(u))for u in unicode_value]
        #         string_value =''
        #         for o in ord_value:
        #             if o == 65533:
        #                 string_value += '?'
        #             else:
        #                 string_value += chr(o)
        #         print ("printing ord value")
        #         [print (ord(s)) for s in string_value]
        #         return string_value
        #     return (unicode_value)
        # return str( value )

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

        print ("this is key after corrected keylength")
        print (key)

        key = self.ToBytes(key)
        print ("this is key after tobytes")
        print (key)

        enc = AES.new(key, AES.MODE_CFB)
        print ("this is enc")
        print (enc)

        data = self.ToBytes(data)
        print ("this is zlibcrc32")
        print (zlib.crc32(data))
        if self.use_checksum:
            data += struct.pack("i", zlib.crc32(data))

            print ("this is data after checksum")
            print (data)
            print ("this is decoded data with latin1")
            print (data.decode("latin-1"))

        # encrypted_bytes =  base64.b64encode(enc.encrypt(data))
        # print ("this is encryoted bytes")
        # print (base64.b64decode(encrypted_bytes))
        theanswer = "KN+p\x80\xac\xe23IX"
        answerbytes=self.ToBytes(theanswer)
        print ("answer in bytes")
        print (answerbytes)
        print (answerbytes.decode("latin-1"))
        print ("asnwer in ord")
        for a in theanswer:
            print (type(ord(a)))
        print ("asnwerbytes in ord")
        for a in answerbytes:
            print (type(a))

        encrypted_answer = enc.encrypt(data)
        for myint in encrypted_answer:
            char = chr(myint)
            print (char)

        # decoded_answer = encrypted_answer.decode('latin-1')
        return encrypted_answer

        # return ((enc.encrypt(data).decode("utf-8")))


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
