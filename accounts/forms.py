from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, Note

class UserLoginForm(AuthenticationForm):
    """Formulario personalizado para el inicio de sesión."""
    username = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('correo@ejemplo.com'),
            'autofocus': True
        })
    )
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Contraseña')
        })
    )

    error_messages = {
        'invalid_login': _(
            "Por favor ingrese un correo y contraseña correctos. "
            "Note que ambos campos pueden ser sensibles a mayúsculas y minúsculas."
        ),
        'inactive': _("Esta cuenta está inactiva."),
    }


class UserRegistrationForm(UserCreationForm):
    """Formulario para el registro de nuevos usuarios."""
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('correo@ejemplo.com')
        })
    )
    first_name = forms.CharField(
        label=_("Nombre"),
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Nombre')
        })
    )
    last_name = forms.CharField(
        label=_("Apellido"),
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Apellido')
        })
    )
    password1 = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Contraseña')
        }),
        help_text=_(
            "Su contraseña no puede ser demasiado similar a su otra información personal.<br>"
            "Su contraseña debe contener al menos 8 caracteres.<br>"
            "Su contraseña no puede ser una contraseña de uso común.<br>"
            "Su contraseña no puede ser enteramente numérica."
        )
    )
    password2 = forms.CharField(
        label=_("Confirmación de contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirmar contraseña')
        }),
        help_text=_("Ingrese la misma contraseña que antes, para verificación.")
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Este correo electrónico ya está en uso. Por favor, utilice otro."))
        return email


class UserProfileForm(forms.ModelForm):
    """Formulario para actualizar el perfil del usuario."""
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'profile_picture')
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Teléfono')}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Dirección')}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class NoteForm(forms.ModelForm):
    """Formulario para crear y editar notas."""
    class Meta:
        model = Note
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Título de la nota')
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Contenido de la nota...')
            }),
        }
        labels = {
            'title': _('Título'),
            'content': _('Contenido'),
        }
