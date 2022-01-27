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
    """
    Студент (учащийся курсов ДВМН).
    """
    name = models.CharField(
        max_length=50,
        default='',
        verbose_name='имя/ник',
        )
    tg_username = models.CharField(
        max_length=32,
        default='',
        verbose_name='пользовательское имя в Telegram',
        )
    discord_username = models.CharField(
        max_length=32,
        default='',
        verbose_name='пользовательское имя в Discord',
        )        
    joined_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        verbose_name='дата создания записи',
        )
    is_far_east = models.BooleanField(
        default=False,
        verbose_name='с Дальнего Востока?',
        )

    def __str__(self):
        return self.name


class ProductManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    call_range_start = models.TimeField(blank=True, null=True)
    call_range_end = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.user.email


class TimeSlot(models.Model):
    """
    Временные интервалы.
    """
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Временной интервал'
        verbose_name_plural = 'Временные интервалы'
        unique_together = ('start', 'end')

    def __str__(self):
        return f'{self.start} - {self.end}'


class StudentProjectPreferences(models.Model):
    """
    Предпочтения студента в проекте.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        verbose_name='студент',
        related_name='projects_preferences',
        )    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name='проект',
        related_name='preferences',
        )
    is_any_week = models.BooleanField(
        verbose_name='на любой неделе?',
        help_text='отметить, если устраивает любая неделя',
        default=False,
        )        
    week = models.ForeignKey(
        Week,
        on_delete=models.CASCADE,
        verbose_name='неделя',
        related_name='project_weeks',
        null=True,
        blank=True,
        )
    is_any_time = models.BooleanField(
        verbose_name='в любое время?',
        help_text='отметить, если устраивает любой из интервалов',
        default=False,
        )
    time_slots = models.ManyToManyField(
        TimeSlot,
        verbose_name='временные интервалы',
        blank=True,
        related_name='time_slots',
        )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='дата/время создания',
        editable=False,
        )

    class Meta:
        verbose_name = 'Предпочтения'
        verbose_name_plural = 'Предпочтения'
        unique_together = ('student', 'project')

    def __str__(self):
        return f'{self.student}/{self.project}'
    
    def clean(self):
        """Проверить значения полей модели."""
        # TODO 
        # 1. Проверить, что week принадлежит тому же project
        # 2. Если is_any_week не отмечено и не выбран ни одна week,
        # то установить is_any_week = True 
        # 3. Если is_any_time не отмечено и не выбран ни один time_slots,
        # то установить is_any_time = True 
        pass