from datetime import timedelta

from django.utils.timezone import now
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
        inventory2 = Inventory.objects.create(
            name="2", type=type2, language=language2, metadata={}
        )
        inventory2.created_at = now() - timedelta(days=4)
        inventory2.save()

    def test_get_items_created_after_certain_day(self):

        # since we are only testing the view, we don't need to make a real request
        request = self.factory.get("/fake/")

        # yesterday's date
        created_after = (now() - timedelta(days=1)).date()

        # get inventories created after yesterday
        view = InventoryListAfterDateView.as_view()
        response = view(request, created_after=str(created_after))

        # should return only the inventory created today
        self.assertEqual(len(response.data), 1)
