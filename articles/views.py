from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST # POST여야만 동작할 수 있다
from django.contrib.auth.decorators import login_required # login해야만 동작할 수 있게 하는 데코레이터
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden #, HttpREsponse
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

from IPython import embed

# Create your views here.
def index(request):
    # ---- request 각각에 저장된 정보를 확인해보기 ---- #
    # print(request)
    # print(request.scheme)
    # print(request.method)
    # print(request.get_host())
    # --------------------------------------------- #
    articles = Article.objects.order_by('-id')
    # embed()
    context = {
        'articles' : articles
    }
    # embed() # 이 함수 만나면 멈춰서 어떤 데이터를 가지고 있는지 터미널을 통해 확인 가능하다.
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        # POST 요청 -> 검증 및 저장
        article_form = ArticleForm(request.POST, request.FILES)
        # 검증
        if article_form.is_valid():
            # 검증에 성공하면 저장
            # title = article_form.cleaned_data.get('title')
            # content = article_form.cleaned_data.get('content')
            # article = Article(title=title, content=content)
            # article.save()

            # meta 클래스 적용후, 이것만 있으면 OK!
            article = article_form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
        # else:
            # 다시 폼으로 돌아가 -> 중복돼서 제거! (아래에 context를 내보내고 else하나로 설정)
    else:
        # GET 요청 -> Form
        article_form = ArticleForm() # 지금 채워져 있어 -> 검증 실패후 채워져 있는 상태 -> 비워줘
        # GET : 비어있는 Form context
        # POST : 검증 실패시 에러메세지와 입력값 채워진 Form context
    context = {
        'article_form': article_form
    }
    return render(request, 'articles/form.html', context)

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comments = article.comment_set.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'articles/detail.html', context)

# def delete(request, article_pk):
#     article = Article.objects.get(pk=article_pk)
#     if request.method == 'POST':
#         article.delete()
#         return redirect('articles:index')
#     else:
#         return redirect('articles:detail', article.pk)

@require_POST
def delete(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if article.user == request.user:
        article.delete()
        return redirect('articles:index')
    else:
        return HttpResponseForbidden

def edit(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/edit.html', context)


def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if article.user == request.user: 
        if request.method == 'POST':
            article_form = ArticleForm(request.POST, instance=article)
            if article_form.is_valid():
                article = article_form.save()
                # article.title = article_form.cleaned_data.get('title')
                # article.content = article_form.cleaned_data.get('content')
                # article.save()
                return redirect('articles:detail', article.pk)
        else:
            article_form = ArticleForm(instance=article)

        context = {
            'article_form': article_form
        }
        return render(request, 'articles/form.html', context)
    else:
        return HttpResponseForbidden

@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        # 1. modelform에 사용자 입력값 넣고
        comment_form = CommentForm(request.POST) # 사용자가 form + modelform
        # 2. 검증하고,
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)   # 저장 잠깐만!! (DB에 쿼리 날리지 말고) comment 인스턴스 줘!
            comment.article = article # 내가 직접 조작한후
            comment.user = request.user
            comment.save() # DB에 쿼리날린다!
            messages.add_message(request, messages.SUCCESS, '댓글이 작성되었습니다!')
        else:
            messages.success(request, '댓글이 형식에 맞지 않습니다.')
            
        return redirect('articles:detail', article_pk)
    else:
        messages.success(request, '댓글 작성 권한이 없습니다. 로그인해주세요')
        return redirect('articles:detail', article_pk)
        # return HttpResponse('Unauthorized', status=401)

@require_POST
def comment_delete(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if comment.user == request.user:
        if request.method == 'POST':
            comment.delete()
            messages.add_message(request, messages.INFO, '댓글이 삭제되었습니다.')
            return redirect('articles:detail', article_pk)
    else:
        # raise PermissionDenied
        return HttpResponseForbidden # 위에거랑 이러랑 둘다 가능!
# request.user를 이용할때는 로그인이 안돼있을때는 User객체에 없기 때문에 오류 발생!!!!!! @login_required로 예외처리해야해!!!!!!!!!!        
@login_required
def like(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # 좋아요를 누른적이 있다면?
    if article in request.user.like_articles.all():
        # 좋아요 취소 로직
        request.user.like_articles.remove(article)
    # 아니면
    else:
        # 좋아요 로직
        request.user.like_articles.add(article)
    return redirect('articles:detail', article_pk)
