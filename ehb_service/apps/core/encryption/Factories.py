import logging

from django.conf import settings

log = logging.getLogger(__name__)

class FactoryEncryptionServices(object):

    @staticmethod
    def use_encryption():
        return getattr(settings, 'EHB_USE_ENCRYPTION', False)

    @staticmethod
    def _load_class(module_name, class_name):
        module = __import__(module_name, globals(), locals(), [class_name], -1)
        return getattr(module, class_name)

    @staticmethod
    def _active_service_loader(service_dict):
        log.debug('FactoryEncryptionServices._active_service_loader - input service_dict: {0}'.format(service_dict))
        if service_dict:
            mn = service_dict.get('module', None)
            cn = service_dict.get('class', None)
            if mn and cn:
                _class = FactoryEncryptionServices._load_class(mn, cn)
                kwargs = service_dict.get('kwargs', None)
                service = _class()
                log.debug('FactoryEncryptionServices._active_service_loader - kwargs: {0}'.format(kwargs))
                if kwargs:
                    service.configure(**kwargs)
                return service

    @staticmethod
    def active_encryption_service():
        return FactoryEncryptionServices._active_service_loader(getattr(settings, 'EHB_ENCRYPTION_SERVICE', None))

    @staticmethod
    def active_key_management_service():
        return FactoryEncryptionServices._active_service_loader(getattr(settings, 'EHB_KEY_MANAGEMENT_SERVICE', None))
