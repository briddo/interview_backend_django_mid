from django.urls import path
from interview.order.views import (
    OrderDateRangeView,
    OrderListCreateView,
    OrderTagListCreateView,
)


urlpatterns = [
    path("date-range/", OrderDateRangeView.as_view(), name="order-date-range"),
    path("tags/", OrderTagListCreateView.as_view(), name="order-detail"),
    path("", OrderListCreateView.as_view(), name="order-list"),
]
