from django.contrib import admin
from .models import Subject, Lesson, Exercise, Option, StudentProgress, Classroom, ClassroomEnrollment, Profile


# lnline for options in questions
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # extra options


class ExerciseAdmin(admin.ModelAdmin):
    inlines = [OptionInline]
    list_display = ('question_text', 'lesson')


# Register your models here.
admin.site.register(Subject)
admin.site.register(Lesson)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Option)
admin.site.register(StudentProgress)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'code', 'created_at')
    search_fields = ('name', 'teacher__username', 'code')


@admin.register(ClassroomEnrollment)
class ClasroomEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'student', 'joined_at')
    search_fields = ('classroom__name', 'student__username')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_teacher', 'is_paid', 'plan_type')
    search_fields = ('user__username',)
