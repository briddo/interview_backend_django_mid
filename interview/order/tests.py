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
def orders_with_different_dates(db, inventory):
    """Create orders with different start and embargo dates."""
    from interview.order.models import Order
    
    base_date = date.today()
    
    # Order 1: starts before range, ends within range
    order1 = Order.objects.create(
        inventory=inventory,
        start_date=base_date - timedelta(days=10),
        embargo_date=base_date + timedelta(days=5),
        is_active=True
    )
    
    # Order 2: starts within range, ends within range
    order2 = Order.objects.create(
        inventory=inventory,
        start_date=base_date + timedelta(days=2),
        embargo_date=base_date + timedelta(days=8),
        is_active=True
    )
    
    # Order 3: starts within range, ends after range
    order3 = Order.objects.create(
        inventory=inventory,
        start_date=base_date + timedelta(days=3),
        embargo_date=base_date + timedelta(days=15),
        is_active=True
    )
    
    # Order 4: starts after range, ends after range
    order4 = Order.objects.create(
        inventory=inventory,
        start_date=base_date + timedelta(days=12),
        embargo_date=base_date + timedelta(days=20),
        is_active=True
    )
    
    return {
        "base_date": base_date,
        "orders": [order1, order2, order3, order4]
    }


@pytest.mark.django_db
class TestOrderDateRangeView:
    """Test cases for the view that lists orders between start and embargo dates."""
    
    def test_list_orders_between_dates_returns_filtered_orders(
        self, api_client, orders_with_different_dates
    ):
        """Test that the view returns only orders within the specified date range."""
        from django.urls import reverse
        from rest_framework import status
        
        base_date = orders_with_different_dates["base_date"]
        # Date range: from 1 day after base_date to 10 days after base_date
        # Should return order2 and order3 (order1 starts before, order4 starts after)
        start_date = (base_date + timedelta(days=1)).strftime("%Y-%m-%d")
        embargo_date = (base_date + timedelta(days=10)).strftime("%Y-%m-%d")
        
        url = reverse("order-date-range")
        response = api_client.get(url, {
            "start_date": start_date,
            "embargo_date": embargo_date
        })
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2
        order_ids = [order["id"] for order in data]
        assert orders_with_different_dates["orders"][1].id in order_ids
        assert orders_with_different_dates["orders"][2].id in order_ids
    
    def test_list_orders_between_dates_requires_date_parameters(
        self, api_client, orders_with_different_dates
    ):
        """Test that the view requires both start_date and embargo_date parameters."""
        from django.urls import reverse
        from rest_framework import status
        
        url = reverse("order-date-range")
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "start_date" in response.json() or "embargo_date" in response.json()

