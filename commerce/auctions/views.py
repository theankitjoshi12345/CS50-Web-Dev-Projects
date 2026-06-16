from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Bid, Comment, Watchlist

categories_list = [
    "Electronics",
    "Fashion & Apparel",
    "Home & Garden",
    "Books & Education",
    "Toys & Hobbies",
    "Sports & Outdoors",
    "Collectibles & Art",
    "Automotive",
    "Health & Beauty",
    "Other"
]


def index(request):
    if request.user.is_authenticated:
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(active=True),
        })
    else:
        return redirect("login")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createListing(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST["name"]
            description = request.POST["description"]
            image = request.FILES.get("image")
            category = request.POST["category"]
            price = request.POST["price"]
            
            newListing = Listing(
                name=name.capitalize(),
                description=description,
                image=image,
                owner=request.user,
                category=category,
                price=price,
            )

            newListing.save()
            messages.success(request, f"Listing for \"{newListing.name}\" has been uploaded successfully.")
            return redirect("listing", id = newListing.id)

        else:
            return render(request, "auctions/listing.html", {
                "categories": categories_list,
            })

    return redirect("login")

@login_required    
def listing(request, id):
    listing = Listing.objects.get(pk=id)
    isWatchlisted = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    return render(request, "auctions/listingIndividual.html", {
        "listing": listing,
        "isWatchlisted":isWatchlisted,
        "comments": Comment.objects.filter(listing = listing)
    })

@login_required
def category(request):
    return render(request, "auctions/category.html",{
        "categories": categories_list,
    })

@login_required
def categorySpecific(request, category):
    return render(request, "auctions/categorySpecific.html",{
        "category":category,
        "listings": Listing.objects.filter(category=category),
        })

@login_required
def placeBid(request, id):
    if request.method=="POST":
        listing=Listing.objects.get(pk=id)
        newBid = Bid(
            bidder = request.user,
            listing = listing,
            amount = request.POST["newBid"]
        )
        newBid.save()
        # print("newBid saved successfully.")
        listing.price = request.POST["newBid"]
        listing.save()
        messages.success(request, "Your bid has placed successfully. Best of luck!")
        return redirect("listing", id=id)
    else:
        return redirect("index")

@login_required
def closeListing(request, id):
    listing = Listing.objects.get(pk=id)
    if (request.user == listing.owner):
        listing.active = False
        highestBid = listing.bids.order_by('-amount').first()
        if highestBid is not None:
            listing.winner = highestBid.bidder
        else:
            listing.winner = None
        print(listing.winner)
        listing.save()
        messages.success(request, f"Your listing for \"{listing.name}\" is closed successfully.")
        return redirect("listing", id=id)
    else:
        redirect("index")

@login_required
def addWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    user = request.user
    watch = Watchlist(user = user, listing = listing)
    watch.save()
    messages.success(request, f"\"{listing.name}\" has been added to your watchlist successfully.")
    return redirect("listing", id)

@login_required
def watchlist(request):
    listings = Listing.objects.filter(watchlistedBy__user = request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def removeWatchlist(request, id):
    listing = Listing.objects.get(pk=id)
    listing.watchlistedBy.filter(user=request.user).delete()
    messages.success(request, f"\"{listing.name}\" has been removed from your watchlist successfully.")
    return redirect("listing", id)

@login_required
def winnings(request):
    listings = Listing.objects.filter(winner=request.user)
    return render(request, "auctions/winnings.html", {
        "listings": listings
    })

@login_required
def addComment(request, id):
    if request.method == "POST": 
        listing = Listing.objects.get(pk=id)
        newComment = Comment(
            commenter = request.user,
            listing = listing,
            content = request.POST["content"]
        )
        newComment.save()
        messages.success(request, "Your comment has been posted.")
    return redirect("listing", id = id)
