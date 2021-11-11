from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    """
    This class contains the essential fields and behaviors of the data for Chats
    Each model maps to a single database table.

    This class is used to create a database table contain those attributes.
    """
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="%(class)s_created_at"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="%(class)s_updated_at"
    )

    from_user = models.ForeignKey(User, related_name='from_chats', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_chats', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        """
        This method return each object's (chat's) sender, receiver and message

        :param name: self - used to access the attributes and methods of the class in python
        :return: str
        """
        return f"{self.from_user}, {self.to_user} --> {self.message}"

    class Meta:
        """
        This class will have the additional behaviours of each chat object specified

        for example the list will be ordered in ascending order for chat model
        """
        ordering = ["id"]


"""
urls
settings -> installed apps

"""