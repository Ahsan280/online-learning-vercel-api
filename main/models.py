from django.db import models
from userauth.models import User
from moviepy.editor import VideoFileClip
from django.db.models import Avg, Count

# Create your models here.

class Instructor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_instructor')
    full_name = models.CharField(max_length=100)
    email=models.EmailField(max_length=100, unique=True)
    description=models.TextField()
    profile_picture=models.ImageField(upload_to="instructor/profile_pictures")
    qualifications=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True, null=True)
    updated_at=models.DateTimeField(auto_now=True, null=True)
    def __str__(self):
        return self.full_name


class Category(models.Model):
    name=models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural="Categories"
    def __str__(self):
        return self.name


class Course(models.Model):
    Instructor=models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='course')
    name=models.CharField(max_length=100)
    description=models.TextField()
    category=models.ManyToManyField(Category)
    image=models.ImageField(upload_to="courses/images", null=True)
    price=models.DecimalField(null=True, decimal_places=2, max_digits=10)
    is_available_to=models.ManyToManyField(User)
    created_at=models.DateTimeField(auto_now_add=True, null=True)
    updated_at=models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name
    def averageRating(self):
        reviews=ReviewRating.objects.filter(course=self).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
        return avg
    def countReview(self):
        reviews = ReviewRating.objects.filter(course=self).aggregate(count=Count('id'))
        count=0
        if reviews['count'] is not None:
            count=int(reviews['count'])
        return count
    
    def enrolled_students(self):
        return self.is_available_to.all().count()
    
class ReviewRating(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_reviews')
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review')
    review=models.TextField()
    rating=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.review

class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lectures')
    name=models.CharField(max_length=100)
    video=models.FileField(upload_to="lectrue/videos")
    is_available_to=models.ManyToManyField(User, null=True)
    created_at=models.DateTimeField(auto_now_add=True, null=True)
    updated_at=models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.name
    def video_duration(self):
        video_path = self.video.path
        clip = VideoFileClip(video_path)
        duration = clip.duration
        clip.close()  # Close the video clip
        return duration