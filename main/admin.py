from django.contrib import admin
from .models import Instructor, Category, Course, Lecture, ReviewRating
# Register your models here.
admin.site.register(Instructor)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(ReviewRating)