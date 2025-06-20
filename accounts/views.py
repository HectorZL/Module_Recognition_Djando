from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .models import User, UserProfile, Note
from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm, NoteForm

# Vistas de autenticación
def login_view(request):
    """Vista para el inicio de sesión de usuarios."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # username es el email en nuestro caso
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, _('¡Bienvenido de nuevo!'))
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, _('Correo o contraseña incorrectos.'))
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    """Vista para el registro de nuevos usuarios."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('¡Registro exitoso! Bienvenido a nuestra plataforma.'))
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    """Vista para cerrar sesión."""
    logout(request)
    messages.info(request, _('Has cerrado sesión correctamente.'))
    return redirect('login')  # This will use Django's built-in login URL


# Vistas de perfil
@login_required
def profile_view(request):
    """Vista para ver y editar el perfil del usuario."""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, _('Perfil actualizado correctamente.'))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


# Vistas de notas
class NoteListView(LoginRequiredMixin, ListView):
    """Vista para listar las notas del usuario."""
    model = Note
    template_name = 'accounts/note_list.html'
    context_object_name = 'notes'
    
    def get_queryset(self):
        return Note.objects.filter(user=self.request.user).order_by('-updated_at')


class NoteCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear una nueva nota."""
    model = Note
    form_class = NoteForm
    template_name = 'accounts/note_form.html'
    success_url = reverse_lazy('accounts:note_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, _('Nota creada correctamente.'))
        return super().form_valid(form)


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Vista para actualizar una nota existente."""
    model = Note
    form_class = NoteForm
    template_name = 'accounts/note_form.html'
    success_url = reverse_lazy('accounts:note_list')
    
    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user
    
    def handle_no_permission(self):
        messages.error(self.request, _('No tienes permiso para editar esta nota.'))
        return redirect('accounts:note_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('Nota actualizada correctamente.'))
        return super().form_valid(form)


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Vista para eliminar una nota."""
    model = Note
    template_name = 'accounts/note_confirm_delete.html'
    success_url = reverse_lazy('accounts:note_list')
    
    def test_func(self):
        note = self.get_object()
        return self.request.user == note.user
    
    def handle_no_permission(self):
        messages.error(self.request, _('No tienes permiso para eliminar esta nota.'))
        return redirect('accounts:note_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Nota eliminada correctamente.'))
        return super().delete(request, *args, **kwargs)


# Vistas de administración
@login_required
@user_passes_test(lambda u: u.is_admin)
def admin_dashboard(request):
    """Panel de administración para usuarios con privilegios de administrador."""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/admin/dashboard.html', {'users': users})


@login_required
@user_passes_test(lambda u: u.is_admin)
def toggle_user_status(request, user_id):
    """Activar/desactivar un usuario (solo para administradores)."""
    if not request.user.is_admin:
        raise PermissionDenied
    
    user = get_object_or_404(User, id=user_id)
    if user != request.user:  # Prevenir auto-bloqueo
        user.is_active = not user.is_active
        user.save()
        status = 'activado' if user.is_active else 'desactivado'
        messages.success(request, f'Usuario {user.email} {status} correctamente.')
    
    return redirect('admin_dashboard')


# Vista de inicio
def home_view(request):
    """Página de inicio."""
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect('accounts:admin_dashboard')
        return redirect('accounts:note_list')
    return render(request, 'home.html')
