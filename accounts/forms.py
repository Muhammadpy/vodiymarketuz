from dataclasses import field
from pyexpat import model
from django import forms
from  .models import Account, UserProfile

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

    def clean(self):
        clean_data=super(RegistrationForm, self).clean()
        password=clean_data.get('password')
        confirm_password=clean_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError('password does not match!')
        


  

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter first Name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter phone_number '
        self.fields['email'].widget.attrs['placeholder']='Enter your email'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


    
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

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


