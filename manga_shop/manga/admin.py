from django.contrib import admin
from .models import Manga, Comment, Genre, Profile, Cart, CartItem

admin.site.register(Manga)
admin.site.register(Comment)
admin.site.register(Genre)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItem)

