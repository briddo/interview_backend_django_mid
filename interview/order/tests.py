from rest_framework.test import APITestCase, APIRequestFactory
from django.utils.timezone import now, timedelta

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from .models import Order
from .views import DeactivateOrderView


class DeactivateOrderViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        inventory = Inventory.objects.create(
            name="Inventory",
            language=InventoryLanguage.objects.create(name="English"),
            type=InventoryType.objects.create(name="Type"),
            metadata={},
        )
        self.order = Order.objects.create(
            is_active=True,
            inventory=inventory,
            start_date=now(),
            embargo_date=now() + timedelta(days=1),
        )

    def test_deactivate_order(self):
        # since we are only testing the view, we don't need to make a real request
        request = self.factory.patch(
            "/fake/",
            {"is_active": False},
            format="json",
        )
        view = DeactivateOrderView.as_view()
        response = view(request, pk=self.order.pk).render()
        self.assertEqual(response.data["is_active"], False)
