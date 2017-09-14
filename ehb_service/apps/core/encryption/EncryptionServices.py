import struct
import zlib
import logging

from Crypto.Cipher import AES

from core.encryption.EncryptionServiceBase import EncryptionService
from core.encryption.Exceptions import CheckSumFailure

log = logging.getLogger(__name__)


class AESEncryption(EncryptionService):

    def configure(self, **kwargs):
        log.debug('AESEncryption.configure - input kwargs: {0}'.format(kwargs))
        self.mode = kwargs.get('mode', AES.MODE_CFB)
        log.debug('AESEncryption.configure - self.mode: {0}'.format(self.mode))
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
        log.debug('in encrypt - **kwargs passed in: {0}'.format(kwargs))
        log.debug('in encrypt - data that is passed in:{0}'.format(data))
        log.debug('in encrypt - here is auto_correct_key_length: '.format(self.auto_correct_key_length))
        if self.auto_correct_key_length:
            key = self._correct_key_length(key)

        enc = AES.new(key, self.mode)

        log.debug('in encrypt - here is use_checksum: {0}'.format(self.use_checksum))
        if self.use_checksum:
            log.debug('in encrypt - data before encryption: {0} '.format(data))
            data += struct.pack("i", zlib.crc32(data))
            log.debug('in encrypt - data after encyption: {0}'.format(data))

        return enc.encrypt(data)

    def decrypt(self, edata, key, **kwargs):
        log.debug('in decrypt - all **kwargs: {0}'.format(kwargs))
        log.debug('in decrypt - data that is passed: {0}'.format(edata))
        log.debug('in decrypt - auto_correct_key_length: {0}'.format(self.auto_correct_key_length))
        if self.auto_correct_key_length:
            key = self._correct_key_length(key)

        enc = AES.new(key, self.mode)
        data = enc.decrypt(edata)
        log.debug('in decrypt - decrypted data: {0}'.format(data))
        log.debug('in decrypt - use_checksum: {0}'.format(self.use_checksum))
        if self.use_checksum:
            cs, data = (data[-4:], data[:-4])
            log.debug('in decrypt - cs: {0}'.format(cs))
            log.debug('in decrypt - data[:-4] : {0}'.format(data))
            if not cs == struct.pack("i", zlib.crc32(data)):
                raise CheckSumFailure('Checksum failed in decrypt')
                log.debug('in decrypt - checksum failed in decrypt - error raised')
        return data

    def is_encrypted(self, edata, key, **kwargs):
        # if checksum is not used, there is in general no way to know if edata is encrypted

        log.debug('in is_encrypted - all **kwargs: {0}'.format(kwargs))
        log.debug('in is_encrypted - data that is passed: {0}'.format(edata))
        log.debug('in is_encrypted - auto_correct_key_length: {0}'.format(self.auto_correct_key_length))
        log.debug('in is_encrypted - use_checksum: {0}'.format(self.use_checksum))
        if self.use_checksum:
            try:
                self.decrypt(edata, key)
                log.debug('in is_encrypted - decrypted data: {0}'.format(self.decrypt(edata, key)))
                log.debug("in is_encrypted - decryption sucessful")
                return True
            except CheckSumFailure:
                log.error("Checksum failure. Unable to decrypt")
                log.debug("Checksum failure. Unable to decrypt")
                return False

    def check_sum_length(self, **kwargs):
        if self.use_checksum:
            return 4
        else:
            return 0
