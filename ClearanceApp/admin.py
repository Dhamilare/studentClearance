from django.contrib import admin
from .models import *

# Register your models here.

admin.site.site_header = 'Clearance System'
admin.site.site_title = 'Clearance System'
admin.site.index_title = 'Welcome to Clearance Management System'

class StudentAdmin(admin.ModelAdmin):
    list_display = ('matric_no', 'surname', 'other_names')
    ordering = ['-id']

class StaffAdmin(admin.ModelAdmin):
    list_display = ('title', 'first_name', 'last_name', 'office')
    ordering = ['-id']

class ClearanceAdmin(admin.ModelAdmin):
    list_display = ('matric_no', 'surname', 'other_names')
    ordering = ['-id']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('matric_no', 'department', 'student')
    ordering = ['-id']

class HODAdmin(admin.ModelAdmin):
    list_display = ('student', 'matric_no', 'level', 'department')
    ordering = ['-id']

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('surname', 'matric_no', 'level', 'department')
    ordering = ['-id']

class BusaryAdmin(admin.ModelAdmin):
    list_display = ('surname', 'matric_no', 'level', 'department')
    ordering = ['-id']

class LibraryAdmin(admin.ModelAdmin):
    list_display = ('surname', 'matric_no', 'level', 'department')
    ordering = ['-id']

admin.site.register(Clearance, ClearanceAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(HOD, HODAdmin)
admin.site.register(Busary, BusaryAdmin)
admin.site.register(Library, LibraryAdmin)
