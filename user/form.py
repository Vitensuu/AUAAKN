from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from django.contrib.auth import get_user_model, authenticate
import re
class RegistrationForm(UserCreationForm):
        password1 = forms.CharField(widget=forms.PasswordInput)
        password2 = forms.CharField(widget=forms.PasswordInput)
         
        class Meta:
                model = User
                fields = ['first_name', 'last_name', 'email', 'phone']
        def save(self, commit=False):
                user = super().save(commit=False)
                user.username = f"{self.cleaned_data['first_name']}{self.cleaned_data['email']}"
                if commit:
                    user.save()
                return user
        
        def clean_password2(self):
               pass1 = self.cleaned_data.get('password1')
               pass2 = self.cleaned_data.get('password2')
               if pass1 and pass2 and pass1 != pass2:
                    raise forms.ValidationError('Passwords do not match')
               if not re.search(r'[A-Z]', pass1):
                    raise forms.ValidationError('Password must contain at least one uppercase letter.')
               if not re.search(r'[a-z]', pass1):
                    raise forms.ValidationError('Password must contain at least one lowercase letter.')
               if not re.search(r'\d', pass1):
                    raise forms.ValidationError('Password must contain at least one digit.')
               if len(pass1) < 8:
                    raise forms.ValidationError('Password must be at least 8 characters long.')
               return pass2
        
        def clean_first_name(self):
          return self.cleaned_data['first_name']

        def clean_last_name(self):
          return self.cleaned_data['last_name']

        def __init__(self, *args, **kwargs):
              super(RegistrationForm, self).__init__(*args, **kwargs)
              for field in self.fields.values():
                    field.widget.attrs.update({'class': 'input-style'})
              self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
              self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
              self.fields['email'].widget.attrs['placeholder'] = 'Email'
              self.fields['phone'].widget.attrs['placeholder'] = 'Phone number'
              self.fields['password1'].widget.attrs['placeholder'] = 'Password'
              self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

              self.fields['password1'].widget.attrs['id'] = 'password-input'
              self.fields['password2'].widget.attrs['id'] = 'password-input'
              


class UserLoginForm(forms.Form):
      email = forms.EmailField(label = 'Email', required=True, max_length=254)
      password = forms.CharField(label='Password', widget=forms.PasswordInput)

      def clean(self):
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if not user:
                  raise forms.ValidationError('Incorrect email address or password')
            self.user = user
            return self.cleaned_data
      def __init__(self, *args, **kwargs):
            super(UserLoginForm, self).__init__(*args, **kwargs)
            self.fields['email'].widget.attrs['placeholder'] = 'Email'
            self.fields['password'].widget.attrs['placeholder'] = 'Password'

            self.fields['password'].widget.attrs['id'] = 'password-input'


