from django.shortcuts import render, redirect, get_object_or_404
from .models import Manga, Comment, Genre, Profile
from .forms import MangaForm, CommentForm, LoginForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework import viewsets
from .serializers import MangaSerializer, GenreSerializer
from flask import Flask, render_template, request, redirect, url_for, session, flash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.conf import settings
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Manga, Cart, CartItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login


def update_cart(request):
    if request.method == 'POST':
        manga_id = request.POST.get('manga_id')
        action = request.POST.get('action')
        cart = Cart.objects.get(user=request.user)
        manga = Manga.objects.get(pk=manga_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, manga=manga)
        if action == 'increment':
            cart_item.quantity += 1
        elif action == 'decrement':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
        cart_item.save()
    return redirect('cart_detail')


def view_comments(request, manga_id):
    manga = get_object_or_404(Manga, pk=manga_id)
    comments = Comment.objects.filter(manga=manga)
    return render(request, 'manga/view_comments.html', {'manga': manga, 'comments': comments})


def purchase_success(request):
    if request.method == 'POST':
        CartItem.objects.all().delete()
        return redirect('cart_detail')


def add_to_cart(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, manga=manga)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'manga/cart_detail.html', {'cart_items': cart_items})


@login_required
def remove_from_cart(request, manga_id):
    manga = get_object_or_404(Manga, id=manga_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, manga=manga)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('manga')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def generate_confirmation_code():
    return str(random.randint(10000, 99999))


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('manga')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.save()
            login(request, user)
            return redirect('manga')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class MangaViewSet(viewsets.ModelViewSet):
    queryset = Manga.objects.all()
    serializer_class = MangaSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


def genre(request, genre_name):
    genre = Genre.objects.get(name=genre_name)
    mangas = Manga.objects.filter(genre=genre)
    return render(request, 'manga/genre.html', {'mangas': mangas, 'genre': genre_name})


def adventure(request):
    mangas = Manga.objects.filter(genre='adventure')
    return render(request, 'manga/genre.html', {'mangas': mangas, 'genre': 'adventure'})


def fantasy(request):
    mangas = Manga.objects.filter(genre='fantasy')
    return render(request, 'manga/genre.html', {'mangas': mangas, 'genre': 'fantasy'})


def action(request):
    mangas = Manga.objects.filter(genre='action')
    return render(request, 'manga/genre.html', {'mangas': mangas, 'genre': 'action'})


def adventures(request):
    mangas = Manga.objects.filter(genre='adventures')
    return render(request, 'manga/genre.html', {'mangas': mangas, 'genre': 'adventures'})


def dark_fantasy(request):
    mangas = Manga.objects.filter(genre='dark_fantasy')
    return render(request, 'manga/genre.html', {'mangas': mangas, 'genre': 'dark_fantasy'})


def supernatural(request):
    mangas = Manga.objects.filter(genre='supernatural')
    return render(request, 'manga/genre.html', {'mangas': mangas, 'genre': 'supernatural'})


def manga(request):
    genres = Genre.objects.all()
    genre_id = request.GET.get('genre')
    mangas = Manga.objects.all()
    if genre_id:
        mangas = mangas.filter(genre_id=genre_id)
    paginator = Paginator(mangas, 1)
    page = request.GET.get('page')
    try:
        mangas = paginator.page(page)
    except PageNotAnInteger:
        mangas = paginator.page(1)
    except EmptyPage:
        mangas = paginator.page(paginator.num_pages)

    return render(request, 'manga/manga.html', {'mangas': mangas, 'genres': genres})


def view_manga(request, manga_id):
    manga = get_object_or_404(Manga, pk=manga_id)
    comments = Comment.objects.filter(manga=manga)
    return render(request, 'manga/view_manga.html', {'manga': manga, 'comments': comments})


def add_manga(request):
    if request.method == 'POST':
        form = MangaForm(request.POST, request.FILES)
        if form.is_valid():
            manga = form.save(commit=False)
            manga.author = request.user
            manga.save()
            return redirect('manga')
    else:
        form = MangaForm()
    return render(request, 'manga/add_manga.html', {'form': form})


def update_manga(request, id):
    manga = get_object_or_404(Manga, pk=id)
    form = MangaForm(request.POST or None, instance=manga)
    if form.is_valid():
        form.save()
        return redirect('manga')
    return render(request, 'manga/update_manga.html', {'form': form})


def delete_manga(request, id):
    manga = get_object_or_404(Manga, pk=id)
    manga.delete()
    return redirect('manga')


def add_comment(request, manga_id):
    manga = get_object_or_404(Manga, pk=manga_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.manga = manga
            comment.save()
            return redirect('manga')
    else:
        form = CommentForm()
    return render(request, 'manga/add_comment.html', {'form': form})


def contact(request):
    return render(request, 'manga/contact.html')

