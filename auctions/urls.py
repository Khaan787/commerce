from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("add_listing/<int:that_listing>", views.add_listing, name="add_listing"),
    path("remove_listing/<int:listing_id>", views.remove_listing, name="remove_listing"),
    path("bid_placed/<int:listing_id>", views.bid_placed, name="bid_placed"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("listing_comment/<int:listing_id>", views.listing_comment, name="listing_comment"),
    path("categories", views.categories, name = "categories"),
    path("category_listings/<str:category>", views.category_listings, name="category_listings")
]
