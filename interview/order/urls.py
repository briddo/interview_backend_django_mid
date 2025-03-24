
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('', OrderListCreateView.as_view(), name='order-list'),
    path('between-start-and-embargo-dates/<str:start_date>/<str:embargo_date>/', OrderListCreateView.as_view(), name='order-list-between-start-and-embargo-dates'),

]
