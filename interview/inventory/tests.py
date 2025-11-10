import pytest
from datetime import datetime, timedelta


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
def inventory_tag(db):
    """Create an inventory tag for testing."""
    from interview.inventory.models import InventoryTag
    return InventoryTag.objects.create(name="Test Tag")


@pytest.fixture
def inventory_items(db, inventory_type, inventory_language, inventory_tag):
    """Create multiple inventory items with different creation dates."""
    from interview.inventory.models import Inventory
    
    # Create items with different creation dates
    base_date = datetime(2025, 1, 1, 12, 0, 0)
    
    # Item created 5 days before the base date
    item1 = Inventory.objects.create(
        name="Old Item",
        type=inventory_type,
        language=inventory_language,
        metadata={"key": "value1"}
    )
    item1.created_at = base_date - timedelta(days=5)
    item1.save()
    item1.tags.add(inventory_tag)
    
    # Item created 2 days before the base date
    item2 = Inventory.objects.create(
        name="Recent Item",
        type=inventory_type,
        language=inventory_language,
        metadata={"key": "value2"}
    )
    item2.created_at = base_date - timedelta(days=2)
    item2.save()
    item2.tags.add(inventory_tag)
    
    # Item created on the base date
    item3 = Inventory.objects.create(
        name="Today Item",
        type=inventory_type,
        language=inventory_language,
        metadata={"key": "value3"}
    )
    item3.created_at = base_date
    item3.save()
    item3.tags.add(inventory_tag)
    
    # Item created 1 day after the base date
    item4 = Inventory.objects.create(
        name="Future Item",
        type=inventory_type,
        language=inventory_language,
        metadata={"key": "value4"}
    )
    item4.created_at = base_date + timedelta(days=1)
    item4.save()
    item4.tags.add(inventory_tag)
    
    return {
        "base_date": base_date,
        "items": [item1, item2, item3, item4]
    }


@pytest.mark.django_db
class TestInventoryCreatedAfterDateView:
    """Test cases for the view that lists inventory items created after a certain day."""
    
    def test_list_inventory_items_after_date_returns_filtered_items(
        self, api_client, inventory_items
    ):
        """Test that the view returns only items created after the specified date."""
        from django.urls import reverse
        from rest_framework import status
        
        base_date = inventory_items["base_date"]
        # Filter date: 3 days before base date (should return item2, item3, item4)
        filter_date = (base_date - timedelta(days=3)).strftime("%Y-%m-%d")
        
        url = reverse("inventory-created-after-date")
        response = api_client.get(url, {"created_after": filter_date})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3
        item_names = [item["name"] for item in data]
        assert "Old Item" not in item_names
        assert "Recent Item" in item_names
        assert "Today Item" in item_names
        assert "Future Item" in item_names
    
    def test_list_inventory_items_after_date_requires_date_parameter(
        self, api_client, inventory_items
    ):
        """Test that the view requires the created_after parameter."""
        from django.urls import reverse
        from rest_framework import status
        
        url = reverse("inventory-created-after-date")
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "created_after" in response.json()
