from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.notes_list, name='notes_list'),
    path('add-note/', views.add_note, name='add_note'),
    path('my-notes/', views.my_notes, name='my_notes'),
    path('edit-note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('view-note/<int:note_id>/', views.view_note, name='view_note'),
    path('my-notes/', views.my_notes, name='my_notes'),
    path('delete-note/<int:note_id>/', views.delete_note, name='delete_note'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]