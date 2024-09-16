# from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
# from django.dispatch import receiver
# from django.core.cache import cache
# from django.conf import settings
# from .models import BlogPost, Reaction

# @receiver(pre_save, sender=BlogPost)
# def pre_save_blog_post(sender, instance, **kwargs):
#     print(f"Preparing to save BlogPost instance: {instance}")

# @receiver(pre_delete, sender=BlogPost)
# def pre_delete_blog_post(sender, instance, **kwargs):
#     print(f"Preparing to delete BlogPost instance: {instance}")

# @receiver(post_save, sender=BlogPost)
# def update_blog_post_cache(sender, instance, **kwargs):
#     cache_key_list = f"{settings.KEY_PREFIX}_blog_post_list"
#     cache_key_detail = f"{settings.KEY_PREFIX}_blog_post_detail_{instance.pk}"
#     print(f"Invalidating cache for key: {cache_key_list}")
#     cache.delete(cache_key_list)
#     print(f"Invalidating cache for key: {cache_key_detail}")
#     cache.delete(cache_key_detail)

# @receiver(post_delete, sender=BlogPost)
# def delete_blog_post_cache(sender, instance, **kwargs):
#     cache_key_list = f"{settings.KEY_PREFIX}_blog_post_list"
#     cache_key_detail = f"{settings.KEY_PREFIX}_blog_post_detail_{instance.pk}"
#     print(f"Invalidating cache for key: {cache_key_list}")
#     cache.delete(cache_key_list)
#     print(f"Invalidating cache for key: {cache_key_detail}")
#     cache.delete(cache_key_detail)

# @receiver(pre_save, sender=Reaction)
# def pre_save_reaction(sender, instance, **kwargs):
#     print(f"Preparing to save Reaction instance: {instance}")

# @receiver(pre_delete, sender=Reaction)
# def pre_delete_reaction(sender, instance, **kwargs):
#     print(f"Preparing to delete Reaction instance: {instance}")

# @receiver(post_save, sender=Reaction)
# def update_reaction_cache(sender, instance, **kwargs):
#     cache_key = f"{settings.KEY_PREFIX}reaction_list"
#     print(f"Invalidating cache for key: {cache_key}")
#     cache.delete(cache_key)

# @receiver(post_delete, sender=Reaction)
# def delete_reaction_cache(sender, instance, **kwargs):
#     cache_key = f"{settings.KEY_PREFIX}reaction_list"
#     print(f"Invalidating cache for key: {cache_key}")
#     cache.delete(cache_key)
