from django.contrib import admin
from .models import User,Task,Remark,Reminder

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Remark)
admin.site.register(Reminder)