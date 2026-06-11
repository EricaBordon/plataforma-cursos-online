from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("courses/<int:pk>/", views.course_detail, name="course-detail-web"),
    path("courses/<int:pk>/enroll/", views.enroll_course, name="course-enroll-web"),
]