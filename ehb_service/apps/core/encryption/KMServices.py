from core.encryption.EncryptionServiceBase import KeyManagementService

class LocalKMS(KeyManagementService):

    def configure(self, **kwargs):
        self.local_key = kwargs.get('key', None)

    def get_key(self, **kwargs):
        return self.local_key
