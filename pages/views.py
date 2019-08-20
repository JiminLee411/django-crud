from django.shortcuts import render

# Create your views here.
def one(request):
    return render(request, 'pages/one.html')

def two(request):
    return render(request, 'pages/two.html')