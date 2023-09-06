from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

# User database
class User(AbstractUser):
    pass


# Customer database
class Customer(models.Model):
    customer_id = models.IntegerField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.CharField(max_length=50)
    info_box = models.CharField(max_length=1000)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user")


# Task database
class Task(models.Model):
    task_id = models.IntegerField()
    task_customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="task_customer_id")
    task_name = models.CharField(max_length=50)
    task_date = models.DateField(null=True, blank=True)
    task_done_date = models.DateField(null=True, blank=True)
    task_price = models.CharField(max_length=15)
    task_done = models.BooleanField(default=False)
    task_to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_to_user")