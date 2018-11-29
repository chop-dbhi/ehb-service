import struct
import zlib
import logging
import base64

from Crypto.Cipher import AES, DES

from core.encryption.EncryptionServiceBase import EncryptionService
from core.encryption.Exceptions import CheckSumFailure

log = logging.getLogger(__name__)


class AESEncryption(EncryptionService):

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

        # convert string to bytes.
        key = key.encode("utf8")
        enc = AES.new(key, self.mode, iv=b'0123456789abcdef')

        if self.use_checksum:
            # struct pack returns a byte object within the values of 'i'
            # of zlib, which is a 32 bit representation of data that we add
            # onto our data
            data += struct.pack("I", zlib.crc32(data))

        # return encrypted data which is utf8 encoded (bytes)
        enrypted_data = enc.encrypt(data)
        print ("this is the encrytped data")
        print (enrypted_data)
        return enrypted_data
        # return  enc.encrypt(data)



    def decrypt(self, edata, key, **kwargs):
        if self.auto_correct_key_length:
            key = self._correct_key_length(key)

        # convert string to bytes
        key = key.encode("utf8")
        enc = AES.new(key, self.mode, iv=b'0123456789abcdef')
        data = enc.decrypt(edata)

        if self.use_checksum:
            cs, data = (data[-4:], data[:-4])
            # cs is the extra bytes that we added to data before
            # (see encrypt for more info on what this is)
            # if the byte object of the 32 bit representation of data
            # doesn't equal cs, we raise error
            if not cs == struct.pack("I", zlib.crc32(data)):
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
