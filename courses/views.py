from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Sum, Q, DecimalField, Value
from django.db.models.functions import Coalesce
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from certificates.models import Certificate
from enrollments.models import Enrollment, LessonProgress

from .forms import (
    CourseForm,
    ModuleForm,
    LessonForm,
    QuizForm,
    QuestionForm,
    AnswerOptionForm,
    ReviewForm,
)

from .models import (
    Course,
    Module,
    Lesson,
    Quiz,
    Question,
    AnswerOption,
    QuizAttempt,
    Review,
)


def instructor_required(view_func):
    """
    Permite el acceso solo a usuarios con rol de instructor.
    """

    def wrapper(request, *args, **kwargs):
        if request.user.role != "instructor":
            return HttpResponseForbidden(
                "Acceso solo para instructores."
            )

        return view_func(request, *args, **kwargs)

    return wrapper


def home(request):
    """
    Muestra la página principal con los cursos publicados.
    """
    courses = Course.objects.filter(is_published=True)

    return render(
        request,
        "courses/public/home.html",
        {"courses": courses}
    )


def course_detail(request, pk):
    """
    Muestra el detalle de un curso publicado.
    El contenido completo solo se muestra si el estudiante pagó,
    o si el usuario es instructor/admin.
    También muestra y habilita reseñas para estudiantes que pagaron el curso.
    """

    course = get_object_or_404(
        Course,
        pk=pk,
        is_published=True
    )

    course.price_display = f"{int(course.price):,}".replace(",", ".")

    can_access_content = False
    completed_lesson_ids = []
    enrollment = None
    progress_percentage = 0

    reviews = Review.objects.select_related("student").filter(
        course=course
    )

    user_review = None
    can_review = False
    review_form = ReviewForm()

    if request.user.is_authenticated:

        enrollment = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).first()

        if request.user.is_staff or request.user.role == "admin":
            can_access_content = True

        elif request.user.role == "instructor" and course.instructor == request.user:
            can_access_content = True

        elif request.user.role == "student" and enrollment:

            if enrollment.status == "paid":
                can_access_content = True
                progress_percentage = enrollment.progress_percentage

                completed_lesson_ids = list(
                    LessonProgress.objects.filter(
                        enrollment=enrollment,
                        is_completed=True
                    ).values_list("lesson_id", flat=True)
                )

                user_review = Review.objects.filter(
                    student=request.user,
                    course=course
                ).first()

                if not user_review:
                    can_review = True

    return render(
        request,
        "courses/public/course_detail.html",
        {
            "course": course,
            "can_access_content": can_access_content,
            "completed_lesson_ids": completed_lesson_ids,
            "enrollment": enrollment,
            "progress_percentage": progress_percentage,
            "reviews": reviews,
            "review_form": review_form,
            "can_review": can_review,
            "user_review": user_review,
        }
    )


@login_required
def enroll_course(request, pk):
    """
    Permite que un usuario autenticado se inscriba a un curso.
    """
    course = get_object_or_404(
        Course,
        pk=pk,
        is_published=True
    )

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
    )

    if created:
        messages.success(
            request,
            "Te inscribiste correctamente al curso."
        )
    else:
        messages.info(
            request,
            "Ya estás inscrito en este curso."
        )

    return redirect("course-detail-web", pk=course.pk)


@login_required
@instructor_required
def instructor_dashboard(request):
    """
    Dashboard del instructor con estadísticas usando agregaciones de Django.
    Usa annotate(), aggregate(), Count(), Avg() y Sum().
    """

    money_field = DecimalField(max_digits=12, decimal_places=2)

    courses = Course.objects.filter(
        instructor=request.user
    ).annotate(
        total_students=Count(
            "enrollments",
            distinct=True
        ),
        total_reviews=Count(
            "reviews",
            distinct=True
        ),
        average_rating=Avg(
            "reviews__rating"
        ),
        total_income=Coalesce(
            Sum(
                "enrollments__payments__amount",
                filter=Q(enrollments__payments__status="approved"),
                distinct=True
            ),
            Value(0, output_field=money_field),
            output_field=money_field
        ),
    )

    stats = courses.aggregate(
        total_courses=Count(
            "id",
            distinct=True
        ),
        total_students=Count(
            "enrollments",
            distinct=True
        ),
        total_reviews=Count(
            "reviews",
            distinct=True
        ),
        average_rating=Avg(
            "reviews__rating"
        ),
        total_income=Coalesce(
            Sum(
                "enrollments__payments__amount",
                filter=Q(enrollments__payments__status="approved"),
                distinct=True
            ),
            Value(0, output_field=money_field),
            output_field=money_field
        ),
    )

    return render(
        request,
        "courses/instructor/instructor_dashboard.html",
        {
            "courses": courses,
            "stats": stats,
        }
    )


