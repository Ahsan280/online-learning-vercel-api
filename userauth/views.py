from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from django.views.decorators.csrf import csrf_exempt
from .serializers import MyTOKS, UserSerializer, RegisterationSerializer
# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTOKS

class RegisterationView(generics.CreateAPIView):
    serializer_class=RegisterationSerializer
    queryset=User.objects.all()
    permission_classes=[AllowAny]

class UserDetailView(generics.RetrieveAPIView):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    permission_classes=[IsAuthenticated]

@csrf_exempt
def update_profile(request, user_id):
    try:
        user=User.objects.get(id=user_id)
        if(request.POST.get('full_name')=='' or request.FILES.get('profile_picture')==None):
            print("Inside if--- Profile Picture", request.FILES.get('profile_picture'))
            return JsonResponse({'status':'failed'})
        full_name=request.POST.get('full_name')
        [first_name, last_name]=full_name.split(' ')
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        user.profile.full_name=request.POST.get('full_name')
        user.profile.profile_picture=request.FILES.get('profile_picture')
        user.profile.save()
        return JsonResponse({'status':'success'})
    except Exception as e:
        print(e)
        print("Inside except--- Profile Picture", request.FILES.get('profile_picture'))
        return JsonResponse({'status':'failed'})

@csrf_exempt
def change_password(request, user_id):
    try:
        user=User.objects.get(id=user_id)
        old_password=request.POST.get('old_password')
        password=request.POST.get('password')
        confirm_password=request.POST.get('password2')
        if confirm_password!=password:
            return JsonResponse({'message':"Password and Confirm Password do not match"})
        
        success=user.check_password(old_password)
        if not success:
            return JsonResponse({'message':"Old Password is incorrect"})
        user.set_password(password)
        user.save()
        return JsonResponse({'message':"Password changed successfully"})
    except:
        return JsonResponse({'message':"Something went wrong"})