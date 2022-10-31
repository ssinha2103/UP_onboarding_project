from .models import Items, Orders, Profile, Stores
from django.contrib import admin

admin.site.register([Profile, Stores, Items, Orders])
