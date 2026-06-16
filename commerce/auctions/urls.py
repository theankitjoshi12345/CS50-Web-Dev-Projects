from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.createListing, name="createListing"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("category", views.category, name="category"),
    path("category/<path:category>", views.categorySpecific, name="categorySpecific"),
    path("placeBid/<int:id>", views.placeBid, name="placeBid"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("winnings", views.winnings, name="winnings"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
]
