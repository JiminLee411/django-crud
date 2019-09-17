from django import forms
from .models import Article
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article # Article 쓰려면 import해야해!!!
        fields = '__all__'
        # fields = ('title', )
        # exclude = ('title', )
        # widgets = {
        #     'title': 
        # }
    # 여기에 꾸미려면!
    # 1. 아래 주석(title부터!)을 그대로 class Meta위에 작성해!
    # 2. class Meta안에 widgets = {}설정!

# class ArticleForm(forms.Form):
#     title = forms.CharField(
#         max_length=10,
#         label='제목',
#         widget=forms.TextInput(
#             attrs={
#                 'placeholder': '제목을 입력하세요.'
#             }
#         ))
#     content = forms.CharField(
#         # label 내용 수정
#         label='내용',
#         # Django form에서 HTML 속성 지정 -> widget
#         widget=forms.Textarea(
#             attrs={
#                 'class': 'my-content',
#                 'placeholder': '내용을 입력하세요.',
#                 'row': 5,
#                 'cols': 60
#             }
#         )
#     )