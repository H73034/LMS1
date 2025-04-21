from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Course, Lesson, Progress, Quiz, Question, UserQuizResult

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CourseForm




def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

# views.py

# views.py
@login_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user  # Set instructor to logged-in user

            # Only allow admin users to upload videos
            if not request.user.is_staff:
                course.video = None  # Remove video field for non-admins

            course.save()
            messages.success(request, "Course added successfully!")
            return redirect('home')
    else:
        form = CourseForm()

        # Hide the video field if the user is not an admin
        if not request.user.is_staff:
            form.fields.pop('video')

    return render(request, 'lms/add_course.html', {'form': form})



# Custom decorator to check if the user is an Instructor
def instructor_required(view_func):
    return user_passes_test(lambda u: u.groups.filter(name='Instructor').exists())(view_func)

# Example view that only Instructors should have access to
@instructor_required
def instructor_dashboard(request):
    return render(request, 'instructor_dashboard.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    courses = Course.objects.all()
    return render(request, 'lms/home.html', {'courses': courses})



def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "User registered successfully")
            return redirect('login')
    return render(request, 'lms/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'lms/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