@login_required
@instructor_required
def course_create(request):
    """
    Permite al instructor crear un nuevo curso.
    """
    if request.method == "POST":
        form = CourseForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()

            messages.success(
                request,
                "Curso creado correctamente."
            )

            return redirect("instructor-dashboard")

    else:
        form = CourseForm()

    return render(
        request,
        "courses/instructor/course_form.html",
        {"form": form}
    )


@login_required
@instructor_required
def course_update(request, pk):
    """
    Permite al instructor editar solo sus propios cursos.
    """
    course = get_object_or_404(
        Course,
        pk=pk,
        instructor=request.user
    )

    if request.method == "POST":
        form = CourseForm(
            request.POST,
            request.FILES,
            instance=course
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Curso actualizado correctamente."
            )

            return redirect("instructor-dashboard")

    else:
        form = CourseForm(instance=course)

    return render(
        request,
        "courses/instructor/course_form.html",
        {
            "form": form,
            "course": course
        }
    )


@login_required
@instructor_required
def course_delete(request, pk):
    """
    Permite al instructor eliminar solo sus propios cursos.
    """
    course = get_object_or_404(
        Course,
        pk=pk,
        instructor=request.user
    )

    if request.method == "POST":
        course.delete()

        messages.success(
            request,
            "Curso eliminado correctamente."
        )

        return redirect("instructor-dashboard")

    return render(
        request,
        "courses/instructor/course_confirm_delete.html",
        {"course": course}
    )


@login_required
@instructor_required
def module_create(request, course_id):
    """
    Permite al instructor crear módulos dentro de sus cursos.
    """
    course = get_object_or_404(
        Course,
        pk=course_id,
        instructor=request.user
    )

    if request.method == "POST":
        form = ModuleForm(request.POST)

        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()

            messages.success(
                request,
                "Módulo agregado correctamente."
            )

            return redirect("instructor-dashboard")

    else:
        form = ModuleForm()

    return render(
        request,
        "courses/instructor/module_form.html",
        {
            "form": form,
            "course": course
        }
    )


@login_required
@instructor_required
def lesson_create(request, module_id):
    """
    Permite al instructor crear lecciones dentro de sus módulos.
    """
    module = get_object_or_404(
        Module,
        pk=module_id,
        course__instructor=request.user
    )

    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES)

        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.module = module
            lesson.save()

            messages.success(
                request,
                "Lección agregada correctamente."
            )

            return redirect("instructor-dashboard")

    else:
        form = LessonForm()

    return render(
        request,
        "courses/instructor/lesson_form.html",
        {
            "form": form,
            "module": module
        }
    )


@login_required
@instructor_required
def module_update(request, pk):
    """
    Permite al instructor editar módulos de sus propios cursos.
    """
    module = get_object_or_404(
        Module,
        pk=pk,
        course__instructor=request.user
    )

    if request.method == "POST":
        form = ModuleForm(request.POST, instance=module)

        if form.is_valid():
            form.save()
            messages.success(request, "Módulo actualizado correctamente.")
            return redirect("instructor-dashboard")

    else:
        form = ModuleForm(instance=module)

    return render(
        request,
        "courses/instructor/module_form.html",
        {
            "form": form,
            "course": module.course,
            "module": module
        }
    )


@login_required
@instructor_required
def module_delete(request, pk):
    """
    Permite al instructor eliminar módulos de sus propios cursos.
    """
    module = get_object_or_404(
        Module,
        pk=pk,
        course__instructor=request.user
    )

    if request.method == "POST":
        module.delete()
        messages.success(request, "Módulo eliminado correctamente.")
        return redirect("instructor-dashboard")

    return render(
        request,
        "courses/instructor/module_confirm_delete.html",
        {"module": module}
    )


@login_required
@instructor_required
def lesson_update(request, pk):
    """
    Permite al instructor editar lecciones de sus propios módulos.
    """
    lesson = get_object_or_404(
        Lesson,
        pk=pk,
        module__course__instructor=request.user
    )

    if request.method == "POST":
        form = LessonForm(request.POST, request.FILES, instance=lesson)

        if form.is_valid():
            form.save()
            messages.success(request, "Lección actualizada correctamente.")
            return redirect("instructor-dashboard")

    else:
        form = LessonForm(instance=lesson)

    return render(
        request,
        "courses/instructor/lesson_form.html",
        {
            "form": form,
            "module": lesson.module,
            "lesson": lesson
        }
    )


@login_required
@instructor_required
def lesson_delete(request, pk):
    """
    Permite al instructor eliminar lecciones de sus propios módulos.
    """
    lesson = get_object_or_404(
        Lesson,
        pk=pk,
        module__course__instructor=request.user
    )

    if request.method == "POST":
        lesson.delete()
        messages.success(request, "Lección eliminada correctamente.")
        return redirect("instructor-dashboard")

    return render(
        request,
        "courses/instructor/lesson_confirm_delete.html",
        {"lesson": lesson}
    )


