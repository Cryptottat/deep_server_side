from django.shortcuts import render,redirect,HttpResponse
from coinbase_commerce.client import Client
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook

from deep_server_side import settings

# Create your views here.
# def point_page_view(request):
#     return render(request, 'payments/point_page.html')
from .models import PointValue
from .forms import CreatePaymentForm
from common.models import User
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib import auth
import logging
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token

def point_page_view(request):
    point_value = PointValue.objects.all().first()
    if point_value is None:
        return HttpResponse('포인트 가격이 설정되지 않았습니다. 관리자에게 문의하십시오.')
    return render(request, 'payments/point_page.html', {'point_value':point_value})

def create_charge(request, username):
    form = CreatePaymentForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            print(username)

            user = User.objects.get(username=username)
            uid= urlsafe_base64_encode(force_bytes(force_bytes(user.pk))).encode().decode()
            # token= account_activation_token.make_token(user)

            last_token = Token.objects.filter(user=user).first()
            if last_token is not None:
                last_token.delete()
            token = Token.objects.create(user=user)
            order_point = form.cleaned_data.get('order_point')
            point_value = PointValue.objects.all().first()
            point_price = point_value.point_price
            order_value = order_point*point_price
            client = Client(api_key=settings.COINBASE_COMMERCE_API_KEY)
            domain_url = 'http://localhost:8000/'
            product = {
                'name': f'{order_point} 포인트',
                'description': '포인트를 충전합니다.',
                'local_price': {
                    'amount': f"{order_value}",
                    'currency': 'KRW'
                },
                'pricing_type': 'fixed_price',
                'redirect_url': domain_url + 'payments/success/' + f"{uid}/{token}/{order_point}",
                'cancel_url': domain_url + 'payments/cancel/' + f"{uid}/{token}/{order_point}",
                'metadata':{
                    'username':username,
                },
            }
            charge = client.charge.create(**product)
            return redirect(charge.hosted_url)
    return render(request, 'payments/point_page.html', {'form': form})

def success_view(request, uid64, token, order_point):
    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)
    token = Token.objects.filter(user=user,key=token).first()
    if token is None:
        return HttpResponse('만료된 요청입니다.')
    if user is not None:
        token.delete()
        order_point = int(order_point)
        user.point = user.point + order_point
        user.save()
        return render(request, 'payments/success.html', {})
    else:
        return HttpResponse('비정상적인 접근입니다.')

def cancel_view(request, uid64, token, order_point):
    uid = force_text(urlsafe_base64_decode(uid64))
    user = User.objects.get(pk=uid)
    token = Token.objects.filter(user=user, key=token).first()
    if token is None:
        return HttpResponse('만료된 요청입니다.')
    if user is not None:
        token.delete()
        return render(request, 'payments/cancel.html', {})
    else:
        return HttpResponse('비정상적인 접근입니다.')


@csrf_exempt
@require_http_methods(['POST'])
def coinbase_webhook(request):
    # logger = logging.getLogger(__name__)

    request_data = request.body.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)
    webhook_secret = settings.COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET

    try:
        event = Webhook.construct_event(request_data, request_sig, webhook_secret)

        # List of all Coinbase webhook events:
        # https://commerce.coinbase.com/docs/api/#webhooks

        if event['type'] == 'charge:confirmed':
            # logger.info('Payment confirmed.')
            customer_id = event['data']['metadata']['customer_id']  # new
            customer_username = event['data']['metadata']['customer_username']  # new
            # TODO: run some custom code here
            # you can also use 'customer_id' or 'customer_username'
            # to fetch an actual Django user

    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)

    # logger.info(f'Received event: id={event.id}, type={event.type}')
    return HttpResponse('ok', status=200)