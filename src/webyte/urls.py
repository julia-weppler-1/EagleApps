from django.contrib import admin
from django.urls import include, path
import user.views as views

urlpatterns = [
    path("", views.index, name="index"),
    path("advisor_login/", views.advisor_login, name='advisor_login'),
    path("user/", include("user.urls")),
    path("admin/", admin.site.urls),
    path("landing/", views.landing),
    path("plan/", views.plan, name="plan"),
    path("updateinfo/", views.update_info, name="update_info"),
    path('accounts/', include('allauth.urls')),
    path("plan/", views.plan, name="plan"),
    path('remove_course/', views.remove_course, name='remove_course'),
    path('course_search/', views.course_search, name='course_search'),
    path("view_major_courses/", views.view_major_courses, name="view_major_courses"),

]