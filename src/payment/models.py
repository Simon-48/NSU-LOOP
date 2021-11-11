from django.db import models

# Create your models here.
class Payment(models.Model):
    mobile_number = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.transaction_id}"