from django.contrib import admin
from .models import register, login

# Register your models here.
@admin.register(register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'id')
    search_fields = ('name', 'email')
    list_filter = ('name',)

@admin.register(login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('username', 'id')
    search_fields = ('username',)

