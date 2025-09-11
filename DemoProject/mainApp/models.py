from django.db import models

# Create your models here.
class Train(models.Model):
    train_number = models.CharField(max_length=10, unique=True)
    