from django.urls import path

from .views import CustomPasswordChangeView, profile_edit

urlpatterns = [
    path('perfil/', profile_edit, name='profile_edit'),
    path('password/', CustomPasswordChangeView.as_view(), name='password_change'),
]
