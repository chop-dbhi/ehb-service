from core.encryption.EncryptionServiceBase import KeyManagementService

class LocalKMS(KeyManagementService):

    def configure(self, **kwargs):
        self.local_key = kwargs.get('key', None)
        self.iv = self.verify_iv(kwargs.get('iv',None)) 

    def get_key(self, **kwargs):
        """Returns Encryption Key"""

        return self.local_key

    def get_iv(self, **kwargs):
        """Returns initialization vector"""
        return self.iv

    def verify_iv(self, iv):
        """IV must be 16 bits long. If no IV is supplied, default IV is returned below."""
        if (iv is None or len(iv.encode('utf-8')) != 16):
            return b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        else:
            return iv.encode('utf8')
