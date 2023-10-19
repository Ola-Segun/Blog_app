from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from . forms import CustomUserCreationForm
from blog.models import Profile
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def droppage(request):
    return render(request, 'drop.html')

def loginUser(request):
    page = 'login'
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog:homepage')
        
        else:
            messages.error(request, "You don't have an account.")
            
    context = {'page': page,}
    return render(request, 'login_register.html', context)


def registerUser(request):
    page = 'register'
    
    form = CustomUserCreationForm()
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            username = request.POST['username']
            UserError = f'The username is already in use.'
            return render(request,'login_register.html', {'UserError':UserError, 'form':form})
        
        elif form.is_valid:
            password1=request.POST['password1']
            password2=request.POST['password2']
            
            if password2 != password1:
                form = CustomUserCreationForm(request.POST)

                password_err = "Password didn't match"
                context_pass = {'password_err': password_err, 'form': form}
                return render(request, 'login_register.html', context_pass)
            
            user = form.save(commit=False)
            user.save()
            
            
            Profile.objects.create(user=user)
            user = authenticate(request, username=user.username, password=request.POST['password1'])
            print('User: ', user)   
            if user is not None:
                login(request, user)
            return redirect('blog:homepage')

    context = {'page': page, 
               'form':form,}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('droppage')


# @login_required
# def profileEdit(request):
#     profile = Profile.objects.get(user=request.user)
#     if request.method == 'POST':
#         user_form = UserEditForm(instance=request.user,
#                             data=request.POST)
#         profile_form = ProfileEdit(instance=request.user.profile,
#                                    data=request.POST,
#                                    files=request.FILES)
#         if user_form.is_valid and profile_form.is_valid:
#             user_form.save()
#             # print(request.POST['date_of_birth'])
#             profile_form.save()
#             messages.success(request, 'Profile updated successfully')
#         else:
#             messages.error(request, 'Error updating your profile')

#     else:
#         user_form = UserEditForm(instance=request.user)
#         profile_form = ProfileEdit(instance=request.user.profile)
    
#     context = {'user_form':user_form, 'profile_form':profile_form, 'profile':profile }

#     return render(request, 'profile.html', context)