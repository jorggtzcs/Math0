from django.contrib import admin
from .models import Subject,Lesson,Exercise,Option,StudentProgress

#lnline for options in questions
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4   #extra options

class ExerciseAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('question_text', 'lesson')

# Register your models here.
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Option)
admin.site.register(StudentProgress)