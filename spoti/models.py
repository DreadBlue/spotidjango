from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    correo = models.TextField(blank=True)
    constrasena = models.CharField(max_length=255)
    canciones = models.JSONField(default=list)

    def __str__(self):
        return self.name