@login_required
@instructor_required
def quiz_create(request, course_id):
    """
    Permite al instructor crear el examen final de uno de sus cursos.
    """
    course = get_object_or_404(
        Course,
        pk=course_id,
        instructor=request.user
    )

    if hasattr(course, "quiz"):
        messages.info(request, "Este curso ya tiene un examen final.")
        return redirect("quiz-update", pk=course.quiz.pk)

    if request.method == "POST":
        form = QuizForm(request.POST)

        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()

            messages.success(request, "Examen creado correctamente.")
            return redirect("instructor-dashboard")

    else:
        form = QuizForm()

    return render(
        request,
        "courses/instructor/quiz_form.html",
        {
            "form": form,
            "course": course
        }
    )


@login_required
@instructor_required
def quiz_update(request, pk):
    """
    Permite al instructor editar el examen final de su curso.
    """
    quiz = get_object_or_404(
        Quiz,
        pk=pk,
        course__instructor=request.user
    )

    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)

        if form.is_valid():
            form.save()
            messages.success(request, "Examen actualizado correctamente.")
            return redirect("instructor-dashboard")

    else:
        form = QuizForm(instance=quiz)

    return render(
        request,
        "courses/instructor/quiz_form.html",
        {
            "form": form,
            "course": quiz.course,
            "quiz": quiz
        }
    )


@login_required
@instructor_required
def quiz_delete(request, pk):
    """
    Permite al instructor eliminar el examen final de su curso.
    """
    quiz = get_object_or_404(
        Quiz,
        pk=pk,
        course__instructor=request.user
    )

    if request.method == "POST":
        quiz.delete()
        messages.success(request, "Examen eliminado correctamente.")
        return redirect("instructor-dashboard")

    return render(
        request,
        "courses/instructor/quiz_confirm_delete.html",
        {"quiz": quiz}
    )


@login_required
@instructor_required
def question_create(request, quiz_id):
    """
    Permite al instructor agregar preguntas al examen.
    """
    quiz = get_object_or_404(
        Quiz,
        pk=quiz_id,
        course__instructor=request.user
    )

    if request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()

            messages.success(request, "Pregunta agregada correctamente.")
            return redirect("instructor-dashboard")

    else:
        form = QuestionForm()

    return render(
        request,
        "courses/instructor/question_form.html",
        {
            "form": form,
            "quiz": quiz
        }
    )


@login_required
@instructor_required
def question_update(request, pk):
    """
    Permite al instructor editar preguntas de sus exámenes.
    """
    question = get_object_or_404(
        Question,
        pk=pk,
        quiz__course__instructor=request.user
    )

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            form.save()
            messages.success(request, "Pregunta actualizada correctamente.")
            return redirect("instructor-dashboard")

    else:
        form = QuestionForm(instance=question)

    return render(
        request,
        "courses/instructor/question_form.html",
        {
            "form": form,
            "quiz": question.quiz,
            "question": question
        }
    )


@login_required
@instructor_required
def question_delete(request, pk):
    """
    Permite al instructor eliminar preguntas de sus exámenes.
    """
    question = get_object_or_404(
        Question,
        pk=pk,
        quiz__course__instructor=request.user
    )

    if request.method == "POST":
        question.delete()
        messages.success(request, "Pregunta eliminada correctamente.")
        return redirect("instructor-dashboard")

    return render(
        request,
        "courses/instructor/question_confirm_delete.html",
        {"question": question}
    )


@login_required
@instructor_required
def answer_create(request, question_id):
    """
    Permite al instructor agregar opciones de respuesta.
    """
    question = get_object_or_404(
        Question,
        pk=question_id,
        quiz__course__instructor=request.user
    )

    if request.method == "POST":
        form = AnswerOptionForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()

            messages.success(request, "Opción agregada correctamente.")
            return redirect("instructor-dashboard")

    else:
        form = AnswerOptionForm()

    return render(
        request,
        "courses/instructor/answer_form.html",
        {
            "form": form,
            "question": question
        }
    )


@login_required
@instructor_required
def answer_update(request, pk):
    """
    Permite al instructor editar opciones de respuesta.
    """
    answer = get_object_or_404(
        AnswerOption,
        pk=pk,
        question__quiz__course__instructor=request.user
    )

    if request.method == "POST":
        form = AnswerOptionForm(request.POST, instance=answer)

        if form.is_valid():
            form.save()
            messages.success(request, "Opción actualizada correctamente.")
            return redirect("instructor-dashboard")

    else:
        form = AnswerOptionForm(instance=answer)

    return render(
        request,
        "courses/instructor/answer_form.html",
        {
            "form": form,
            "question": answer.question,
            "answer": answer
        }
    )


