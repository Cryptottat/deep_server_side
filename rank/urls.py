from django.urls import path

from . import views

app_name = 'rank'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    path('order/<str:username>', views.order, name='order'),
    path('order_page/', views.order_page, name='order_page'),
    path('order_history/<str:username>/', views.order_history, name='order_history'),
    path('point/', views.point, name='point'),

]
