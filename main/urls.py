from django.urls import path
from .import views
urlpatterns = [
    path('all-courses/', views.AllCourses.as_view(), name='all-courses'),
    path('latest-courses/', views.LatestCourses.as_view()),
    path('all-latest-courses/', views.AllLatestCourses.as_view()),
    path('all-category/', views.CategoryList.as_view(), name='category-list'),
    path('create-instructor/', views.CreateInstructor.as_view(), name='create-instructor'),
    path('instructor-list/', views.InstructorList.as_view(), name='instructor-list'),
    path('instructor-by-user/<int:pk>/', views.GetInstructorByUser.as_view(), name='instructor-by-user'),
    path('create-course/', views.CreateCourse.as_view(), name="create-course"),
    path("instructor-courses/<int:instructor_id>/", views.InstructorCourses.as_view(), name="instructor-courses"),
    path("instructor-detail-courses/<int:instructor_id>/", views.InstructorDetailCourses.as_view(),),
    path('course-detail/<int:pk>/', views.CourseDetail.as_view(), name='course-detail'),
    path('add-lecture/', views.AddLecture.as_view(), name='add-lecture'),
    path('lecture-list/<int:course_id>/', views.LectureList.as_view(), name="lecture-list"),
    path('check_is_instructor/<int:course_id>/<int:user_id>/', views.check_is_instructor, name="check"),
    path('check_is_available/<int:course_id>/<int:user_id>/', views.check_is_available, name='is_available'),
    path('make_course_available/<int:course_id>/<int:user_id>/', views.make_course_available),
    path('enrolled_courses/<int:user_id>/', views.EnrolledCourses.as_view()),
    
    
    path('create-review/', views.CreateReview.as_view()),
    path('check-has-reviewd/<int:course_id>/<int:user_id>/', views.check_has_reviewed),
    path('update-review/<int:pk>/', views.UpdateReview.as_view()),
    
    path('popular-courses/', views.PopularCourses.as_view()),
    path('all-popular-courses/', views.AllPopularCourses.as_view()),
    path('delete-course/<int:pk>/', views.DeleteCourse.as_view()),
    path('course-reviews/<int:course_id>/', views.CourseReviews.as_view()),
    path('instructor-details/<int:pk>/', views.InstructorDetails.as_view()),
    path('searched-courses/<search>/', views.SearchedCourses.as_view())

]
