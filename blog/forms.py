from django import forms
from .models import Comment, Profile, Post
from django.contrib.auth.models import User 
from taggit.models import Tag



class EmailPostForm(forms.Form):
    # fields = ('name')
    title = forms.CharField(max_length=25)
    # email = forms.EmailField()
    to = forms.EmailField()
    comments =forms.CharField(required=False,
                              widget=forms.Textarea)
    
    # def __init__(self, *args, ** kwargs):
    #     super(EmailPostForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        
    def __init__(self, *args, ** kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder':'example@email.com'})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
        
        
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, ** kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder':'example@email.com'})

        
class ProfileEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'profile_picture')
        
    def __init__(self, *args, ** kwargs):
        super(ProfileEdit, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control', 'placeholder':'YYYY-MM-DD'})
        self.fields['profile_picture'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
        
class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.SelectMultiple)
    # tags = forms.
    class Meta:
        model = Post
        fields = ('title', 'slug', 'body', 'tags', 'image', 'status')      
        widgets = {'slug': forms.HiddenInput(),}
        
    def __init__(self, *args, ** kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
        self.fields['slug'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
        self.fields['body'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
        self.fields['status'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
        self.fields['tags'].widget.attrs.update({'class': 'form-control', 'placeholder':''})