@login_required
@instructor_required
def answer_delete(request, pk):
    """
    Permite al instructor eliminar opciones de respuesta.
    """
    answer = get_object_or_404(
        AnswerOption,
        pk=pk,
        question__quiz__course__instructor=request.user
    )

    if request.method == "POST":
        answer.delete()
        messages.success(request, "Opción eliminada correctamente.")
        return redirect("instructor-dashboard")

    return render(
        request,
        "courses/instructor/answer_confirm_delete.html",
        {"answer": answer}
    )


@login_required
def take_quiz(request, course_id):
    """
    Permite al estudiante rendir el examen final.
    Máximo 2 intentos.
    Si aprueba, genera certificado.
    """

    course = get_object_or_404(
        Course,
        pk=course_id,
        is_published=True
    )

    quiz = get_object_or_404(
        Quiz,
        course=course,
        is_active=True
    )

    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course,
        status="paid"
    ).first()

    if not enrollment:
        return HttpResponseForbidden(
            "Debes inscribirte y pagar el curso para rendir el examen."
        )

    if enrollment.progress_percentage < 100:
        return HttpResponseForbidden(
            "Debes completar todas las lecciones antes de rendir el examen."
        )

    approved_attempt = QuizAttempt.objects.filter(
        enrollment=enrollment,
        quiz=quiz,
        passed=True
    ).first()

    if approved_attempt:
        certificate = Certificate.objects.filter(
            enrollment=enrollment
        ).first()

        return render(
            request,
            "courses/student/quiz_result.html",
            {
                "quiz": quiz,
                "course": course,
                "score": approved_attempt.score,
                "passed": True,
                "attempts_used": QuizAttempt.objects.filter(
                    enrollment=enrollment,
                    quiz=quiz
                ).count(),
                "max_attempts": 2,
                "certificate": certificate,
            }
        )

    attempts_used = QuizAttempt.objects.filter(
        enrollment=enrollment,
        quiz=quiz
    ).count()

    max_attempts = 2

    if attempts_used >= max_attempts:
        return render(
            request,
            "courses/student/quiz_result.html",
            {
                "quiz": quiz,
                "course": course,
                "score": 0,
                "passed": False,
                "attempts_used": attempts_used,
                "max_attempts": max_attempts,
                "no_attempts_left": True,
                "certificate": None,
            }
        )

    if request.method == "POST":

        total_points = 0
        earned_points = 0

        for question in quiz.questions.all():

            total_points += question.points

            selected_option_id = request.POST.get(
                f"question_{question.id}"
            )

            if selected_option_id:

                selected_option = AnswerOption.objects.filter(
                    id=selected_option_id,
                    question=question
                ).first()

                if selected_option and selected_option.is_correct:
                    earned_points += question.points

        score = 0

        if total_points > 0:
            score = round(
                (earned_points / total_points) * 100
            )

        passed = score >= quiz.passing_score

        attempt = QuizAttempt.objects.create(
            quiz=quiz,
            enrollment=enrollment,
            score=score,
            passed=passed,
            attempt_number=attempts_used + 1
        )

        certificate = None

        if passed:
            enrollment.mark_as_completed()

            certificate, created = Certificate.objects.get_or_create(
                enrollment=enrollment
            )

            messages.success(
                request,
                "Aprobaste el examen final. Tu certificado ya está disponible."
            )
        else:
            messages.warning(
                request,
                "No alcanzaste el puntaje mínimo."
            )

        return render(
            request,
            "courses/student/quiz_result.html",
            {
                "quiz": quiz,
                "course": course,
                "score": score,
                "passed": passed,
                "attempts_used": attempt.attempt_number,
                "max_attempts": max_attempts,
                "certificate": certificate,
            }
        )

    return render(
        request,
        "courses/student/take_quiz.html",
        {
            "quiz": quiz,
            "course": course,
            "attempts_used": attempts_used,
            "max_attempts": max_attempts,
        }
    )

@login_required
def add_review(request, course_id):
    """
    Permite a un estudiante dejar una reseña de un curso pagado.
    Solo se permite una reseña por estudiante y curso.
    """

    course = get_object_or_404(
        Course,
        pk=course_id,
        is_published=True
    )

    enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course,
        status="paid"
    ).first()

    if not enrollment:
        return HttpResponseForbidden(
            "Solo puedes reseñar cursos en los que estás inscrito y pagado."
        )

    if Review.objects.filter(student=request.user, course=course).exists():
        messages.info(
            request,
            "Ya dejaste una reseña para este curso."
        )
        return redirect("course-detail-web", pk=course.pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.student = request.user
            review.course = course
            review.save()

            messages.success(
                request,
                "Tu reseña fue publicada correctamente."
            )

    return redirect("course-detail-web", pk=course.pk)