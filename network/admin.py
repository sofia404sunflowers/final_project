from django.contrib import admin
from .models import Post, User, Recording
admin.site.register(User)
admin.site.register(Recording)
admin.site.register(Post)
# Register your models here.
