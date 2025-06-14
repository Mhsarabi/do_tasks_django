from django.db import models
from account.models import User

# Create your models here.
class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='task')
    task=models.CharField(max_length=300)
    done=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user}-{self.task[:10]}"