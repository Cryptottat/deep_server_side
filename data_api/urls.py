from django.conf.urls import url
from . import views


urlpatterns = [
    url('set_data', views.SetData.as_view(), name='set_data'),
    url('get_data', views.GetData.as_view(), name='get_data'),
]