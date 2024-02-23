from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('shop/', shop, name='shop'),
    path('about/', about, name='about'),
    path('download/Taze prise list 2024.pdf/', lambda request: FileResponse(open('media/Taze prise list 2024.pdf', 'rb'), content_type='application/pdf'), name='download_pdf'),
    path('product/<str:slug>/', product_detail, name='product_detail'),
    path('category/<str:slug>/', category_detail, name='category_detail'),

    #here is add cart urls
    path('add-to-cart/<int:pk>', add_to_cart_view, name='add-to-cart'),
    path('cart', cart_view, name='cart'),
    path('remove-from-cart/<int:pk>', remove_from_cart_view, name='remove-from-cart'),

    #here is confirmation urls
    path('register/', signup, name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    activate, name='activate'),
    path('confirm/', confirm, name='confirm'),
    path('success/', success, name='success'),
    path('logout/', signout, name='logout'),
    path('login/', user_login, name='login'),

    #here is newsletter's urls
    path('send_newsletter/', send_newsletter, name='send_newsletter'),
]
