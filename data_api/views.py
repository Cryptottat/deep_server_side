from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TaskData, ProxyInfo, GoogleAccountInfo
import json
import time


class SetData(APIView):
    def post(self, request):
        server_num = request.data.get('server_num', "")  #
        run = request.data.get('run', "")  #
        keyword = request.data.get('keyword', "")  #
        link = request.data.get('link', "")  #
        time_info = str(int(time.time()))

        task_data_info = TaskData.objects.filter(server_num=server_num).first()
        if task_data_info is not None:
            task_data_info.server_num = server_num
            task_data_info.run = run
            task_data_info.keyword = keyword
            task_data_info.link = link
            task_data_info.time_info = time_info
            task_data_info.save()
        else:
            TaskData.objects.create(
                server_num=server_num,
                run=run,
                keyword=keyword,
                link=link,
                time_info=time_info
            )

        all_task_data = TaskData.objects.all()
        task_data_list = []
        for task_data in all_task_data:
            data = dict(
                server_num=task_data.server_num,
                run=task_data.run,
                keyword=task_data.keyword,
                link=task_data.link,
                time_info=task_data.time_info,
            )
            task_data_list.append(data)

        return Response(data=task_data_list)


class GetData(APIView):
    def post(self, request):
        all_task_data = TaskData.objects.all()
        task_data_list = []
        for task_data in all_task_data:
            data = dict(
                server_num=task_data.server_num,
                run=task_data.run,
                keyword=task_data.keyword,
                link=task_data.link,
                time_info=task_data.time_info,
            )
            task_data_list.append(data)

        return Response(data=task_data_list)


class SetProxy(APIView):
    """
    account = models.CharField(max_length=20, null=False, default=False)
    proxy = models.CharField(max_length=50, null=False, default=False)
    usable = models.BooleanField(default=True)
    success_count = models.IntegerField(null=False, default=0)
    fail_count = models.IntegerField(max_length=5, null=False, default=0)
    using_request_time = models.CharField(max_length=100, null=False, default=0)
    """

    def post(self, request):
        account = request.data.get('account', "")  #
        proxy_list = request.data.get('proxy_list',[])
        for proxy in proxy_list:
            if not ProxyInfo.objects.filter(proxy=proxy).exists():
                ProxyInfo.objects.create(
                    account=account,
                    proxy=proxy,
                )
        data = list(ProxyInfo.objects.values().all())
        return Response(data=data)


class GetProxy(APIView):
    """
    account = models.CharField(max_length=20, null=False, default=False)
    proxy = models.CharField(max_length=50, null=False, default=False)
    usable = models.BooleanField(default=True)
    success_count = models.IntegerField(null=False, default=0)
    fail_count = models.IntegerField(max_length=5, null=False, default=0)
    using_request_time = models.CharField(max_length=100, null=False, default=0)
    """

    def post(self, request):
        account = request.data.get('account', "")
        min_success = int(request.data.get('min_success', 0)) - 1
        max_fail = int(request.data.get('max_fail', 9999)) + 1
        make_unusable = request.data.get('make_unusable', False)
        proxy_info = ProxyInfo.objects.filter(
            account=account,
            success_count__gt=min_success,
            fail_count__lt=max_fail,
            usable=True
        ).first()
        print(proxy_info)
        if proxy_info is None:
            return Response(data=None)
        last_using_request_time = proxy_info.using_request_time

        proxy_info.usable = not make_unusable
        if make_unusable:
            proxy_info.using_request_time = str(int(time.time()))
        proxy_info.save()

        data = dict(
            account=proxy_info.account,
            proxy=proxy_info.proxy,
            usable=proxy_info.usable,
            success_count=proxy_info.success_count,
            fail_count=proxy_info.fail_count,
            using_request_time=last_using_request_time,
        )
        return Response(data=data)


