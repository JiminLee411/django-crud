import hashlib
from django import template

register = template.Library()

@register.filter
def makehash(user):
    email = user.email
    social_user = user.socialaccount_set.all().first() # 프로필이 없으면 오류 발생하므로 [0]이 아닌 .first()로 저장
    if social_user:
        return social_user.extra_data.get('properties').get('profile_image')

    return 'https://www.gravatar.com/avatar/' + hashlib.md5(email.strip().lower().encode('utf-8')).hexdigest() + "?d=mp"
