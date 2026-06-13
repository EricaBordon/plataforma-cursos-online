from django.contrib import admin
from .models import Category, Course, Module, Lesson, Review


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "instructor",
        "category",
        "price",
        "is_published",
        "created_at",
    )
    list_filter = ("is_published", "category", "created_at")
    search_fields = ("title", "description", "instructor__email")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title", "course__title")
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "module", "order", "duration")
    list_filter = ("module",)
    search_fields = ("title", "module__title")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "student",
        "rating",
        "created_at",
    )

    list_filter = (
        "rating",
        "created_at",
    )