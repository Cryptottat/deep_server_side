from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,HttpResponse
from common.forms import UserForm

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from common.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text

from django.contrib.auth.models import User
from django.contrib import auth

from .models import User

def activate(request, uid64, token):
    # 되는 버전
    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth.login(request, user)
        return redirect('rank:index')
    else:
        return HttpResponse('비정상적인 접근입니다.')

def signup(request):
    # 되는 버전
    # if request.method == "POST":
    #     if request.POST["password1"] == request.POST["password2"]:
    #         user = User.objects.create_user(
    #             username=request.POST["username"],
    #             password=request.POST["password1"],
    #             email=request.POST["email"],
    #         )
    #         user.is_active = False
    #         user.save()
    #         # nickname = request.POST["nickname"]
    #         # profile = Profile(user=user, nickname=nickname)
    #         # profile.save()
    #         current_site = get_current_site(request)
    #         # localhost:8000
    #         message = render_to_string('common/user_activate_email.html', {
    #             'user': user,
    #             'domain': current_site.domain,
    #             'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
    #             'token': account_activation_token.make_token(user),
    #         })
    #         mail_subject = "[SOT] 회원가입 인증 메일입니다."
    #         user_email = request.POST["email"]
    #         email = EmailMessage(mail_subject, message, to=[user_email])
    #         email.send()
    #         return HttpResponse(
    #             '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
    #             'justify-content: center; align-items: center;">'
    #             '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
    #             '</div>'
    #         )
    #         return redirect('rank:index')
    #     return render(request, 'common/signup.html')
    if request.method == "POST":
        form = UserForm(request.POST)


        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user = form.save()
            user.is_active = False
            user.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # user = authenticate(username=username, password=raw_password)  # 사용자 인증
            # user.is_active = False
            # user.save()
            current_site = get_current_site(request)
            # localhost:8000
            message = render_to_string('common/user_activate_email.html', {
                'user': username,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(force_bytes(user.pk))).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = "[상단작업.com] 회원가입 인증 메일입니다."

            email = EmailMessage(mail_subject, message, to=[user_email])
            email.send()
            return HttpResponse(
                '<div style="font-size: 40px; width: 100%; height:100%; display:flex; text-align:center; '
                'justify-content: center; align-items: center;">'
                '입력하신 이메일<span>로 인증 링크가 전송되었습니다.</span>'
                '</div>'
            )
            return redirect('rank:index')



            # login(request, user)  # 로그인
            # return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})