from django.urls import path
from .views import RegisterMemberView, LoginView, UserProfileView, AllUserSerializer

urlpatterns = [
    path('register/', RegisterMemberView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('all/', AllUserSerializer.as_view()),
]
