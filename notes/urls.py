from .views import NotesView, NotesPublicView
from django.urls import path

urlpatterns = [
    path('notes-view/', NotesView.as_view()),
    path('notes-public/', NotesPublicView.as_view()),

]
