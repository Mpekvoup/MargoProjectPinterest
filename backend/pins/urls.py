from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Pins
    path('pin/<int:pk>/', views.pin_detail, name='pin_detail'),
    path('pin/create/', views.pin_create, name='pin_create'),
    path('pin/<int:pk>/edit/', views.pin_edit, name='pin_edit'),
    path('pin/<int:pk>/delete/', views.pin_delete, name='pin_delete'),
    path('pin/<int:pk>/like/', views.pin_like, name='pin_like'),

    # Boards
    path('boards/', views.board_list, name='board_list'),
    path('board/<slug:slug>/', views.board_detail, name='board_detail'),
    path('board/create/', views.board_create, name='board_create'),
    path('board/<slug:slug>/edit/', views.board_edit, name='board_edit'),
    path('board/<slug:slug>/delete/', views.board_delete, name='board_delete'),

    # Profile
    path('user/<str:username>/', views.profile, name='profile'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
