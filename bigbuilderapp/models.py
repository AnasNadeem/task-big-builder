from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    asked_amount = models.DecimalField(max_digits=10, decimal_places=2)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class TaskPic(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='task_pics')
    
    def __str__(self):
        return self.task.name + " - " + self.pic.name


class TaskPayment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task.name + " - " + str(self.payment)
