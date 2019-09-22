from django.contrib import admin

# Register your models here.
from .models import Post, Preference, Comment

admin.site.register(Post)
admin.site.register(Preference)
admin.site.register(Comment)