from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TaskData, ProxyInfo, GoogleAccountInfo, ThreadInfo
import json
import time


class SetData(APIView):
    def post(self, request):
        server_num = request.data.get('server_num', "")  #
        task_run = request.data.get('task_run', "")  #
        keyword = request.data.get('keyword', "")  #
        link = request.data.get('link', "")  #
        login_check = request.data.get('login_check', "")  #
        get_proxy_make_unusable = request.data.get('get_proxy_make_unusable', True)  #
        get_google_account_make_unusable = request.data.get('get_google_account_make_unusable', True)  #
        time_info = str(int(time.time()))

        task_data_info = TaskData.objects.filter(server_num=server_num).first()
        if task_data_info is not None:
            task_data_info.server_num = server_num
            task_data_info.task_run = task_run
            task_data_info.keyword = keyword
            task_data_info.link = link
            task_data_info.login_check = login_check
            task_data_info.time_info = time_info
            task_data_info.get_proxy_make_unusable = get_proxy_make_unusable
            task_data_info.get_google_account_make_unusable = get_google_account_make_unusable

            task_data_info.save()
        else:
            TaskData.objects.create(
                server_num=server_num,
                task_run=task_run,
                keyword=keyword,
                link=link,
                login_check=login_check,
                get_proxy_make_unusable=get_proxy_make_unusable,
                get_google_account_make_unusable=get_google_account_make_unusable,
                time_info=time_info
            )

        all_task_data = TaskData.objects.all()
        task_data_list = []
        for task_data in all_task_data:
            data = dict(
                server_num=task_data.server_num,
                task_run=task_data.task_run,
                keyword=task_data.keyword,
                link=task_data.link,
                login_check=task_data.login_check,
                get_proxy_make_unusable=task_data.get_proxy_make_unusable,
                get_google_account_make_unusable=task_data.get_google_account_make_unusable,
                time_info=task_data.time_info,
            )
            task_data_list.append(data)

        return Response(data=task_data_list)


class GetData(APIView):
    def post(self, request):
        print('get data')
        host_name = request.data.get('host_name', None)  #
        anydesk_id = request.data.get('anydesk_id', None)  #
        hai_ip_account = request.data.get('hai_ip_account', None)  #
        total_logged_in = request.data.get('total_logged_in', None)  #
        thread_list = request.data.get('thread_list', [])  #

        for thread in thread_list:
            if not ThreadInfo.objects.filter(host_name=host_name, anydesk_id=anydesk_id, thread_index=thread['thread_index']).exists():
                ThreadInfo.objects.create(
                    host_name=host_name,
                    anydesk_id=anydesk_id,
                    hai_ip_account=hai_ip_account,
                    total_logged_in=0,
                    thread_index=thread['thread_index'],
                    server_num=thread['server_num'],
                    proxy=thread['proxy'],
                    google_id=thread['google_id'],
                    google_password=thread['google_password'],
                    google_email=thread['google_email'],
                    user_agent=thread['user_agent'],
                    google_logged_in=thread['google_logged_in'],
                    now_state=thread['now_state'],
                    is_filter=False,
                    last_connected_timestamp = int(time.time())
                )
                continue
            thread_info = ThreadInfo.objects.filter(host_name=host_name, anydesk_id=anydesk_id, thread_index=thread['thread_index']).first()
            thread_info.server_num = thread['server_num']
            thread_info.proxy = thread['proxy']
            thread_info.google_id = thread['google_id']
            thread_info.google_password = thread['google_password']
            thread_info.google_email = thread['google_email']
            thread_info.user_agent = thread['user_agent']
            thread_info.google_logged_in = thread['google_logged_in']
            thread_info.now_state = thread['now_state']
            thread_info.save()
        thread_info_list = ThreadInfo.objects.filter(host_name=host_name, anydesk_id=anydesk_id).all()
        return_thread_info_list = []
        for thread in thread_info_list:
            data = dict(
                thread_index=thread.thread_index,
                server_num=thread.server_num,
                proxy=thread.proxy,
                google_id=thread.google_id,
                google_password=thread.google_password,
                google_email=thread.google_email,
                keyword=thread.keyword,
                is_filter=thread.is_filter,
                target_url=thread.target_url,
                enter_type=thread.enter_type,
                target_state=thread.target_state
            )
            return_thread_info_list.append(data)
        return_data = {'thread_list':return_thread_info_list}
        return Response(data=return_data)


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
        proxy_list = request.data.get('proxy_list', [])
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

        if proxy_info is None:  # 원래 주면 안되는데 데이터..ㅠ
            proxy_info = ProxyInfo.objects.filter(
                account=account,
                usable=True
            ).first()
            data = dict(
                account=proxy_info.account,
                proxy=proxy_info.proxy,
                usable=proxy_info.usable,
                success_count=proxy_info.success_count,
                fail_count=proxy_info.fail_count,
                using_request_time=int(time.time()),
            )
            return Response(data=data)

            # return Response(data=None)
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
        proxy_info.save()

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
        replace = request.data.get('replace', False)
        for account in account_list:
            if replace or GoogleAccountInfo.objects.filter(google_id=account['id']).exists() is False:
                GoogleAccountInfo.objects.create(
                    google_id=account['id'],
                    google_password=account['password'],
                    email=account['email'],
                    matched_hai_ip_account=account['matched_hai_ip_account'],
                    matched_proxy=account['matched_proxy'],
                )
        list_for_return = []
        all_google_account_info = list(GoogleAccountInfo.objects.all())
        for google_account_info in all_google_account_info:
            data = dict(
                id=google_account_info.google_id,
                password=google_account_info.google_password,
                email=google_account_info.email,
                user_agent=google_account_info.user_agent,
                usable=google_account_info.usable,
                matched_hai_ip_account=google_account_info.matched_hai_ip_account,
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
        proxy = request.data.get('proxy', None)
        make_unusable = request.data.get('make_unusable', False)
        google_account_info_filtered_by_matched_proxy = None
        if not proxy == None:
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
                user_agent=google_account_info.user_agent,
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
        if google_account_info is None:  # 원래 데이터 주면 안되는 부분
            google_account_info = GoogleAccountInfo.objects.filter(
                usable=True
            ).first()
            data = dict(
                id=google_account_info.google_id,
                password=google_account_info.google_password,
                email=google_account_info.email,
                user_agent=google_account_info.user_agent,
                usable=google_account_info.usable,
                matched_proxy=google_account_info.matched_proxy,
                success_count=google_account_info.success_count,
                fail_count=google_account_info.fail_count,
                using_request_time=int(time.time()),
            )
            return Response(data=data)
            # return Response(data=data)
        last_using_request_time = google_account_info.using_request_time
        google_account_info.usable = not make_unusable
        if make_unusable:
            google_account_info.using_request_time = int(time.time())
        google_account_info.save()
        data = dict(
            id=google_account_info.google_id,
            password=google_account_info.google_password,
            email=google_account_info.email,
            user_agent=google_account_info.user_agent,
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
        elif change_field == 'user_agent':
            if change_type == 'replace' or change_type == 'edit':
                google_account_info.user_agent = change_value
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