class ChangeProxy(APIView):
    """
    account = models.CharField(max_length=20, null=False, default=False)
    proxy = models.CharField(max_length=50, null=False, default=False)
    usable = models.BooleanField(default=True)
    success_count = models.IntegerField(null=False, default=0)
    fail_count = models.IntegerField(null=False, default=0)
    using_request_time = models.CharField(max_length=100, null=True, default=0)
    """
    def post(self, request):
        proxy = request.data.get('proxy', '')
        change_field = request.data.get('change_field', '')
        change_type = request.data.get('change_type', "")
        change_value = request.data.get('change_value', False)
        proxy_info = ProxyInfo.objects.filter(
            proxy=proxy,
        ).first()
        if proxy_info is None:
            return Response(data=None)
        change_target = None
        if change_field == 'usable':
            if change_type == 'replace' or change_type == 'edit':
                proxy_info.usable = change_value
        elif change_field == 'account':
            if change_type == 'replace' or change_type == 'edit':
                proxy_info.account = change_value
        elif change_field == 'success_count':
            if change_type == 'add':
                proxy_info.success_count += change_value
            elif change_type == 'subtract':
                proxy_info.success_count -= change_value
        elif change_field == 'fail_count':
            if change_type == 'add':
                proxy_info.fail_count += change_value
            elif change_type == 'subtract':
                proxy_info.fail_count -= change_value
        change_target.save()

        data = ProxyInfo.objects.filter(
            proxy=proxy,
        ).values().first()
        return Response(data=data)



class SetGoogleAccount(APIView):
    """
    id = models.CharField(max_length=100, null=False, default=False)
    password = models.CharField(max_length=100, null=False, default=False)
    email = models.CharField(max_length=100, null=False, default=False)
    usable = models.BooleanField(default=True)
    matched_proxy = models.CharField(max_length=50, null=True, default=None)
    success_count = models.IntegerField(null=False, default=0)
    fail_count = models.IntegerField(null=False, default=0)
    using_request_time = models.CharField(max_length=100, null=True, default=0)
    """

    def post(self, request):
        account_list = request.data.get('account_list', [])
        for account in account_list:
            if not GoogleAccountInfo.objects.filter(google_id=account['id'], google_password=account['password'], email=account['email']).exists():
                GoogleAccountInfo.objects.create(
                    google_id=account['id'],
                    google_password=account['password'],
                    email=account['email']
                )
        list_for_return = []
        all_google_account_info = list(GoogleAccountInfo.objects.all())
        for google_account_info in all_google_account_info:
            data = dict(
                id=google_account_info.google_id,
                password=google_account_info.google_password,
                email=google_account_info.email,
                usable=google_account_info.usable,
                matched_proxy=google_account_info.matched_proxy,
                success_count=google_account_info.success_count,
                fail_count=google_account_info.fail_count,
                using_request_time=google_account_info.using_request_time
            )
            list_for_return.append(data)
        return Response(data=list_for_return)


