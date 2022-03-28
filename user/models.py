from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('A', 'Admin'),
        ('E', 'Employee')
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=1, choices=ROLES)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        username = getattr(self, 'email')
        setattr(self, 'username', username)
        super(User, self).save()


class Leaves(models.Model):
    STATUS = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected')
    )
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='leaves')
    start = models.DateField()
    end = models.DateField()
    day_count = models.IntegerField()
    status = models.CharField(max_length=1, choices=STATUS, default='P')
    attachment = models.FileField(upload_to='images/leave_attachments', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        start = getattr(self, 'start')
        end = getattr(self, 'end')
        day_count = (end - start).days + 1
        setattr(self, 'day_count', day_count)
        super(Leaves, self).save()
