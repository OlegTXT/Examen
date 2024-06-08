from django.urls import path, include
from rest_framework import routers
from .views import MangaViewSet, GenreViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'mangas', MangaViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = [
    path('', views.manga, name='manga'),
    path('genre/<str:genre>/', views.genre, name='genre'),
    path('manga/add/', views.add_manga, name='add_manga'),
    path('manga/<int:id>/update/', views.update_manga, name='update_manga'),
    path('manga/<int:id>/delete/', views.delete_manga, name='delete_manga'),
    path('manga/<int:manga_id>/comment/', views.add_comment, name='add_comment'),
    path('manga/<int:manga_id>/', views.view_manga, name='view_manga'),
    path('add_to_cart/<int:manga_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:manga_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('manga/<int:manga_id>/comments/', views.view_comments, name='view_comments'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove_from_cart/<int:manga_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('purchase_success/', views.purchase_success, name='purchase_success'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('contact/', views.contact, name='contact'),

    path('adventure/', views.adventure, name='adventure'),
    path('fantasy/', views.fantasy, name='fantasy'),
    path('action/', views.action, name='action'),
    path('adventures/', views.adventures, name='adventures'),
    path('dark_fantasy/', views.dark_fantasy, name='dark_fantasy'),
    path('supernatural/', views.supernatural, name='supernatural'),
    path('api/', include(router.urls)),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]

