from django import forms

from .models import (
    Course,
    Module,
    Lesson,
    Quiz,
    Question,
    AnswerOption,
    Review,
)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["category", "title", "description", "price", "thumbnail", "is_published"]


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ["title", "order"]


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ["title", "content", "video", "attachment", "duration", "order"]


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ["title", "description", "passing_score", "is_active"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "order", "points"]


class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ["text", "is_correct"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 5,
            }),
            "comment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Escribe tu opinión sobre el curso",
            }),
        }