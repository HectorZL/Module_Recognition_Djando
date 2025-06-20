from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
import os

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model that uses email as the unique identifier."""
    
    username = None
    email = models.EmailField(_('correo electrónico'), unique=True)
    first_name = models.CharField(_('nombre'), max_length=30, blank=False)
    last_name = models.CharField(_('apellido'), max_length=150, blank=False)
    is_admin = models.BooleanField(_('es administrador'), default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    class Meta:
        verbose_name = _('usuario')
        verbose_name_plural = _('usuarios')


def user_profile_image_path(instance, filename):
    """File will be uploaded to MEDIA_ROOT/users/<id>/<filename>"""
    return f'users/{instance.user.id}/{filename}'


class UserProfile(models.Model):
    """Extended user profile information."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile'
    )
    phone = models.CharField(_('teléfono'), max_length=20, blank=True)
    address = models.TextField(_('dirección'), blank=True)
    profile_picture = models.ImageField(
        _('foto de perfil'),
        upload_to=user_profile_image_path,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ]
    )
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('última actualización'), auto_now=True)
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"
    
    class Meta:
        verbose_name = _('perfil de usuario')
        verbose_name_plural = _('perfiles de usuario')


class Note(models.Model):
    """Notes associated with users."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name=_('usuario')
    )
    title = models.CharField(_('título'), max_length=200)
    content = models.TextField(_('contenido'))
    created_at = models.DateTimeField(_('fecha de creación'), auto_now_add=True)
    updated_at = models.DateTimeField(_('última actualización'), auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"
    
    class Meta:
        verbose_name = _('nota')
        verbose_name_plural = _('notas')
        ordering = ['-updated_at']
