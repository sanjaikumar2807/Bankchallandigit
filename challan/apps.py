"""
Django app configuration for challan application.
"""

from django.apps import AppConfig


class ChallanConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'challan'
    verbose_name = 'Bank Challan Machine'
    
    def ready(self):
        """
        App initialization code.
        """
        import logging
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        logger = logging.getLogger(__name__)
        logger.info('Bank Challan Machine app is ready')
        
        # Python 3.14 compatibility patch for Django BaseContext copy
        try:
            from django.template import context as django_context
            def _fixed_base_context_copy(ctx_self):
                duplicate = object.__new__(ctx_self.__class__)
                duplicate.__dict__.update(ctx_self.__dict__)
                duplicate.dicts = ctx_self.dicts[:]
                return duplicate
            django_context.BaseContext.__copy__ = _fixed_base_context_copy
        except Exception as e:
            logger.warning(f"Could not apply BaseContext patch: {e}")
