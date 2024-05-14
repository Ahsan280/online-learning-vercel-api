from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresg"),
    path('register/', views.RegisterationView.as_view(), name='register'),
    path('dashboard/<int:pk>/', views.UserDetailView.as_view(), name='dashboard'),
    path('update-profile/<int:user_id>/', views.update_profile),
    path('change-password/<int:user_id>/', views.change_password)
]
