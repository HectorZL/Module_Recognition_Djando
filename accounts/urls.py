from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Perfil
    path('profile/', views.profile_view, name='profile'),
    
    # Notas
    path('notes/', views.NoteListView.as_view(), name='note_list'),
    path('notes/add/', views.NoteCreateView.as_view(), name='note_create'),
    path('notes/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_update'),
    path('notes/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    
    # Administración
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/<int:user_id>/toggle/', views.toggle_user_status, name='toggle_user_status'),
]
