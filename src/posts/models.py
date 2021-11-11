from django.db import models
from django.core.validators import FileExtensionValidator
from profiles.models import Profile
# Create your models here.

class Post(models.Model):
    """
    This class contains the essential fields and behaviors of the data you’re storing. 
	Each model maps to a single database table.
    
    This class is used to create a database table containg those attributes.
    """
    content = models.TextField()
    image = models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank=True)
    liked = models.ManyToManyField(Profile, blank=True, related_name='likes')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        """
		This method return the post content size as 20.

		:param name: self - used to access the attributes and methods of the class in python
		:param type: reference
		:return: str
		"""
        return str(self.content[:20])

    def num_likes(self):
        """
		This method will return the number of likes received in a post.

		:param name: self - used to access the attributes and methods of the class in python
		:param type: reference
		:return: str
		"""
        return self.liked.all().count()

    def num_comments(self):
        """
		This method will return the number of comments received in a post.

		:param name: self - used to access the attributes and methods of the class in python
		:param type: reference
		:return: str
		"""
        return self.comment_set.all().count()

    class Meta:
        ordering = ('-created',)

class Comment(models.Model):
    """
    This class contains the essential fields and behaviors of the data you’re storing. 
	Each model maps to a single database table.
    
    This class is used to create a database table containg those attributes.
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
		This method will return the comment primary key to make a relation with post object.

		:param name: self - used to access the attributes and methods of the class in python
		:param type: reference
		:return: str
		"""
        return str(self.pk)

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model): 
    """
    This class contains the essential fields and behaviors of the data you’re storing. 
    Each model maps to a single database table.
    
    This class is used to create a database table containg those attributes.
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """
		This method will return user, post and like choices.

		:param name: self - used to access the attributes and methods of the class in python
		:param type: reference
		:return: str
		"""
        return f"{self.user}-{self.post}-{self.value}"