from django.apps import AppConfig


class BlogManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_manager'

    def ready(self):
        import blog_manager.signals 
        import blog_manager.checks 

