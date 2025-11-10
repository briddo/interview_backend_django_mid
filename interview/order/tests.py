import pytest
from datetime import date, timedelta


@pytest.fixture
def api_client():
    """Create an API client for testing."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def inventory_type(db):
    """Create an inventory type for testing."""
    from interview.inventory.models import InventoryType
    return InventoryType.objects.create(name="Test Type")


@pytest.fixture
def inventory_language(db):
    """Create an inventory language for testing."""
    from interview.inventory.models import InventoryLanguage
    return InventoryLanguage.objects.create(name="Test Language")


@pytest.fixture
def inventory(db, inventory_type, inventory_language):
    """Create an inventory item for testing."""
    from interview.inventory.models import Inventory
    return Inventory.objects.create(
        name="Test Inventory",
        type=inventory_type,
        language=inventory_language,
        metadata={"key": "value"}
    )


@pytest.fixture
def active_order(db, inventory):
    """Create an active order for testing."""
    from interview.order.models import Order
    return Order.objects.create(
        inventory=inventory,
        start_date=date.today(),
        embargo_date=date.today() + timedelta(days=30),
        is_active=True
    )


@pytest.mark.django_db
class TestDeactivateOrderView:
    """Test cases for the view that deactivates an order."""
    
    def test_deactivate_order_sets_is_active_to_false(
        self, api_client, active_order
    ):
        """Test that the view sets is_active to False on the order."""
        from django.urls import reverse
        from rest_framework import status
        
        url = reverse("order-deactivate", kwargs={"id": active_order.id})
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_200_OK
        active_order.refresh_from_db()
        assert active_order.is_active is False
    
    def test_deactivate_order_returns_404_for_nonexistent_order(
        self, api_client
    ):
        """Test that the view returns 404 for a non-existent order."""
        from django.urls import reverse
        from rest_framework import status
        
        url = reverse("order-deactivate", kwargs={"id": 99999})
        response = api_client.post(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