class GetGoogleAccount(APIView):
    """
    id = models.CharField(max_length=100, null=False, default=False)
    password = models.CharField(max_length=100, null=False, default=False)
    email = models.CharField(max_length=100, null=False, default=False)
    usable = models.BooleanField(default=True)
    matched_proxy = models.CharField(max_length=50, null=True, default=None)
    success_count = models.IntegerField(null=False, default=0)
    fail_count = models.IntegerField(null=False, default=0)
    using_request_time = models.CharField(max_length=100, null=True, default=0)
    """

    def post(self, request):
        min_success = int(request.data.get('min_success', 0)) - 1
        max_fail = int(request.data.get('max_fail', 9999)) + 1
        proxy = request.data.get('proxy', "")
        make_unusable = request.data.get('make_unusable', False)
        google_account_info_filtered_by_matched_proxy = None
        if not proxy == "":
            google_account_info_filtered_by_matched_proxy = GoogleAccountInfo.objects.filter(
                matched_proxy=proxy,
                success_count__gt=min_success,
                fail_count__lt=max_fail,
                usable=True
            ).first()
        if google_account_info_filtered_by_matched_proxy is not None:
            last_using_request_time = google_account_info_filtered_by_matched_proxy.using_request_time
            google_account_info_filtered_by_matched_proxy.usable = not make_unusable
            if make_unusable:
                google_account_info_filtered_by_matched_proxy.using_request_time = int(time.time())
            google_account_info_filtered_by_matched_proxy.save()
            google_account_info = google_account_info_filtered_by_matched_proxy
            data = dict(
                id=google_account_info.google_id,
                password=google_account_info.google_password,
                email=google_account_info.email,
                usable=google_account_info.usable,
                matched_proxy=google_account_info.matched_proxy,
                success_count=google_account_info.success_count,
                fail_count=google_account_info.fail_count,
                using_request_time=last_using_request_time,
            )
            return Response(data=data)

        google_account_info = GoogleAccountInfo.objects.filter(
            success_count__gt=min_success,
            fail_count__lt=max_fail,
            usable=True
        ).first()
        if google_account_info is None:
            return Response(data=None)
        last_using_request_time = google_account_info.using_request_time
        google_account_info.usable = not make_unusable
        if make_unusable:
            google_account_info.using_request_time = int(time.time())
        google_account_info.save()
        data = dict(
            id=google_account_info.google_id,
            password=google_account_info.google_password,
            email=google_account_info.email,
            usable=google_account_info.usable,
            matched_proxy=google_account_info.matched_proxy,
            success_count=google_account_info.success_count,
            fail_count=google_account_info.fail_count,
            using_request_time=last_using_request_time,
        )
        return Response(data=data)



class ChangeGoogleAccount(APIView):
    """
    oogle_id = models.CharField(max_length=100, null=False, default=False)
    google_password = models.CharField(max_length=100, null=False, default=False)
    email = models.CharField(max_length=100, null=False, default=False)
    usable = models.BooleanField(default=True)
    matched_proxy = models.CharField(max_length=50, null=True, default=None)
    success_count = models.IntegerField(null=False, default=0)
    fail_count = models.IntegerField(null=False, default=0)
    using_request_time = models.CharField(max_length=100, null=True, default=0)
    """
    def post(self, request):
        google_id = request.data.get('id', '')
        change_field = request.data.get('change_field', '')
        change_type = request.data.get('change_type', "")
        change_value = request.data.get('change_value', False)
        print(google_id)
        google_account_info = GoogleAccountInfo.objects.filter(
            google_id=google_id,
        ).first()
        if google_account_info is None:
            return Response(data=None)

        if change_field == 'usable':
            if change_type == 'replace' or change_type == 'edit':
                google_account_info.usable = change_value
        elif change_field == 'matched_proxy':
            if change_type == 'replace' or change_type == 'edit':
                google_account_info.matched_proxy = change_value
        elif change_field == 'success_count':
            if change_type == 'add':
                google_account_info.success_count += change_value
            elif change_type == 'replace' or change_type == 'edit':
                google_account_info.success_count = change_value
        elif change_field == 'fail_count':
            if change_type == 'add':
                google_account_info.fail_count += change_value
            elif change_type == 'replace' or change_type == 'edit':
                google_account_info.fail_count = change_value
        google_account_info.save()

        data = GoogleAccountInfo.objects.filter(
            google_id=google_id,
        ).values().first()
        return Response(data=data)

class MakeProxyAllUsable(APIView):
    def post(self, request):
        proxy_info_list = ProxyInfo.objects.all()
        for proxy_info in proxy_info_list:
            proxy_info.usable = True
            proxy_info.save()
        return Response(data=None)

class MakeGoogleAccountAllUsable(APIView):
    def post(self, request):
        google_account_info_list = GoogleAccountInfo.objects.all()
        for google_account_info in google_account_info_list:
            google_account_info.usable = True
            google_account_info.save()
        return Response(data=None)
