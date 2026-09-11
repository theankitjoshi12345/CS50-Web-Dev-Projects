from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import json

from .models import User, Comment, Post, Like


def index(request):
    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get('page', 1)
    pageObject = paginator.get_page(pageNumber)
    return render(request, "network/index.html", {
        "posts":pageObject,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def newpost(request):
    if request.method == "POST":
        try: 
            data = json.loads(request.body)
            content = data.get("content", "").strip()

            newpost = Post(user=request.user, content=content)
            newpost.save()

            return JsonResponse({
                "message":"Post created successfully.",
                "post":newpost.serialize()
            }, status=201)
        except Exception as e:
            return JsonResponse({
                "error":str(e)
            }, status = 400)

    return redirect("index")

def delete(request, id):
    if (request.method != "DELETE"):
        return redirect('index')
    try:
        post = Post.objects.get(id=id)
        post.delete()
        return JsonResponse({
            "message":"Post deleted successfully."
        }, status=200)
    except Exception as e:
        return JsonResponse({
            "message": str(e)
        }, status=400)

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get('page', 1)
    pageObject = paginator.get_page(pageNumber)
    if(request.user in user.followers.all()):
        followButtonNeeded = "Unfollow"
    else:
        followButtonNeeded = "Follow"
    return render(request, "network/profile.html", {
        "posts":pageObject,
        "following":user.following.all().count(),
        "followers": user.followers.all().count(),
        "username": username,
        "followButtonNeeded": (request.user.username != username),
        "followButtonValue": followButtonNeeded,
    })

@login_required
def following(request):
    posts = Post.objects.filter(user__in=request.user.following.all()).order_by("-timestamp")
    paginator = Paginator(posts, 10)
    pageNumber = request.GET.get('page', 1)
    pageObject = paginator.get_page(pageNumber)
    return render(request, "network/following.html", {
        "posts":pageObject,
    })

@login_required
def follow(request, username):
    if (request.method == "PUT"):
        try:
            user = User.objects.get(username=username)
            request.user.following.add(user)
            return JsonResponse({
                "message": "follow request successful"
            }, status = 200)
        except Exception as e:
            return JsonResponse({
                "message":str(e),
            }, status = 400)
    return redirect('index')

@login_required
def unfollow(request, username):
    if (request.method == "PUT"):
        try:
            user = User.objects.get(username=username)
            request.user.following.remove(user)
            return JsonResponse({
                "message": "unfollow request successful"
            }, status = 200)
        except Exception as e:
            return JsonResponse({
                "message":str(e),
            }, status = 400)
    return redirect('index')

@login_required
def edit(request, id):
    if (request.method == "PUT"):
        try:
            post = Post.objects.get(id=id)
            if(request.user == post.user):
                data = json.loads(request.body)
                post.content = data.get('content')
                post.save()
                return JsonResponse({
                    "message": "Post updated successfully"
                }, status=200)
        except Exception as e:
            return JsonResponse({
                "message": str(e)
            }, status=400)
    return redirect('index')

@login_required
def likes(request, id):
    if (request.method == "PUT"):
        try:
            post = Post.objects.get(id=id);
            liked = Like.objects.filter(user=request.user, post=post).exists()
            if(liked):
                Like.objects.filter(user=request.user, post=post).delete()
            else:
                Like.objects.create(user=request.user, post=post)
            return JsonResponse({
                "message":"Like button worked successfully.",
                "likes":post.likes.count()
            }, status=200)
        except Exception as e:
            return JsonResponse({
                "message":str(e),
            }, status=400)      
    return redirect('index')