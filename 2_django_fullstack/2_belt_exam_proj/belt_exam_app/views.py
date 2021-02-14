from django.shortcuts import render, redirect
from .models import User, Quote
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
        return redirect('/')
    else:
        # if we get True after checking the password, we may put the user id in session
        users_with_email = User.objects.filter(email=request.POST['email'])
        # request.session must match the same as registration! ie => 'logged_ID'
        request.session['logged_ID'] = users_with_email[0].id
        # never render on a post, always redirect!
        return redirect('/quotes')


def registration_submission(request):
    errors = User.objects.register_validator(request.POST)
    print("*-* *-* *-* *-* *-*")
    print(errors)
    print("*-* *-* *-* *-* *-*")

    if len(errors) > 0:
        for value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        # encrypt password first!
        securedpw = bcrypt.hashpw(
            request.POST['pw'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            fname=request.POST["fname"], lname=request.POST["lname"], email=request.POST["email"], pw=securedpw)
        request.session['logged_ID'] = new_user.id

    return redirect('/quotes')


def logout(request):
    request.session.clear()

    return redirect('/')


def quotes(request):
    if 'logged_ID' not in request.session:
        messages.error(
            request, "Please log in or create an account before trying to continue.")

        return redirect('/')

    context = {
        'loggedIn_user': User.objects.get(id=request.session['logged_ID']),
        'quotes': Quote.objects.all(),
    }

    return render(request, 'quotes.html', context)


def quote_post(request):
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for value in errors.items():
            messages.error(request, value)
    else:
        loggedIn_user = User.objects.get(id=request.session['logged_ID'])
        Quote.objects.create(
            author=request.POST["author"], quote=request.POST["quote"], user=loggedIn_user)

    return redirect('/quotes')


# How to restrict number of clicks?
def like(request, quoteID):
    person_to_like_quote = User.objects.get(id=request.session['logged_ID'])
    quote_to_get_like = Quote.objects.get(id=quoteID)

    if quote_to_get_like in person_to_like_quote.liked_quotes.all():
        quote_to_get_like.likes.remove(person_to_like_quote)
    else:
        quote_to_get_like.likes.add(person_to_like_quote)

    return redirect('/quotes')


def user_quotes(request, userID):
    all_quotes = Quote.objects.all()
    users_quotes = all_quotes.filter(user_id=userID)

    context = {
        'users_quotes': users_quotes
    }

    return render(request, "userquotes.html", context)

def edit_account(request):
    curr_user = User.objects.get(id=request.session['logged_ID'])

    context = {
        'curr_user': curr_user,
    }

    return render(request, "editaccount.html", context)

def update_account(request):
    curr_user = User.objects.get(id=request.session['logged_ID'])
    errors = User.objects.update_validator(request.POST)
    print("*-* *-* *-* *-* *-*")
    print(errors)
    print("*-* *-* *-* *-* *-*")

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit_account')
    else:
        curr_user.fname = request.POST['fname']
        curr_user.lname = request.POST['lname']
        curr_user.email = request.POST['email']
        curr_user.save()

    return redirect('/edit_account')

def delete_comment(request, quoteID):
    quote_to_delete = Quote.objects.get(id=quoteID)
    quote_to_delete.delete()

    return redirect('/quotes')
