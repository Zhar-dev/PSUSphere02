from django.contrib import admin
from .models import College, Program, Organization, Student, OrgMember

# Register your models here.

admin.site.register(College)
admin.site.register(Program)
admin.site.register(Organization)
admin.site.register(Student)
admin.site.register(OrgMember)