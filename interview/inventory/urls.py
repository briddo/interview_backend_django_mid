from django.urls import path
from interview.inventory.views import (
    InventoryCreatedAfterDateView,
    InventoryLanguageListCreateView,
    InventoryLanguageRetrieveUpdateDestroyView,
    InventoryListCreateView,
    InventoryRetrieveUpdateDestroyView,
    InventoryTagListCreateView,
    InventoryTagRetrieveUpdateDestroyView,
    InventoryTypeListCreateView,
    InventoryTypeRetrieveUpdateDestroyView,
)
from interview.order.views import OrderListCreateView, OrderTagListCreateView


urlpatterns = [
    path(
        "created-after-date/",
        InventoryCreatedAfterDateView.as_view(),
        name="inventory-created-after-date",
    ),
    path(
        "<int:id>/",
        InventoryRetrieveUpdateDestroyView.as_view(),
        name="inventory-detail",
    ),
    path(
        "languages/<int:id>/",
        InventoryLanguageRetrieveUpdateDestroyView.as_view(),
        name="inventory-languages-detail",
    ),
    path(
        "tags/<int:id>/",
        InventoryTagRetrieveUpdateDestroyView.as_view(),
        name="inventory-tags-detail",
    ),
    path(
        "types/<int:id>/",
        InventoryTypeRetrieveUpdateDestroyView.as_view(),
        name="inventory-types-detail",
    ),
    path(
        "languages/",
        InventoryLanguageListCreateView.as_view(),
        name="inventory-languages-list",
    ),
    path("tags/", InventoryTagListCreateView.as_view(), name="inventory-tags-list"),
    path("types/", InventoryTypeListCreateView.as_view(), name="inventory-types-list"),
    path("", InventoryListCreateView.as_view(), name="inventory-list"),
]
