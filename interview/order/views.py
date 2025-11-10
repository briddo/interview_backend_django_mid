from datetime import datetime
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrderDateRangeView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request):
        start_date = request.query_params.get("start_date")
        embargo_date = request.query_params.get("embargo_date")
        
        if not start_date or not embargo_date:
            return Response(
                {
                    "start_date": "This field is required." if not start_date else None,
                    "embargo_date": "This field is required." if not embargo_date else None,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_date_parsed = datetime.strptime(start_date, "%Y-%m-%d").date()
            embargo_date_parsed = datetime.strptime(embargo_date, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Filter orders where start_date is between the query start_date and embargo_date
        queryset = self.queryset.filter(
            start_date__gte=start_date_parsed,
            start_date__lte=embargo_date_parsed
        )
        serializer = self.serializer_class(queryset, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
