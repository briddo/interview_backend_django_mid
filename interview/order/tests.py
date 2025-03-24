from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from interview.inventory.models import InventoryLanguage, InventoryType
from interview.order.models import Inventory, Order


class BetweenStartAndEmbargoDatesTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        inventory = Inventory.objects.create(
            name="Inventory",
            language=InventoryLanguage.objects.create(name="English"),
            type=InventoryType.objects.create(name="Type"),
            metadata={},
        )
        self.order1 = Order.objects.create(
            inventory=inventory,
            start_date="2022-01-01",
            embargo_date="2022-01-31",
        )
        self.order2 = Order.objects.create(
            inventory=inventory,
            start_date="2022-02-01",
            embargo_date="2022-02-28",
        )

        self.url_all = reverse(
            "order-list-between-start-and-embargo-dates",
            kwargs={"start_date": "2022-01-01", "embargo_date": "2022-02-28"},
        )
        self.url_one = reverse(
            "order-list-between-start-and-embargo-dates",
            kwargs={"start_date": "2022-01-01", "embargo_date": "2022-01-31"},
        )

    def test_between_start_and_embargo_dates(self):
        response = self.client.get(self.url_all)
        self.assertEqual(len(response.data), 2)
        response = self.client.get(self.url_one)
        self.assertEqual(len(response.data), 1)
