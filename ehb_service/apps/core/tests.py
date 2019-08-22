#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.test import TestCase
from Crypto.Cipher import AES

from core.encryption.EncryptionServices import AESEncryption
from core.encryption.KMServices import LocalKMS


class TestAESEncryption(TestCase):
    def setUp(self):
        pass

    def test_correct_key_length(self):
        service = AESEncryption()
        service.configure()
        key = service._correct_key_length('*' * 10)
        self.assertEqual(len(key), AES.block_size)
        key = service._correct_key_length('*' * 20)
        self.assertEqual(len(key), AES.block_size)
        key = service._correct_key_length('*'*16)
        self.assertEqual(len(key), AES.block_size)

    def test_encrypt(self):
        service = AESEncryption()
        service.configure()
        self.assertEqual(b'KN+p\x80\xac\xe23IX', service.encrypt(b'secret', '123456',b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

    def test_decrypt(self):
        service = AESEncryption()
        service.configure()
        self.assertEqual(b'secret', service.decrypt(b'KN+p\x80\xac\xe23IX', '123456',b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

    def test_is_encrypted(self):
        service = AESEncryption()
        service.configure()
        self.assertTrue(service.is_encrypted(b'KN+p\x80\xac\xe23IX', '123456', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

    def test_check_sum_length(self):
        service = AESEncryption()
        service.configure()
        self.assertEqual(service.check_sum_length(), 4)
        service.configure(use_checksum=False)
        self.assertEqual(service.check_sum_length(), 0)
    
    def return_correct_iv(self):
        kms = LocalKMS()
        kms.configure(iv = '1234567891234567')
        self.assertEqual(kms.iv,b'1234567891234567')

    def test_return_default_iv_none(self):
        kms = LocalKMS()
        kms.configure()
        self.assertEqual(kms.iv,b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def test_return_default_iv_bad(self):
        kms = LocalKMS()
        kms.configure(iv= "1820982")
        self.assertEqual(kms.iv,b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

