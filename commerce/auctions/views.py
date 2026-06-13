from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import User, Listing, Bid, Comment

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
            "listings": Listing.objects.all(),
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
                name=name,
                description=description,
                image=image,
                owner=request.user,
                category=category,
                price=price,
            )

            newListing.save()
            return redirect("index")

        else:
            return render(request, "auctions/listing.html", {
                "categories": categories_list,
            })

    return redirect("login")

    
