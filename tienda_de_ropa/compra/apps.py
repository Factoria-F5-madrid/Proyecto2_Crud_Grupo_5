from django.apps import AppConfig

class CompraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'compra'
    verbose_name = 'Módulo de Compras' # Puedes mantener este o el que ya tengas

    def ready(self):
        # Importa las señales aquí para que Django las descubra y conecte
        # Si las funciones @receiver están en models.py, importa models.
        # Si las movieras a un archivo signals.py, importarías signals.
        import compra.models 
        