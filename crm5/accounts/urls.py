from django.urls import path
from accounts import views

urlpatterns = [
    path('',views.login, name = 'location1'),
    path('home/<str:ck>/<str:pk>/',views.home, name = 'home'),
    path('products/<str:pk>/', views.products, name = 'products'), #seller id
    path('recommand/<str:pk>/', views.recommand, name = 'recommand'),
    path('location/<str:pk>/', views.location, name = 'location'),
    path('customer/<str:pk>/', views.customer, name = 'customer'), #name= 的意思是简便称呼 比如narbar就可以直接link
    path('login/',views.login, name = 'login'),
    path('filter/<str:pk>/',views.userPreference, name = 'filter'),
    path('register/',views.register, name = 'register'),
    path('create_product/<str:pk>/', views.createProduct, name = "create_product"),
    path('update_product/<str:ck>/<str:pk>/', views.updateProduct, name = "update_product"),
    path('delete_product/<str:ck>/<str:pk>/', views.deleteProduct, name = "delete_product"),
    path('buy_product/<str:ck>/<str:pk>/', views.buyProduct, name = "buy_product"), #seller id, product id
]
