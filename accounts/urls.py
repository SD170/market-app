from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),


    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),


    path('account/', views.accountsSettings, name="account"),
    
    
    path('products/', views.products, name='products'),  
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('createOrder/<str:pk>/', views.createOrder, name="createOrder"),
    path('updateOrder/<str:pk>/', views.updateOrder, name="updateOrder"),
    path('deleteOrder/<str:pk>/', views.deleteOrder, name="deleteOrder"),


    path(
        'reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
        name="password_reset"
        ),
        
    path(
        'reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name='password_reset_done'
        ),

    path(
        'reset_password/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
        name='password_reset_confirm'
        ),

    path(
        'reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name='password_reset_complete'
        ),
]

