from django.shortcuts import render, redirect
from .models import User, Book, Review
from django.contrib import messages
import bcrypt

# start of landing page
def index(request):
    return render(request, "index.html")

def login_submission(request):
    errors = User.objects.login_validator(request.POST)
    print("*-* *-* *-* *-* *-*")
    print(errors)
    print("*-* *-* *-* *-* *-*")

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        # if we get True after checking the password, we may put the user id in session
        users_with_email = User.objects.filter(email=request.POST['email'])
        # request.session must match the same as registration! ie => 'logged_ID'
        request.session['logged_ID'] = users_with_email[0].id
        # never render on a post, always redirect!
        return redirect('/books')


def logout(request):
    request.session.clear()

    return redirect('/')


def registration_submission(request):
    errors = User.objects.register_validator(request.POST)
    print("*-* *-* *-* *-* *-*")
    print(errors)
    print("*-* *-* *-* *-* *-*")

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    else:
        # encrypt password first!
        securedpw = bcrypt.hashpw(
            request.POST['pw'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            fname=request.POST["fname"], lname=request.POST["lname"], email=request.POST["email"], pw=securedpw)
        request.session['logged_ID'] = new_user.id

    return redirect('/books')

# start of books
def books(request):
    if 'logged_ID' not in request.session:
        messages.error(
            request, "Please log in or create an account before trying to continue.")

        return redirect('/')

    context = {
        'loggedIn_user': User.objects.get(id=request.session['logged_ID'])
    }

    return render(request, 'books.html', context)


def books_add(request):
    if 'logged_ID' not in request.session:
        messages.error(
            request, "Please log in or create an account before trying to continue.")

    context = {
        "books": Book.objects.all(),
        "reviews": Review.objects.all(),
    }

    return render(request, "books_add.html", context)
