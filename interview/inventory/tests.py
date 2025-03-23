from datetime import timedelta
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Inventory, InventoryLanguage, InventoryType
from .views import InventoryListAfterDateView


class InventoryListAfterDateViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # Create two inventories:
        # Inventory 1 created today
        type1 = InventoryType.objects.create(name="1")
        language1 = InventoryLanguage.objects.create(name="1")
        Inventory.objects.create(
            name="1", created_at=now(), type=type1, language=language1, metadata={}
        )
        # Inventory 2 created 4 days ago
        type2 = InventoryType.objects.create(name="2")
        language2 = InventoryLanguage.objects.create(name="2")
        Inventory.objects.create(
            name="2", created_at=now() - timedelta(days=4), type=type2, language=language2, metadata={}
        )

    def test_get_items_created_after_certain_day(self):
        request = self.factory.get(reverse("inventory-list-created-after-date"))
        self.view = InventoryListAfterDateView.as_view()
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
