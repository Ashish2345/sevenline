import os
import uuid
from cryptography.fernet import Fernet
from django.conf import settings
# from .models import EncryptedStringAccess


class FernetEncryptionV1:
    def __init__(self):
        self.key = settings.ENCRYPTION_KEY
        print(self.key)
        self.fernet = Fernet(self.key)

    def _encryptStringV1(self, data):
        return self.fernet.encrypt(bytes(data, 'utf-8')).decode("utf-8")

    def _decryptStringV1(self, data):
        return self.fernet.decrypt(data.encode("utf-8")).decode("utf-8")


def _encrypt(data):
    fernet_object = FernetEncryptionV1()
    encryption_check = _decrypt(data)
    if _isEncrypted(data) is False:
        try:
            processed_data = fernet_object._encryptStringV1(data)
        except Exception as e:
            processed_data = data
            print(e, 'encryption exception')
    else:
        processed_data = data
    return processed_data


def _decrypt(data):
    fernet_object = FernetEncryptionV1()
    if _isEncrypted(data) is True:
        try:
            processed_data = fernet_object._decryptStringV1(data)
        except Exception as e:
            print(e, 'decryption exception')
            processed_data = data
    else:
        processed_data = data
    return processed_data


def _isEncrypted(data):
    fernet_object = FernetEncryptionV1()
    try:
        processed_data = fernet_object._decryptStringV1(data)
        return True
    except Exception as e:
        return False
