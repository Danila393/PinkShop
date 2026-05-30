from django import forms
from .models import Profile
from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 999-99-99'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш адрес'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone

        clean_p = phone.replace(' ', '').replace('-', '')
        if not clean_p.replace('+', '').isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры!")
        if not (clean_p.startswith('+7') or clean_p.startswith('8')):
            raise forms.ValidationError("Номер должен начинаться с +7 или 8!")
        return phone


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Пароль'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Повторите пароль'
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают!")
        return cleaned_data