from django.forms import ModelForm
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django import forms
# from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder':'Enter username',})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder':'Password',})
        self.fields['password2'].widget.attrs.update({'class': 'form-control',  'placeholder':'Confirm password',})
        
        
# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')

#     def __init__(self, *args, ** kwargs):
#         super(UserEditForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
#         self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
#         self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder':'example@email.com'})

        
# class ProfileEdit(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('date_of_birth', 'profile_picture')
        
#     def __init__(self, *args, ** kwargs):
#         super(ProfileEdit, self).__init__(*args, **kwargs)
#         self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control', 'placeholder':'YYYY-MM-DD'})
#         self.fields['profile_picture'].widget.attrs.update({'class': 'form-control', 'placeholder':''})