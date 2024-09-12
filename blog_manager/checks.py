from django.core.checks import Error, register, Tags, Warning
from .models import BlogPost
from django.conf import settings

@register()
def check_authentication_configuration(app_configs, **kwargs):
    warnings = []

    if not getattr(settings, 'REST_FRAMEWORK', {}).get('DEFAULT_AUTHENTICATION_CLASSES'):
        warnings.append(
            Warning(
                'The REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES setting is not configured.',
                hint='Add appropriate authentication classes to the REST_FRAMEWORK settings.',
                id='blog_manager.W001',
            )
        )

    if not settings.AUTHENTICATION_BACKENDS:
        warnings.append(
            Warning(
                'The AUTHENTICATION_BACKENDS setting is not configured.',
                hint='Add authentication backends to the AUTHENTICATION_BACKENDS setting.',
                id='blog_manager.W002',
            )
        )

    return warnings


@register()
def check_blogpost_fields(app_configs, **kwargs):
    errors = []
    
    missing_title_posts = BlogPost.objects.filter(title__isnull=True) | BlogPost.objects.filter(title='')
    for blog_post in missing_title_posts:
        errors.append(
            Error(
                f"BlogPost with ID {blog_post.id} is missing a title.",
                obj=blog_post,
                id='blog_manager.E001',
            )
        )
    
    missing_author_posts = BlogPost.objects.filter(author__isnull=True)
    for blog_post in missing_author_posts:
        errors.append(
            Error(
                f"BlogPost with ID {blog_post.id} is missing an author.",
                obj=blog_post,
                id='blog_manager.E002',
            )
        )
    
    return errors

#@register(Tags.database)  
@register(Tags.security, deploy=True)
def check_settings_configuration(app_configs, **kwargs):
    errors = []
    from django.conf import settings
    if not settings.SECRET_KEY:
        errors.append(
            Error(
                "SECRET_KEY is not set in settings.",
                id='blog_manager.E003',
            )
        )
    return errors
