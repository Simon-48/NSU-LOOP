from django.db import models

# Create your models here.
class Jackpot(models.Model):
    """
    This class contains the essential fields and behaviors of the data you’re storing. 
	Each model maps to a single database table.
    
    This class is used to create a database table containg those attributes.
   
    """ 
    lucky_id = models.CharField(max_length=3)
    verified = models.BooleanField(default=False)

    def __str__(self):
        """
    	This method return the lucky pick id.

		:param name: self - used to access the attributes and methods of the class in python
		:param type: reference
		:return: str
    
        """
        return f"{self.lucky_id}"