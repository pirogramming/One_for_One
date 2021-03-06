from random import randint

from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from django.core.serializers import json
from django.db.models.functions import datetime
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import random
from django.views import View

# from core.models import Category
from .models import Profile, Univ, AuthSms

from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.

def randstr(length):
    rstr = "0123456789abcdefghijklnmopqrstuvwxyzABCDEFGHIJKLNMOPQRSTUVWXYZ"
    rstr_len = len(rstr) - 1
    result = ""
    for i in range(length):
        result += rstr[random.randint(0, rstr_len)]
    return result


def home(request):
    return render(request, 'home.html')


def goto_signup(request):
    if request.method == 'POST':
        univ = request.POST['univ']
        return redirect(reverse('account:signup', args=[univ]))
    else:
        univs = Univ.objects.all()
        data = {
            'univs': univs
        }
        return render(request, 'choice_univ.html', data)


def signup(request, pk):
    univs = Univ.objects.all()
    univ = Univ.objects.get(pk=pk)
    if request.method == "POST":

        if request.POST["password1"] == request.POST["password2"]:
            email = request.POST['email_id'] + '@' + request.POST['email_domain']
            user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password1"],
                last_name=randstr(50),
                email=request.POST["email_id"]
            )
            user.is_active = False
            user.save()
            nickname = request.POST["nickname"]
            phone_number = request.POST['phone_number']
            profile = Profile(
                user=user,
                nickname=nickname,
                univ=univ,
                phone_number=phone_number,
            )
            profile.save()
            auth.login(request, user)
            mail = EmailMessage('<저기요> 회원가입 인증 메일입니다.',
                                'url을 클릭하면 인증됩니다.' + 'http://52.79.67.35/account/active/' + user.last_name,
                                to=[email])
            mail.send()
            return redirect('core:main')
        else:
            return render(request, 'signup.html', {'message': '비밀번호가 일치하지 않습니다.', 'pk': request.GET.pk})
    else:
        UNIV_DOMAIN_MAPPING = {
            '가천대학교 글로벌캠퍼스': 'gc.gachon.ac.kr',
            '경기대학교 수원캠퍼스': 'kyonggi.ac.kr',
            '경희대학교 국제캠퍼스': 'khu.ac.kr',
            '성신여자대학교': 'sungshin.ac.kr',
            '세종대학교': 'sju.ac.kr',
            '숙명여자대학교': 'sookmyung.ac.kr',
            '중앙대학교': 'cau.ac.kr',
            '한국외국어대학교 서울캠퍼스': 'hufs.ac.kr',
            '한양대학교': 'hanyang.ac.kr',
            '서울대학교': 'snu.ac.kr',
            '성균관대학교 자연과학캠퍼스': 'g.skku.edu',
            '이화여자대학교': 'ewhain.net',
            '홍익대학교': 'mail.hongik.ac.kr',
            '고려대학교': 'korea.ac.kr',
        }

        profiles = Profile.objects.all()
        data = {
            'univs': univs,
            'univ': univ,
            'email_domain': UNIV_DOMAIN_MAPPING.get(univ.name),

            'username_list': [profile.user.username for profile in profiles],
            'nickname_list': [profile.nickname for profile in profiles],
            'phone_number_list': [profile.phone_number for profile in profiles],
            'email_id_list': [profile.user.email for profile in profiles],

            'de_username': "",
            'de_password1': "",
            'de_password2': "",
            'de_email_id': "",
            'de_nickname': "",
            'de_phone_number': "",
        }
        return render(request, 'signup.html', data)


def login(request):
    if request.user.is_authenticated:
        current_user = request.user
        profile = Profile.objects.get(user=current_user)
        data = {
            'profile': profile
        }
    else:
        univs = Univ.objects.all()
        data = {
            'univs': univs
        }
    if request.method == "POST":
        username = request.POST["id"]
        password = request.POST["password"]
        # 해당 user가 있으면 username, 없으면 None
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            profile = Profile.objects.get(user=user)
            univ = profile.univ
            auth.login(request, user)
            return redirect(reverse('core:home', args=[univ.id]))
        else:
            return render(request, 'login.html', {'error': '없는 아이디이거나 비밀번호가 일치하지 않습니다.'})
    else:
        return render(request, 'login.html', data)


def logout(request):
    auth.logout(request)
    return redirect("core:main")


def user_active(request, token):
    user = User.objects.get(last_name=token)
    user.is_active = True
    user.last_name = ''
    user.save()
    message = "이메일이 인증되었습니다."
    # univ = user.profile.univ_id
    # profile = user.profile
    return render(request, 'signup_complete.html', {'message':message})


def send_sms(request, pk):
    from account.utils import AuthSmsSendView
    assv = AuthSmsSendView()
    user_phone_number = request.POST['user_phone_number']
    assv.post(request, user_phone_number)
    return render(request, 'test3.html')


def test(request):
    return render(request, 'test3.html', {'count': 6})


def auth_check(request, pk):
    user_authsms = AuthSms.objects.get(phone_number=request.POST['user_phone_number'])
    if int(request.POST['user_auth_number']) == int(user_authsms.auth_number):
        print(request.POST['user_auth_number'])
        print(user_authsms.auth_number)
        return render(request, 'test3.html')
    else:
        return None
