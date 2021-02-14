from django.shortcuts import render, redirect
from .models import Book, Author, User
from django.contrib import messages
import bcrypt


# Homepage, etc
def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


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
        return redirect('/home')


def logout(request):
    request.session.clear()

    return redirect('/')


def home(request):
    if 'logged_ID' not in request.session:
        messages.error(
            request, "Please log in or create an account before trying to continue.")

        return redirect('/')

    context = {
        'loggedIn_user': User.objects.get(id=request.session['logged_ID'])
    }

    return render(request, 'home.html', context)


def register(request):
    return render(request, 'registration.html')


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

    return redirect('/home')


# Books
def books(request):
    if 'logged_ID' not in request.session:
        messages.error(
            request, "Please log in or create an account before trying to continue.")

        return redirect('/')

    context = {
        "books": Book.objects.all(),
    }

    return render(request, 'books.html', context)


def add_book(request):
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')

    Book.objects.create(
        title=request.POST["title"], desc=request.POST["desc"])

    return redirect('/books')


def edit_book(request, bookID):
    if 'logged_ID' not in request.session:
        messages.error(
            request, "Please log in or create an account before trying to continue.")

        return redirect('/')

    non_authors = Author.objects.exclude(books=Book.objects.get(id=bookID))
    exclude_authors = Author.objects.filter(books=Book.objects.get(id=bookID))

    context = {
        "book_to_show": Book.objects.get(id=bookID),
        "authors_of_book": Book.objects.get(id=bookID).authors.all(),
        "authors": Author.objects.all(),
        "non_authors": non_authors,
        "exclude_authors": exclude_authors,
    }

    return render(request, "book_info.html", context)


def delete_book(request, bookID):
    Book.objects.get(id=bookID).delete()

    return redirect('/books')


def edit_book_objects(request, bookID):
    # validation
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_book/{bookID}')

    # edit/save info in db fields
    book = Book.objects.get(id=bookID)
    book.title = request.POST['title']
    book.save()

    book = Book.objects.get(id=bookID)
    book.desc = request.POST['desc']
    book.save()

    return redirect(f'/edit_book/{bookID}')


def add_auth2book(request, bookID):
    selected_author = Author.objects.get(id=request.POST['auth_to_book'])
    selected_author.books.add(bookID)

    return redirect(f'/edit_book/{bookID}')


def remove_auth2book(request, bookID):
    selected_author = Author.objects.get(id=request.POST['auth_to_book'])
    selected_author.books.remove(bookID)

    return redirect(f'/edit_book/{bookID}')


# Authors
def authors(request):
    if 'logged_ID' not in request.session:
        messages.error(
            request, "Please log in or create an account before trying to continue.")

        return redirect('/')

    context = {
        "authors": Author.objects.all(),
    }

    return render(request, 'authors.html', context)


def add_author(request):
    errors = Author.objects.author_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/authors')

    Author.objects.create(
        first_name=request.POST["first_name"], last_name=request.POST["last_name"],
        notes=request.POST["notes"])

    return redirect('/authors')


def delete_author(request, authorID):
    Author.objects.get(id=authorID).delete()

    return redirect('/authors')


def edit_author(request, authorID):
    if 'logged_ID' not in request.session:
        messages.error(
            request, "Please log in or create an account before trying to continue.")

        return redirect('/')

    non_books = Book.objects.exclude(authors=Author.objects.get(id=authorID))
    exclude_books = Book.objects.filter(
        authors=Author.objects.get(id=authorID))

    context = {
        "author_to_show": Author.objects.get(id=authorID),
        "books_of_author": Author.objects.get(id=authorID).books.all(),
        "books": Book.objects.all(),
        "non_books": non_books,
        "exclude_books": exclude_books,
    }

    return render(request, "author_info.html", context)


def edit_author_objects(request, authorID):
    errors = Author.objects.author_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/edit_author/{authorID}')

    author = Author.objects.get(id=authorID)
    author.first_name = request.POST['first_name']
    author.save()

    author = Author.objects.get(id=authorID)
    author.last_name = request.POST['last_name']
    author.save()

    author = Author.objects.get(id=authorID)
    author.notes = request.POST['notes']
    author.save()

    return redirect(f'/edit_author/{authorID}')


def add_book2auth(request, authorID):
    selected_book = Book.objects.get(id=request.POST['book_to_auth'])
    selected_book.authors.add(authorID)

    return redirect(f'/edit_author/{authorID}')


def remove_book2auth(request, authorID):
    selected_book = Book.objects.get(id=request.POST['book_to_auth'])
    selected_book.authors.remove(authorID)

    return redirect(f'/edit_author/{authorID}')
