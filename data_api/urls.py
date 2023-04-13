from django.conf.urls import url
from . import views


urlpatterns = [
    url('set_data', views.SetData.as_view(), name='set_data'),
    url('get_data', views.GetData.as_view(), name='get_data'),
    url('set_proxy', views.SetProxy.as_view(), name='set_proxy'),
    url('get_proxy', views.GetProxy.as_view(), name='get_proxy'),
    url('set_google_account', views.SetGoogleAccount.as_view(), name='set_google_account'),
    url('get_google_account', views.GetGoogleAccount.as_view(), name='get_google_account'),
]