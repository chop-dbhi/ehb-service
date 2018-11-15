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
            print ("this is key type")
            print (type(key))
            return key + (AES.block_size-l)*self.padding
        else:
            return key

    def encrypt(self, data, key, **kwargs):
        if self.auto_correct_key_length:
            key = self._correct_key_length(key)

        # convert string to bytes. Using latin1 to allow for
        # extended ASCII Types > 127 because the cipher text
        # that is a result of encryption will return ASCII > 127
        key = key.encode("utf8")
        # data = base64.b64encode(data)
        enc = AES.new(key, AES.MODE_CFB)

        # enc = AES.new(key, AES.MODE_CFB, iv=b'0123456789abcdef')

        if self.use_checksum:
            # struct pack returns a byte object within the values of 'i'
            # of zlib, which is a 32 bit representation of data.
            # we add this to data
            # print ("this is zlib data")
            # print (zlib.crc32(data))
            # data_to_add = struct.pack("I", zlib.crc32(data))
            # print ("this is data to add")
            # print (data_to_add)
            data += struct.pack("I", zlib.crc32(data))

        encrypted_data_bytes = enc.encrypt(data)
        print ("this is encrypted data bytes")
        print (encrypted_data_bytes.decode("latin1"))
        print ("this is the length")
        print (len(encrypted_data_bytes))

        # return string of encrypted data bytes
        return encrypted_data_bytes
        # return (base64.b64encode(encrypted_data_bytes)).decode("latin1")


    def decrypt(self, edata, key, **kwargs):
        if self.auto_correct_key_length:
            key = self._correct_key_length(key)

        print ("this is key")
        print (key)
        print ("this is edata")
        print (edata)

        # convert string to bytes
        key = key.encode("latin1")

        enc = AES.new(key, self.mode, iv=b'0123456789abcdef')
        # enc = AES.new(key, self.mode, iv=b'0123456789abcdef')
        # data = enc.decrypt(edata).decode("latin1")
        data = enc.decrypt(edata)
        print ("this is data decrypted")
        print (data)

        if self.use_checksum:
            cs, data = (data[-4:], data[:-4])
            # convert back to bytes
            # cs = cs.encode("latin1")
            # check_data = data.encode("latin1")
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
