from django.contrib import admin
from faskApp.models import User,Empresa,Notificacion,Tarea
# Register your models here.

admin.site.register(User)
admin.site.register(Notificacion)
admin.site.register(Empresa)
admin.site.register(Tarea)