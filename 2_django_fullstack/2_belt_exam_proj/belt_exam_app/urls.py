from django.urls import path
from . import views

urlpatterns = [
    # --------------------------------------------------------------
    # Homepage, etc
    # --------------------------------------------------------------
    path('', views.index),
    path('login_submission', views.login_submission),
    path('registration_submission', views.registration_submission),
    path('quotes', views.quotes),
    path('logout', views.logout),
    # --------------------------------------------------------------
    # quotes_submission, etc
    # --------------------------------------------------------------
    path('quote_post', views.quote_post),
    path('like/<int:quoteID>', views.like),
    # path('dislike/<int:quoteID>', views.dislike),
    path('user/<int:userID>', views.user_quotes),
    path('edit_account', views.edit_account),
    path('update_account', views.update_account),
    path('delete_comment/<int:quoteID>', views.delete_comment),
]