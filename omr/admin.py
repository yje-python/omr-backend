from django.contrib import admin

# Register your models here.
from .models import Exam, Subject, Answer, WrongNote

admin.site.register(Exam)
admin.site.register(Subject)
admin.site.register(Answer)
admin.site.register(WrongNote)