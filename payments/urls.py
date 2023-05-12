from django.urls import path

from . import views

app_name = 'payments'
urlpatterns = [
    # path('', views.index, name='index'),
    # path('<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    # path('order/<str:username>', views.order, name='order'),
    # path('order_page/', views.order_page, name='order_page'),
    # path('order_history/<str:username>/', views.order_history, name='order_history'),
    path('point/', views.point_page_view, name='point'),
    path('create/<str:username>/',views.create_charge, name='create'),
    path('success/<slug:uid64>/<slug:token>/<str:order_point>/', views.success_view, name='payments-success'),  # new
    path('cancel/<slug:uid64>/<slug:token>/<str:order_point>/', views.cancel_view, name='payments-cancel'),  # new
    # path('webhook/', views.coinbase_webhook),
    # path('', views.home_view, name='payments-home'),
]
