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
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction")
]
