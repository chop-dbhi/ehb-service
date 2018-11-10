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

        # convert string to bytes
        key = key.encode("utf8")
        data = data.encode("utf8")

        enc = AES.new(key, AES.MODE_CFB)

        if self.use_checksum:
            data += struct.pack("i", zlib.crc32(data))

        encrypted_data_bytes = enc.encrypt(data)
        iv = base64.b64encode(enc.iv).decode("utf8")
        encrypted_data = base64.b64encode(encrypted_data_bytes).decode('utf-8')

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
