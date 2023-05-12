from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement  # 유저정보 불러와야됨
from common.models import User
from .models import Order,PricePerHour
from .forms import OrderForm
from django.utils import timezone

# def point(request):
#     return render(request, 'rank/point_page.html')
#     return redirect('rank:index')
def order_history(request,username):
    order_list = Order.objects.filter(username=username)
    return render(request, 'rank/order_history.html', {'order_list':order_list, 'username':username})
def order_page(request):
    Price_Per_Hour = PricePerHour.objects.all().first()
    if Price_Per_Hour is None:
        return HttpResponse('시간당 포인트가 설정되지 않았습니다. 관리자에게 문의하십시오.')
    price_per_hour = Price_Per_Hour.price_per_hour
    return render(request, 'rank/order_page.html',{"price_per_hour":price_per_hour})
def order(request, username):
    print('ordddddddddddddddddddddder')
    if request.method == "POST":
        print('ordddddddddddddddddddddder2222222222222222222222')
        form = OrderForm(request.POST)
        print('ordddddddddddddddddddddder333333333333333333333333333333333333333333')
        print(form.data.get('target_time'))
        if form.is_valid():
            print(2)
            target_time = form.cleaned_data.get('target_time')
            keyword = form.cleaned_data.get('keyword')
            target_url = form.cleaned_data.get('target_url')
            charge = form.cleaned_data.get('charge')
            price_per_hour = PricePerHour.objects.all().first().price_per_hour
            need_point = int(charge)*int(price_per_hour)
            print(3)
            user = User.objects.filter(username=username).first()
            if user.point < int(need_point):
                form.add_error('charge', '포인트가 부족합니다.')
                return render(request, 'rank/order_page.html', {'form': form})

            user.point = user.point - need_point
            user.save()
            print(4)
            Order.objects.create(
                username=username,
                target_time=target_time,
                keyword=keyword,
                target_url=target_url,
                charge=charge,
                order_time=timezone.now()
            )
            print(5)
            # order_list = Order.objects.filter(username=username)
            print('username:',username)
            return redirect('rank:order_history',  username)
            # return render(request, 'rank/order_history.html', {'order_list': order_list})
    return render(request, 'rank/order_page.html', {'form': form})


def announcement_detail(request, announcement_id):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    context = {'announcement': announcement}
    return render(request, 'rank/announcement_detail.html', context)


def index(request):
    announcement_list = Announcement.objects.order_by('-create_date')
    context = {'announcement_list': announcement_list}
    return render(request, 'rank/announcement_list.html', context)
    # question_list = Question.objects.order_by('-create_date')
    # context = {'question_list': question_list}
    # return render(request, 'rank/index.html')
    # 파이보 인덱스 페이지 참고해 작업할것.


"""
# 인덱스 페이지 작업할때 해당 로그인 되어있고, 안되어있고 따라서 로그인 페이지로 리다이렉트 시킬것인지 페이지 표시 할 것인지 체크

(... 생략 ...)
<li class="nav-item">
    {% if user.is_authenticated %}
    <a class="nav-link" href="{% url 'common:logout' %}">{{ user.username }} (로그아웃)</a>
    {% else %}
    <a class="nav-link" href="{% url 'common:login' %}">로그인</a>
    {% endif %}
</li>
(... 생략 ...)
"""
