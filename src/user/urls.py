from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

app_name = 'user'

urlpatterns = [
    path("/", views.landing, name="landing"),
    path("updateinfo/", views.update_info, name="update_info"),
    path("plan/", views.plan, name="plan"),
    path("department_view/", views.department_view, name="department_view"),
    path("course_search/", views.course_search, name="course_search"),
    re_path(r'^accounts/profile/$', RedirectView.as_view(url='/landing', permanent=True), name='profile_redirect'),
    path("view_major_courses/", views.view_major_courses, name="view_major_courses"),
]