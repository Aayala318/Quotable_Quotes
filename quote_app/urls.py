from django.contrib.messages.api import success
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("success", views.success),
    path("login", views.login),
    path("quotes", views.show_all),
    path("quotes/create", views.create_quote),
    path("quotes/<int:user_id>", views.show_one),
    path("quotes/<int:quote_id>/edit", views.edit),
    path("quotes/<int:quote_id>/update", views.update),
    path("quotes/<int:quote_id>/delete", views.delete),
    path("favorite/<int:quote_id>", views.favorite),
    path("unfavorite/<int:quote_id>", views.unfavorite),
    path("logout", views.logout)
]