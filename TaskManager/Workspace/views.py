from django.shortcuts import render, redirect, HttpResponse
from .models import Tasks
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Homepage view 
def homepage(request):
    all_tasks = Tasks.objects.all()
    context = {'all_tasks': all_tasks}
    return render(request, 'Workspace/index.html', context)

# Add Task view 
@login_required(login_url='/login/')
def add_task(request):
    if request.method == "POST":
        taskname = request.POST.get('taskname')
        description = request.POST.get('taskdes')
        date = request.POST.get('duedate')

        # Create a new task and save it
        Tasks.objects.create(task_name=taskname, description=description, due_date=date)

        messages.success(request, "Task added successfully.")
        return redirect('/') 
    return render(request, 'Workspace/add_tasks.html')

# Delete Task view
@login_required(login_url='/login/')
def delete(request, id):
    try:
        task = Tasks.objects.get(id=id)
        task.delete()
        messages.success(request, "Task deleted successfully.")
    except Tasks.DoesNotExist:
        messages.error(request, "Task not found.")
    return redirect('/')

# Update Task view
@login_required(login_url='/login/')
def update(request, id):
    task = Tasks.objects.get(id=id)

    if request.method == "POST":
        task_name = request.POST.get('taskname')
        task_des = request.POST.get('taskdes')

        
        completed  = request.POST.get('completion') == 'on'
        
        task.completion = completed

       
        
        task.task_name = task_name
        task.description = task_des
        task.save()

        messages.success(request, "Task updated successfully.")
        return redirect('/')

    context = {'task': task}
    return render(request, 'Workspace/update.html', context)

# Logout view 
def logout_page(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('/')

# Login view
from django.http import JsonResponse
import json

def login_page(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login successful"}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return render(request, 'login/login.html')


# Registration view
import json
from django.http import JsonResponse

def register(request):
    if request.method == "POST":
        try:
            # Handle both fetch() JSON and form submission
            if request.headers.get('Content-Type') == 'application/json':
                data = json.loads(request.body)
                username = data.get('username')
                first_name = data.get('firstname')
                last_name = data.get('lastname')
                email = data.get('email')
                password = data.get('password')
            else:
                # fallback for regular form submission
                username = request.POST.get('username')
                first_name = request.POST.get('firstname')
                last_name = request.POST.get('lastname')
                email = request.POST.get('email')
                password = request.POST.get('password')

            if not all([username, first_name, last_name, email, password]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists.'}, status=400)

            # Create and save the new user
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()

            return JsonResponse({'message': 'Account created successfully. Please log in.'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'register/register.html')
