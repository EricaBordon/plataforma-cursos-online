from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Course(models.Model):
    instructor  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price       = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    thumbnail   = models.ImageField(upload_to='courses/', null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title  = models.CharField(max_length=200)
    order  = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    module   = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title    = models.CharField(max_length=200)
    content  = models.TextField(blank=True)
    order    = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title