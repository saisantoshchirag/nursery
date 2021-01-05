from django.contrib.auth import login,logout
from django.shortcuts import render,redirect
from .forms import LoginForm,SignupForm
from .models import Profile
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Profile.objects.create(user=user,type=request.POST['type'])
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})



def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('nursery:home')
    else:
        print(request.method)
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.login(request)

            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('nursery:home')
    else:
        form = LoginForm()
    return render(request, 'registration/login_new.html',{'form': form})

class SignupView(APIView):
    serializer = UserSerializer
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.data['password']!=request.data['password1']:
            error = {'password':'passwords doesnot match'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        if request.data['type'] not in ['Nursery','User']:
            error = {'Type':'Type should be Nursery or User'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        User.objects.create(username=request.data['username'],email=request.data['email'],password=request.data['password'])
        user = User.objects.get(username=request.data['username'])
        Profile.objects.create(user=user,type=request.data['type'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)

