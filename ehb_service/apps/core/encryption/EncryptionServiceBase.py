from abc import ABCMeta, abstractmethod

class EncryptionService(object, metaclass=ABCMeta):
    @abstractmethod
    def configure(self, **kwargs):
        pass

    @abstractmethod
    def encrypt(self, data, key, **kwargs):
        pass

    @abstractmethod
    def decrypt(self, edata, key, **kwargs):
        pass

    @abstractmethod
    def is_encrypted(self, edata, key, **kwargs):
        pass

    @abstractmethod
    def block_size(self, **kwargs):
        pass

    @abstractmethod
    def check_sum_length(self, **kwargs):
        pass

class KeyManagementService(object):
    __metaclass = ABCMeta

    # Abstract methods
    @abstractmethod
    def configure(self, **kwargs):
        pass

    @abstractmethod
    def get_key(self, **kwargs):
        pass

    @abstractmethod
    def get_iv(seif, **kwargs):
        pass
