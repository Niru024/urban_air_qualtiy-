from django.db import models

# Create your models here.
class register(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name = "User Registration"
        verbose_name_plural = "User Registrations"
    
    def __str__(self):
        return f"{self.name} ({self.email})"
        
class login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "User Login"
        verbose_name_plural = "User Logins"
    
    def __str__(self):
        return self.username

  