# from typing import Self
# from django.db.models.signals import (
#     pre_init, post_init, pre_save, pre_delete,
#     post_save, post_delete, pre_migrate, post_migrate
# )
# from django.contrib.auth.signals import (
#     user_logged_in, user_logged_out, user_login_failed
# )
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import BlogPost, UserProfile
# from django.core.signals import (
#     request_started, request_finished, got_request_exception
# )
# from django.db.backends.signals import connection_created
# from django.dispatch import Signal, receiver 


# # Authentication(login/logout) Signals
# @receiver(user_logged_in, sender=User)
# def handle_user_login(sender, request, user, **kwargs):
#     """Triggered when a user successfully logs in."""
#     print("---------------------")
#     print("User Login Successful")
#     print(f"User: {user.username} logged in.")
#     print(f"Request Path: {request.path}")
#     print(f"Additional Info: {kwargs}")


# @receiver(user_logged_out, sender=User)
# def handle_user_logout(sender, request, user, **kwargs):
#     """Triggered when a user logs out."""
#     print("---------------------")
#     print("User Logout")
#     print(f"User: {user.username} logged out.")
#     print(f"Request Path: {request.path}")
#     print(f"Additional Info: {kwargs}")


# @receiver(user_login_failed)
# def handle_login_failure(sender, credentials, request, **kwargs):
#     """Triggered when a login attempt fails."""
#     print("---------------------")
#     print("User Login Failed")
#     print(f"Attempted Credentials: {credentials.get('username')}")
#     print(f"Request Path: {request.path}")
#     print(f"Additional Info: {kwargs}")


# # Model class Signals
# @receiver(pre_save, sender=BlogPost)
# def before_blog_post_save(sender, instance, **kwargs):
#     """Triggered before saving a BlogPost instance."""
#     print("---------------------")
#     print("About to Save BlogPost")
#     print(f"BlogPost Title: {instance.title}")
#     print(f"Additional Info: {kwargs}")


# @receiver(post_save, sender=BlogPost)
# def after_blog_post_save(sender, instance, created, **kwargs):
#     """Triggered after saving a BlogPost instance."""
#     action = "Created" if created else "Updated"
#     print("---------------------")
#     print(f"BlogPost {action}: {instance.title}")
#     print(f"Additional Info: {kwargs}")


# @receiver(pre_delete, sender=BlogPost)
# def before_blog_post_delete(sender, instance, **kwargs):
#     """Triggered before deleting a BlogPost instance."""
#     print("---------------------")
#     print("About to Delete BlogPost")
#     print(f"BlogPost Title: {instance.title}")
#     print(f"Additional Info: {kwargs}")


# @receiver(post_delete, sender=BlogPost)
# def after_blog_post_delete(sender, instance, **kwargs):
#     """Triggered after deleting a BlogPost instance."""
#     print("---------------------")
#     print(f"BlogPost Deleted: {instance.title}")
#     print(f"Additional Info: {kwargs}")


# @receiver(pre_init, sender=User)
# def before_user_init(sender, *args, **kwargs):
#     """Triggered before initializing a User instance."""
#     print("---------------------")
#     print("Initializing User Instance")
#     print(f"Sender: {sender}")
#     print(f"Additional Args: {args}")
#     print(f"Additional Info: {kwargs}")


# @receiver(post_init, sender=User)
# def after_user_init(sender, *args, **kwargs):
#     """Triggered after initializing a User instance."""
#     print("---------------------")
#     print("User Instance Initialized")
#     print(f"Sender: {sender}")
#     print(f"Additional Args: {args}")
#     print(f"Additional Info: {kwargs}")


# # Request/Response Signals
# @receiver(request_started)
# def on_request_started(sender, environ, **kwargs):
#     """Triggered when a request starts."""
#     print("---------------------")
#     print("Request Started")
#     print(f"Environment: {environ}")
#     print(f"Additional Info: {kwargs}")


# @receiver(request_finished)
# def on_request_finished(sender, **kwargs):
#     """Triggered when a request finishes."""
#     print("---------------------")
#     print("Request Finished")
#     print(f"Sender: {sender}")
#     print(f"Additional Info: {kwargs}")


# @receiver(got_request_exception)
# def on_request_exception(sender, request, **kwargs):
#     """Triggered when an exception occurs during request handling."""
#     print("---------------------")
#     print("Request Exception Occurred")
#     print(f"Request Path: {request.path}")
#     print(f"Additional Info: {kwargs}")


# # Management Signals
# @receiver(pre_migrate)
# def before_migrate(sender, app_config, verbosity, interactive, using, plan, apps, **kwargs):
#     """Triggered before migrations are applied."""
#     print("---------------------")
#     print("Before Migrate")
#     print(f"App: {app_config.name}")
#     print(f"Plan: {plan}")
#     print(f"Additional Info: {kwargs}")


# @receiver(post_migrate)
# def after_migrate(sender, app_config, verbosity, interactive, using, plan, apps, **kwargs):
#     """Triggered after migrations are applied."""
#     print("---------------------")
#     print("Migrations Completed")
#     print(f"App: {app_config.name}")
#     print(f"Plan: {plan}")
#     print(f"Additional Info: {kwargs}")


# # Database Connection Signals
# @receiver(connection_created)
# def on_database_connection_created(sender, connection, **kwargs):
#     """Triggered when a database connection is created."""
#     print("---------------------")
#     print("Database Connection Established")
#     print(f"Sender: {sender}")
#     print(f"Connection Details: {connection}")
#     print(f"Additional Info: {kwargs}")
    
# custom_signal = Signal()

# @receiver(post_save, sender=UserProfile)
# def user_profile_post_save(sender, instance, created, **kwargs):
#     first_name = instance.first_name
#     last_name = instance.last_name

#     custom_signal.send(sender=sender, first_name=first_name, last_name=last_name)

# @receiver(custom_signal)
# def custom_signal_receiver(sender, **kwargs):
#     first_name = kwargs.get('first_name')
#     last_name = kwargs.get('last_name')
#     print("custom signals for userprofiles")
#     print(f'Signal received from {sender}: {first_name}, {last_name}')