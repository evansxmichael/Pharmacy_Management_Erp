from django.apps import AppConfig

# ==========================================
# APP CONFIGURATION
# ==========================================
class StoreConfig(AppConfig):
    """
    The central configuration file for the 'store' application.
    Django uses this class to load the app and register it with the main project.
    """
    name = 'store'