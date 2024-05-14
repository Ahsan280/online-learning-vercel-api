from rest_framework import serializers
from .models import Instructor, Course, Category, Lecture, ReviewRating



class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lecture
        fields=['id', 'course', 'name', 'video', 'is_available_to', 'video_duration']
        
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Instructor
        fields='__all__'

class InstructorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=Instructor
        fields='__all__'
        depth=1
        
class ReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReviewRating
        fields='__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ReviewRating
        fields='__all__'
        depth=1
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        
class CourseSerializer(serializers.ModelSerializer):
    # category=CategorySerializer()
    class Meta:
        model=Course
        fields='__all__'
        # depth=1

class CourseDetailSerializer(serializers.ModelSerializer):
    # category=CategorySerializer()
    class Meta:
        model=Course
        fields=['id', 'Instructor', 'name',
                'description', 'category',
                'image', 'price',
                'is_available_to', 'created_at',
                'updated_at', 'enrolled_students',
                'averageRating', 'countReview']
        depth=1