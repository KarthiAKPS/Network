from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm
from django.core.paginator import Paginator
import json
from .models import User, Post, Follow, Comment

def index(request):
    if request.method=="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.creater = request.user
            post.save()
            return HttpResponseRedirect( reverse("index"))
        else:
            return render(request, "network/index.html", {
                "form": form,
                "message": "Enter valid details"
                })
    else:
        user = request.user
        form = PostForm()
        all_posts = Post.objects.all().order_by('time').reverse()
        liked_posts = []
        posts_id = []
        for post in all_posts:
            if user in post.liked.all():
                liked_posts.append(post)
                posts_id.append(post.id)
        p = Paginator(all_posts, 10)
        page_no = request.GET.get('page')
        posts = p.get_page(page_no)
        return render(request, "network/index.html", {
                "form" : form,
                "posts": posts,
                "liked" : liked_posts,
                "p_id" : posts_id
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

def profile(request, id):
    u = User.objects.get(pk = id)
    user = request.user
    same = u == user
    all_posts = Post.objects.filter(creater = u).order_by('time').reverse()
    p = Paginator(all_posts, 10)
    page_no = request.GET.get('page')
    posts = p.get_page(page_no)
    fowings = Follow.objects.filter(following = id)
    fowers = Follow.objects.filter(me = id)
    if Follow.objects.filter(following = u, me = user):
        s = True
    else:
        s = False
    return render(request, "network/profile.html", {
            "posts": posts,
            "usr" : u,
            'fg' : fowings,
            'fr' : fowers,
            'u' : same,
            's' : s
        })
    
def follow(request, id):
    i = request.user
    u = User.objects.get(pk = id)
    if Follow.objects.filter(following = u, me =i):
        print('already following')
    else:
        f = Follow(following = u, me = i)
        f.save()
    return HttpResponseRedirect(reverse('profile', args=(id, )))

def unfollow(request, id):
    i = request.user
    u = User.objects.get(pk = id)
    f = Follow.objects.filter(following = u, me = i)
    f.delete()
    return HttpResponseRedirect(reverse('profile', args=(id, )))

def following(request):
    follng = Follow.objects.filter(me = request.user)
    all_posts = Post.objects.all().order_by('time').reverse()
    f_list = []
    for post in all_posts:
        for per in follng:
            if post.creater == per.following:
                f_list.append(post)
    p = Paginator(f_list, 10)
    page_no = request.GET.get('page')
    posts = p.get_page(page_no)
    
    user = request.user
    liked_posts = []
    posts_id = []
    for post in all_posts:
        if user in post.liked.all():
            liked_posts.append(post)
            posts_id.append(post.id)
    
    return render(request, "network/following.html", {
            "posts": posts,
            "liked" : liked_posts,
            "p_id" : posts_id
        })
    
def delete(request, id):
    Post.objects.filter(pk = id).delete()
    return HttpResponseRedirect(reverse('index'))

def edit(request, id):
    if request.method == 'POST':
        post = Post.objects.get(pk = id)
        data = json.loads(request.body)
        post.content = data["content"]
        post.save()
        return JsonResponse({'data': data['content'], 'message':'successfully changed'})
    
def like(request, id):
    post = Post.objects.get(pk = id)
    user = request.user
    u = Post.objects.filter(liked = user)
    all_posts = Post.objects.all().order_by('time').reverse()
    posts_id = []
    for p in all_posts:
        if user in p.liked.all():
            posts_id.append(p.id)
    if post in u:
        print('already liked')
        return HttpResponseRedirect(reverse('unlike', args=(id,)))
    else:
        post.liked.add(user)
        post.save()
        return JsonResponse({'message':'liked successfully', 'data':posts_id})
    
def unlike(request, id):
    post = Post.objects.get(pk = id)
    user = request.user
    u = Post.objects.filter(liked = user)
    all_posts = Post.objects.all().order_by('time').reverse()
    posts_id = []
    for p in all_posts:
        if user in p.liked.all():
            posts_id.append(p.id)
    if post in u:
        post.liked.remove(user)
        post.save()
        return JsonResponse({'message':'unliked successfully', 'data':posts_id})
    else:
        print('already unliked')
        return HttpResponseRedirect(reverse('like', args=(id,)))

def comment(request, id):
    if request.method == 'POST':
        comments = request.POST['comment']
        u = request.user
        i = Post.objects.get(pk = id)
        o = Comment(commenter=u, comment=comments, commented=i )
        o.save()
        return HttpResponseRedirect(reverse("readcomms", args=(i.id, )))

def readcomms(request, id):
    i = Post.objects.get(pk = id)
    try:
        comms = Comment.objects.filter(commented = i)
        return render(request, 'network/comment.html', {
                                                    'i': id,
                                                    'comms': comms})
    except:
        message = "no comments"
        return render(request, 'network/comment.html', {
                                                    'i': id,
                                                    'm': message})