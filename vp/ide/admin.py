from django.contrib import admin

# Register your models here.
from .models import Side_Menu_Node, User_Menu_Access

admin.site.register(Side_Menu_Node)
admin.site.register(User_Menu_Access)