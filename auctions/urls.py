from django.urls import path

from . import views
from .views import ListingCreateView, ListingDetailView

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", ListingCreateView.as_view(), name="listing-add"),
    path("<int:pk>", ListingDetailView.as_view(), name="listing-detail"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/add", views.add_to_watchlist, name="add-to-watchlist"),
    path("watchlist/<int:listing_id>/remove", views.remove_from_watchlist, name="remove-from-watchlist"),
    path("listing/<int:listing_id>", views.listing_page, name="listing-page"),
    path("bidding/<int:listing_id>", views.bidding, name="bidding"),
    path("listing/<int:listing_id>/close", views.close_auction, name="close-auction"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_name>", views.category, name="category")
]
