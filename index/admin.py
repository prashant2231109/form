from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Choices)
admin.site.register(Questions)
admin.site.register(Form)
admin.site.register(Answers)
admin.site.register(Responses)
