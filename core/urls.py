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
]
