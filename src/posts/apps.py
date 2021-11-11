from django.apps import AppConfig


class PostsConfig(AppConfig):
    """
    This class contains the app posts and set the verbose to 'Posts, Comments, Likes'.
    The verbose will be shown in django admin.
    
    """
    name = 'posts'
    verbose_name = 'Posts, Comments, Likes'