from django.contrib import admin
from .models import Profile, Relationship, Skill
# Register your models here.

admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(Skill)