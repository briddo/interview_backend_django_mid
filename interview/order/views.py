from rest_framework import generics
from django.utils.dateparse import parse_date

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        start = self.kwargs.get("start_date")
        end = self.kwargs.get("embargo_date")

        if start and end:
            try:
                start_dt = parse_date(start)
                end_dt = parse_date(end)
                queryset = queryset.filter(
                    start_date__gte=start_dt,
                    embargo_date__lte=end_dt
                )
            except (TypeError, ValueError):
                pass

        return queryset
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer
