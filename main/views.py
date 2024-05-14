from django.shortcuts import render
from rest_framework import generics
from .serializers import CourseSerializer, CategorySerializer, InstructorSerializer, InstructorDetailSerializer,ReviewsSerializer, ReviewRatingSerializer, CourseDetailSerializer, LectureSerializer
from .models import Category, Course, Instructor, Lecture, ReviewRating
from userauth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.db.models import Q

# Create your views here.

class AllCourses(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class=CourseSerializer
    permission_classes=[AllowAny]

class LatestCourses(generics.ListAPIView):
    serializer_class=CourseSerializer
    permission_classes=[AllowAny]
    def get_queryset(self):
        courses=Course.objects.all().order_by('-created_at')[:6]
        return courses

class AllLatestCourses(generics.ListAPIView):
    serializer_class=CourseSerializer
    permission_classes=[AllowAny]
    def get_queryset(self):
        courses=Course.objects.all().order_by('-created_at')
        return courses
class PopularCourses(generics.ListAPIView):
    serializer_class=CourseSerializer
    permission_classes=[AllowAny]
    def get_queryset(self):
        courses=Course.objects.all()
        return courses
    
class CreateInstructor(generics.CreateAPIView):
    queryset = Instructor.objects.all()
    serializer_class=InstructorSerializer
    permission_classes=[IsAuthenticated]

class InstructorList(generics.ListAPIView):
    queryset = Instructor.objects.all()
    serializer_class=InstructorSerializer
    permission_classes=[AllowAny]
    
class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class=CategorySerializer

class CreateReview(generics.CreateAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class=ReviewRatingSerializer
    permission_classes=[IsAuthenticated]
    
class CreateCourse(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class=CourseSerializer
    def create(self, request, *args, **kwargs):
        # Here, you can customize the creation of the model instance
        request_data = request.data
        name = request_data.get('name')
        instructor_id = request_data.get('Instructor')
        
        price = request_data.get('price')
        description = request_data.get('description')
        image=request_data.get('image')
        instructor=Instructor.objects.get(id=instructor_id)
   
        
        categories_str = request_data.get('category', '')  # Get the string of category IDs
        category_ids = [int(id) for id in categories_str.split(',') if id.strip()] 
    
        category=Category.objects.filter(id__in=category_ids)
        
        course_instance = Course.objects.create(
            name=name,
            Instructor=instructor,
            price=price,
            description=description,
            image=image
        )
        course_instance.save()
        course_instance.category.set(category)
        course_instance.save()
        serializer = self.get_serializer(instance=course_instance)
        # Return the response
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class GetInstructorByUser(generics.ListAPIView):
    # queryset=Instructor.objects.all()
    serializer_class=InstructorSerializer
    permission_classes=[AllowAny]
    
    def get_queryset(self):
        user_id=self.kwargs['pk']
        user=User.objects.get(id=user_id)
        try:
            instructor=Instructor.objects.filter(user=user)
        except Instructor.DoesNotExist:
            instructor=None
        return instructor

class InstructorCourses(generics.ListAPIView):
    serializer_class=CourseSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        instructro_id=self.kwargs['instructor_id']
        instructor=Instructor.objects.get(id=instructro_id)
        courses=Course.objects.filter(Instructor=instructor)
        return courses

class InstructorDetailCourses(generics.ListAPIView):
    serializer_class=CourseSerializer
    permission_classes=[AllowAny]
    def get_queryset(self):
        instructro_id=self.kwargs['instructor_id']
        instructor=Instructor.objects.get(id=instructro_id)
        courses=Course.objects.filter(Instructor=instructor)
        return courses

class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class=CourseDetailSerializer

class InstructorDetails(generics.RetrieveAPIView):
    queryset = Instructor.objects.all()
    serializer_class=InstructorDetailSerializer
    # permission_classes=[AllowAny]

class AddLecture(generics.CreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class=LectureSerializer
    permission_classes=[IsAuthenticated]

class LectureList(generics.ListAPIView):
    serializer_class=LectureSerializer
    def get_queryset(self):
        course_id=self.kwargs['course_id']
        course=Course.objects.get(id=course_id)
        lectures=Lecture.objects.filter(course=course)
        return lectures

def check_is_instructor(request, course_id, user_id):
    try:
        user=User.objects.get(id=user_id)
        course=Course.objects.get(id=course_id)
        if course.Instructor.user==user:
            return JsonResponse({'bool':True})
        else:
            return JsonResponse({'bool':False})
    except:
        return JsonResponse({'bool':False})

def check_is_available(request, course_id, user_id):
    try:
        course=Course.objects.get(id=course_id)
        user=User.objects.get(id=user_id)
        is_available = course.is_available_to.filter(id=user_id).exists()
        if is_available:
            return JsonResponse({'bool':True})
        else:
            return JsonResponse({'bool':False})
    except:
        return JsonResponse({'bool':False})

def make_course_available(request,course_id, user_id):
    try:
        course=Course.objects.get(id=course_id)
        user=User.objects.get(id=user_id)
        course.is_available_to.add(user)
        course.save()
        return JsonResponse({'bool':True})
    except:
        return JsonResponse({'bool':False})

class EnrolledCourses(generics.ListAPIView):
    serializer_class=CourseSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        courses=Course.objects.filter(is_available_to__id=user_id)
        return courses


def check_has_reviewed(request, course_id, user_id):
    try:
        course=Course.objects.get(id=course_id)
        user=User.objects.get(id=user_id)
        review=ReviewRating.objects.filter(course=course, user=user).exists()
        if review:
            course_review=ReviewRating.objects.get(course=course, user=user)
            
            return JsonResponse({'bool':True, 'review_id':course_review.id})
        else:
            return JsonResponse({'bool':False})
    except:
        return JsonResponse({'bool':False})

class UpdateReview(generics.UpdateAPIView):
    queryset = ReviewRating.objects.all()
    serializer_class=ReviewRatingSerializer
    permission_classes=[IsAuthenticated]

class CourseReviews(generics.ListAPIView):
    serializer_class=ReviewsSerializer
    permission_classes=[AllowAny]
    
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        course=Course.objects.get(id=course_id)
        reviews=ReviewRating.objects.filter(course=course)
        return reviews
        

class DeleteCourse(generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class=CourseSerializer
    permission_classes=[IsAuthenticated]

class PopularCourses(generics.ListAPIView):
    serializer_class=CourseSerializer
    permission_classes=[AllowAny]
    def get_queryset(self):
        courses=Course.objects.all()
        popular_courses=sorted(courses, key=lambda x: x.averageRating(), reverse=True)[:6]
        return popular_courses

class AllPopularCourses(generics.ListAPIView):
    serializer_class=CourseSerializer
    permission_classes=[AllowAny]
    def get_queryset(self):
        courses=Course.objects.all()
        popular_courses=sorted(courses, key=lambda x: x.averageRating(), reverse=True)
        return popular_courses

class SearchedCourses(generics.ListAPIView):
    serializer_class=CourseSerializer
    permission_classes=[AllowAny]
    
    def get_queryset(self):
        search=self.kwargs['search']
        courses=Course.objects.filter(Q(name__icontains=search) | 
                                      Q(category__name__icontains=search) | 
                                      Q(description__contains=search))
        
        return set(courses)