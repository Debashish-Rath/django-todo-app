from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import TodoItem
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import send_mail
from TODO import settings


# Dashboard
def index(request):
    items = TodoItem.objects.filter(user_id=request.user.id)
    return render(request, 'index.html', {'items': items})


'''
CRUD Functionalities

add_todo_item --> creates a todo record in the database
update_todo_item --> updates the todo record of corresponding todo_id of the user
delete_todo_item --> deletes todo record

'''


def add_todo_item(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        todo_obj = TodoItem.objects.create(
            title=title, description=description, user_id=request.user.id)
        todo_obj.save()

        user_obj = User.objects.filter(username=request.user)

        user_email_list = []
        for row in user_obj:
            user_email_list.append(row.email)

        send_todo_added_email(title, description, user_email_list)
    return redirect('/')


def update_todo_item(request, todo_id):
    try:
        item = TodoItem.objects.get(pk=todo_id)
        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            completion_status = request.POST['status']
            item.title = title
            item.description = description

            status = False
            if completion_status == 'Completed':
                status = True

            item.completed = status
            item.save()
    except TodoItem.DoesNotExist:
        return JsonResponse({"error": "Error Occured during updation !!!"})
    return redirect('/')


def delete_todo_item(request, todo_id):
    try:
        item = TodoItem.objects.get(pk=todo_id)
        item.delete()
    except TodoItem.DoesNotExist:
        pass
    return redirect('/')


'''User Authentication System ( Register, Login, Logout )'''


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if len(password) < 8:
            messages.info(
                request, 'Password Length Should be greater than 8 !!!')
            return redirect('register')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User already exists !!!')
                return redirect('register')

            user = User.objects.create(
                username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            user.set_password(password)
            user.save()

            return redirect('login_user')
        else:
            messages.info(
                request, "Password & Confirm Passwords didn't Match  !!! Please Try Again ")
    return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'Invalid Credentials !!!')
            return redirect("login_user")
    return render(request, 'login.html')


def logout_user(request):
    auth.logout(request)
    return redirect('/')


def send_todo_added_email(title, description, recipients):
    subject = 'New TODO Item Added'
    message = f'A new TODO item has been added: \n\nTitle: {title}\n\n'\
        f"Description: {description}\n\n"

    from_email = settings.EMAIL_HOST_USER
    recipient_list = recipients
    send_mail(subject, message, from_email, recipient_list)
