from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TaskData
import time

class SetData(APIView):
    def post(self, request):
        server_num = request.data.get('server_num', "")  #
        run = request.data.get('run', "") #
        keyword = request.data.get('keyword', "") #
        link = request.data.get('link', "")  #
        time_info = str(int(time.time()))

        task_data_info = TaskData.objects.filter(server_num=server_num).first()
        task_data_info.server_num = server_num
        task_data_info.run = run
        task_data_info.keyword = keyword
        task_data_info.link = link
        task_data_info.time_info = time_info
        task_data_info.save()
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