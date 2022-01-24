"""
For administration pannel (http://localhost:8000/admin/)
"""

from django.contrib import admin
from .models import User, Post

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
