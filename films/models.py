from django.db import models

# Create your models here.


class Film(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    rating_kp = models.FloatField()
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
