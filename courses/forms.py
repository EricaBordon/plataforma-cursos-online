from django import forms

from .models import Course, Module, Lesson, Quiz, Question, AnswerOption

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "category",
            "title",
            "description",
            "price",
            "thumbnail",
            "is_published",
        ]


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = [
            "title",
            "order",
        ]


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = [
            "title",
            "content",
            "video",
            "attachment",
            "duration",
            "order",
        ]

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            "title",
            "description",
            "passing_score",
            "is_active",
        ]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            "text",
            "order",
            "points",
        ]


class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = [
            "text",
            "is_correct",
        ]