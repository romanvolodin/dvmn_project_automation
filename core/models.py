from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(max_length=50, default="")
    telegram_id = models.CharField(max_length=20, default="")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joinned = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.name}, {self.email}"


class Project(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Week(models.Model):
    project = models.ForeignKey(
        "Project", related_name="weeks", on_delete=models.CASCADE
    )
    start_date = models.DateField()
    product_managers = models.ManyToManyField("ProductManager", related_name="weeks")

    def __str__(self):
        return f"{self.project.title} {self.start_date}"


class Team(models.Model):
    week = models.ForeignKey(Week, related_name="teams", on_delete=models.CASCADE)
    start_call_at = models.TimeField()
    product_manager = models.ForeignKey(
        "ProductManager", related_name="teams", on_delete=models.CASCADE
    )
    members = models.ManyToManyField("Student")

    def __str__(self):
        return f"{self.week}, call at {self.start_call_at}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_far_east = models.BooleanField(default=False)
    call_range_start = models.TimeField(blank=True, null=True)
    call_range_end = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.user.name


class ProductManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    call_range_start = models.TimeField(blank=True, null=True)
    call_range_end = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.user.name
