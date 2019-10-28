from IPython import embed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm # UserCreationForm : 회원가입 폼,  AuthenticationForm : 인증과 관련된 form
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model # User 클래스 사용하려면 이거 불러와야해!!

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # 회원가입에 성공했으면 로그인 바로 시켜주는 코드
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # 로그인
            user = form.get_user() # 현재 valid한 User를 찾아서 준다.
            auth_login(request, user) # request에 login관련 정보가 다 들어있다. / auth_login() : 로그인시켜주는 함수
            # return redirect('articles:index')
            return redirect(request.GET.get('next') or 'articles:index') # next : 이전 요청을 받기 위해서
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user) # 비밀번호 update후 로그인 유지하는 함수
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user) # 반드시 첫번째 인자로 user
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def profile(request, account_pk):
    User = get_user_model()
    user_profile = get_object_or_404(User, pk=account_pk)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'accounts/profile.html', context)

def follow(request, account_pk):
    User = get_user_model()
    user_profile = get_object_or_404(User, pk=account_pk)
    if user_profile != request.user:
        if request.user in user_profile.followers.all():
            user_profile.followers.remove(request.user)
        else:
            user_profile.followers.add(request.user)
    return redirect('accounts:profile', account_pk)