from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('add_note/', views.add_note, name='add_note'),
    path('view_note/<int:pk>', views.view_note, name='view_note'),
    path('delete_note/<int:pk>', views.delete_note, name='delete_note'),
    path('update_note/<int:pk>', views.update_note, name='update_note'),
]