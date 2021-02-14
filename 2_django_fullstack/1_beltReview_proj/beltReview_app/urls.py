from django.urls import path
from . import views

urlpatterns = [
    # --------------------------------------------------------------
    # Homepage, etc
    # --------------------------------------------------------------
    path('', views.index),
    path('login_submission', views.login_submission),
    path('books', views.books),
    path('registration_submission', views.registration_submission),
    path('logout', views.logout),
    # --------------------------------------------------------------
    # books, etc
    # --------------------------------------------------------------
    path('books/add', views.books_add)
]
