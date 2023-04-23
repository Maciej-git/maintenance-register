from django.contrib import admin
from .models import User, Location, Group, Machine, Area, Request, Note

# Register your models here.
admin.site.register(User)
admin.site.register(Location)
admin.site.register(Area)
admin.site.register(Group)
admin.site.register(Machine)
admin.site.register(Request)
admin.site.register(Note)