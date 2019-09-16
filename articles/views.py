from django.shortcuts import render, redirect
# from IPython import embed

from .models import Article, Comment
from django.views.decorators.http import require_POST # POST여야만 동작할 수 있다

# Create your views here.
def index(request):
    # ---- request 각각에 저장된 정보를 확인해보기 ---- #
    # print(request)
    # print(request.scheme)
    # print(request.method)
    # print(request.get_host())
    # --------------------------------------------- #
    articles = Article.objects.order_by('-id')
    context = {
        'articles' : articles
    }
    # embed() # 이 함수 만나면 멈춰서 어떤 데이터를 가지고 있는지 터미널을 통해 확인 가능하다.
    return render(request, 'articles/index.html', context)

# def new(request):
#     return render(request, 'articles/new.html')

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article(title=title, content=content)
        article.save()
        # embed()
        return redirect('articles:detail', article.pk)
    else:
        return render(request, 'articles/new.html')

def detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    comments = article.comment_set.all()
    context = {
        'article': article,
        'comments': comments,
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
    article.delete()
    return redirect('articles:index')

def edit(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    context = {
        'article': article
    }
    return render(request, 'articles/edit.html', context)

def update(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article.title = title
        article.content = content
        article.save()
        return redirect('articles:detail', article.pk)
    else:
        context = {
            'article': article
        }
        return render(request, 'articles/edit.html', context)

def comment_create(request, article_pk):
    if request.method == 'POST':
        article = Article.objects.get(pk=article_pk)
        content = request.POST.get('content')
        comment = Comment()
        comment.content = content
        comment.article_id = article_pk
        comment.save()
        return redirect('articles:detail', article.pk)

    else:
        return redirect('articles:detail', article.pk)

