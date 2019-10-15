from IPython import embed
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # UserCreationForm : 회원가입 폼,  AuthenticationForm : 인증과 관련된 form
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('articles:index')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # 회원가입에 성공했으면 로그인 바로 시켜주는 코드
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
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
