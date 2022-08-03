from dataclasses import field
from pyexpat import model
from django import forms
from  .models import Account

from django import forms
from django.contrib.auth import forms as auth_forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter password'
    }))

    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm password'
    }))
    class Meta:
        model=Account
        fields=['first_name', 'last_name' ,'phone_number', 'email', 'password',]

  

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter first Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter phone_number '
        self.fields['email'].widget.attrs['placeholder']='Enter your email'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    def clean(self):
        clean_data=super(RegistrationForm, self).clean()
        password=clean_data.get('password')
        confirm_password=clean_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError('password does not match!')
        

    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = auth_forms.ReadOnlyPasswordHashField(label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"password/\">this form</a>.")

    class Meta:
        model = Account
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


