from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listings, name="create"),
    path("create/", views.create_listings, name="create"),
    path("listings/<int:product_id>", views.display_listing, name="listings"),
    path("bid", views.bid, name="bid"),
    path("comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("categories", views.categories, name="categories"),
    path("filter_categories/<str:cat>", views.filter_categories, name="filter_categories"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),
    path("my_winnings", views.my_winnings, name="my_winnings"),
]
