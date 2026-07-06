from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    path(
        "courses/<int:pk>/",
        views.course_detail,
        name="course-detail-web"
    ),

    path(
        "courses/<int:pk>/enroll/",
        views.enroll_course,
        name="course-enroll-web"
    ),

    path(
        "instructor/",
        views.instructor_dashboard,
        name="instructor-dashboard"
    ),

    path(
        "instructor/create/",
        views.course_create,
        name="course-create"
    ),

    path(
        "instructor/<int:pk>/edit/",
        views.course_update,
        name="course-update"
    ),

    path(
        "instructor/<int:pk>/delete/",
        views.course_delete,
        name="course-delete"
    ),

    path(
        "instructor/<int:course_id>/module/create/",
        views.module_create,
        name="module-create"
    ),

    path(
        "instructor/module/<int:module_id>/lesson/create/",
        views.lesson_create,
        name="lesson-create"
    ),
    path(
    "instructor/module/<int:pk>/edit/",
    views.module_update,
    name="module-update"
    ),

    path(
    "instructor/module/<int:pk>/delete/",
    views.module_delete,
    name="module-delete"
    ),

    path(
    "instructor/lesson/<int:pk>/edit/",
    views.lesson_update,
    name="lesson-update"
    ),

    path(
    "instructor/lesson/<int:pk>/delete/",
    views.lesson_delete,
    name="lesson-delete"
    ),

        path(
        "instructor/course/<int:course_id>/quiz/create/",
        views.quiz_create,
        name="quiz-create"
    ),

    path(
        "instructor/quiz/<int:pk>/edit/",
        views.quiz_update,
        name="quiz-update"
    ),

    path(
        "instructor/quiz/<int:pk>/delete/",
        views.quiz_delete,
        name="quiz-delete"
    ),

    path(
        "instructor/quiz/<int:quiz_id>/question/create/",
        views.question_create,
        name="question-create"
    ),

    path(
        "instructor/question/<int:pk>/edit/",
        views.question_update,
        name="question-update"
    ),

    path(
        "instructor/question/<int:pk>/delete/",
        views.question_delete,
        name="question-delete"
    ),

    path(
        "instructor/question/<int:question_id>/answer/create/",
        views.answer_create,
        name="answer-create"
    ),

    path(
        "instructor/answer/<int:pk>/edit/",
        views.answer_update,
        name="answer-update"
    ),

    path(
        "instructor/answer/<int:pk>/delete/",
        views.answer_delete,
        name="answer-delete"
    ),
    path(
    "courses/<int:course_id>/quiz/",
    views.take_quiz,
    name="take-quiz",
    ),
    path(
    "courses/<int:course_id>/review/",
    views.add_review,
    name="add-review",
    ),
]