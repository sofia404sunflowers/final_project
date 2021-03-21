import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Recording


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    posts_list = [post.serialize() for post in posts]
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{
        "page_obj": page_obj,
    })

def video_posts(request):
    records = Recording.objects.all().order_by('-id')

    paginator = Paginator(records, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/videolist.html",{
        "page_obj": page_obj,
    })

def video_post(request, video_id):
    record = Recording.objects.get(id=video_id)
    return render(request, "network/videopage.html",{
        "record": record,
    })

def follow(request, account_id):

    follover = request.user
    following = User.objects.get(id=account_id)

    follover.follows.add(following)
    follover.save()

    following.followers.add(follover)
    following.save()

    return HttpResponseRedirect(reverse("account", args=[account_id]))


def unfollow(request, account_id):
    follover = request.user
    following = User.objects.get(id=account_id)

    follover.follows.remove(following)
    follover.save()

    following.followers.remove(follover)
    following.save()

    return HttpResponseRedirect(reverse("account", args=[account_id]))


def account(request, account_id):
    user = User.objects.get(id=account_id)
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    user_in_follow_list = request.user in user.followers.all()


    posts_list = [post.serialize() for post in posts]
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/account.html",{
        "account": user,
        "posts": posts,
        "user_in_follow_list": user_in_follow_list,
        "page_obj": page_obj,
    })


@csrf_exempt
@login_required
def following(request):
    if request.user.is_authenticated:
        user = request.user
        follows = user.follows.all()
        posts = []
        for follow in follows:
            follow_posts = Post.objects.filter(user = follow)
            for follow_post in follow_posts:
                posts.append(follow_post)

        posts.sort(key=lambda x: x.timestamp, reverse=True)
        posts_list = [post.serialize() for post in posts]
        paginator = Paginator(posts_list, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html",{
            "page_obj": page_obj,
        })
    else:
        return HttpResponseRedirect(reverse("index"))



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


class Posts(ListView):
    paginate_by = 3  # для наглядности
    model = Post
    template_name = "network/posts.html"
    posts = Post.objects.all().order_by('-timestamp')
    queryset = [post.serialize() for post in posts]


def post_list(request):

    posts = Post.objects.all().order_by('-timestamp')

    return JsonResponse([post.serialize() for post in posts], safe=False, )


@csrf_exempt
@login_required
def post_submit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    text = data["text"]
    user = request.user
    post = Post.objects.create(user=user, text=text)
    post.save()

    return JsonResponse({"message": "Post posted successfully.", "data": post.serialize()}, status=201)




@csrf_exempt
@login_required
def post_details(request, post_id):

    # Query for requested post
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("text") is not None:
            post.text = data["text"]
        elif data.get("likes") == "True":
            post.likes.add(request.user)
        elif data.get("unlikes") == "True":
            post.likes.remove(request.user)

        post.save()
        return JsonResponse(post.serialize(), status=200)

    # Post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

