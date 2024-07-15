from django.contrib import admin

from .models import Advisor, Student, Administrator, Plan, Course, Econ_major, CS_Major_BA,CS_Major_BS,CS_Major_Core, ScienceComponent

admin.site.register(Advisor)
admin.site.register(Student)
admin.site.register(Administrator)
admin.site.register(Plan)
admin.site.register(Course)
admin.site.register(Econ_major)
admin.site.register(CS_Major_Core)
admin.site.register(CS_Major_BS)
admin.site.register(CS_Major_BA)
admin.site.register(ScienceComponent)

