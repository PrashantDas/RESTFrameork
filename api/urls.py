from django.urls import path, include

urlpatterns = [
    path('members/', include('members.urls')),
    path('notes/', include('notes.urls')),
]
