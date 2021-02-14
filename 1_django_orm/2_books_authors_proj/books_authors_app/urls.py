from django.urls import path
from . import views

urlpatterns = [
    # -
    # Homepage, etc
    #  -
    path('', views.index),
    path('login', views.login),
    path('login_submission', views.login_submission),
    path('home', views.home),
    path('register', views.register),
    path('registration_submission', views.registration_submission),
    path('logout', views.logout),
    # -
    # books
    # -
    path('books', views.books),
    path('add_book', views.add_book),
    path('edit_book/<int:bookID>', views.edit_book),
    path('delete_book/<int:bookID>', views.delete_book),
    path('edit_book_objects/<int:bookID>', views.edit_book_objects),
    path('add_auth2book/<int:bookID>', views.add_auth2book),
    path('remove_auth2book/<int:bookID>', views.remove_auth2book),
    # -
    # authors
    # -
    path('authors', views.authors),
    path('add_author', views.add_author),
    path('edit_author/<int:authorID>', views.edit_author),
    path('delete_author/<int:authorID>', views.delete_author),
    path('edit_author_objects/<int:authorID>', views.edit_author_objects),
    path('add_book2auth/<int:authorID>', views.add_book2auth),
    path('remove_book2auth/<int:authorID>', views.remove_book2auth),
]
