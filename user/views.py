from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.

@login_required
def profile(request):
    return render(request, 'user/profile.html')

@login_required
def profile_update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
        username = u_form.cleaned_data['username']
        messages.success(request, f"Account updated for {username} successfully!!! ")
        return redirect('user-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile )
    
    return render(request, 'user/profile_update.html',{'u_form' : u_form,'p_form' : p_form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f"Account created for {username} successfully!!! ")
            return redirect('user-login')
    else:
        form = UserRegisterForm()

    return render(request, 'user/register.html', {'form' : form})

def logout_user(request):
    logout(request)
    return redirect('password_reset_done')