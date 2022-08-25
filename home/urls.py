from home import views
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .middlewares.auth import  auth_middleware

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('store/', views.store , name='store'),
    path('product/', views.product, name='product'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('productpage/', views.productPage, name='productPage'),
    path('signup/', views.signup.as_view(), name='signup'),
    path('login/', views.login.as_view(), name='login'),
    path('logout/', views.logout , name='logout'),
    path('search/', views.search , name='search'),
    path('faq/', views.faq , name='faq'),
    path('cart/', views.Cart.as_view() , name='cart'),
    path('checkOut/', auth_middleware(views.checkOut.as_view()) , name='checkOut'),
    # path('orders', auth_middleware(OrderView.as_view()), name='orders'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)