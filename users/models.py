from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class Role(models.TextChoices):
    ADMIN      = 'admin',      'Admin'
    INSTRUCTOR = 'instructor', 'Instructor'
    STUDENT    = 'student',    'Student'


class User(AbstractUser):
    email = models.EmailField(unique=True)
    role  = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return f'{self.email} ({self.role})'


class Profile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar     = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio        = models.TextField(blank=True)
    birthdate  = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f'Perfil de {self.user.email}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)