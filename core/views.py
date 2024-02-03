import os

from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from Shatumar import settings
from .forms import FeedbackForm
from .models import *
from django.utils.translation import gettext_lazy as _


def home(request):
    products = Products.objects.order_by('?')[0:9]
    categories = Category.objects.order_by('?')[0:3]
    return render(request, 'core/index.html', {'products': products, 'categories': categories})


def shop(request):
    products = Products.objects.all()
    paginator = Paginator(products, 10)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    categories = Category.objects.annotate(cnt=Count('products')).filter(cnt__gt=0)
    return render(request, 'core/shop.html', {'page_obj': page_obj, 'categories': categories})


def about(request):
    about_us = About.objects.get(pk=1)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            subject = form.cleaned_data['subject']
            message = f'Email: {feedback.email}\nMessage: {feedback.subject}'
            from_email = form.cleaned_data['email']
            to_email = settings.DEFAULT_FROM_EMAIL
            mail = send_mail(subject, message, from_email, [to_email], fail_silently=False)
            if mail:
                form.save()
                messages.success(request, _('Hat üstünlikli ugradyldy'))
            else:
                feedback.delete()
                messages.error(request, _('Internet birikdirmesi ýitdi'))
        else:
            messages.error(request, _('Näsazlyk ýüze çykdy'))
            # return redirect('about')
    else:
        form = FeedbackForm()
    return render(request, 'core/about.html', {'form': form,  'about_us': about_us})


def product_detail(request, slug):
    product = Products.objects.get(slug=slug)
    return render(request, 'core/product_detail.html', {'product': product})


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    products = Products.objects.filter(category__slug=slug)
    paginator = Paginator(products, 10)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    categories = Category.objects.annotate(cnt=Count('products')).filter(cnt__gt=0)
    return render(request, 'core/category_detail.html', {'category': category, 'page_obj': page_obj, 'categories': categories})


# any one can add product to cart, no need of signin
def add_to_cart_view(request, pk):
    products = Products.objects.all()
    paginator = Paginator(products, 10)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    categories = Category.objects.annotate(cnt=Count('products')).filter(cnt__gt=0)

    # for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 1

    response = render(request, 'core/shop.html',
                      {'products': products, 'product_count_in_cart': product_count_in_cart, 'page_obj': page_obj, 'categories': categories})

    # adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids == "":
            product_ids = str(pk)
        else:
            product_ids = product_ids + "|" + str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product = Products.objects.get(id=pk)
    return response


# for checkout of cart
def cart_view(request):
    # for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    # fetching product details from db whose id is present in cookie
    products = None
    total = 0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart = product_ids.split('|')
            products = Products.objects.all().filter(id__in=product_id_in_cart)

            # for total price shown in cart
            for p in products:
                total = total + p.cost
    return render(request, 'core/cart.html',
                  {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart})


def remove_from_cart_view(request, pk):
    # for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    # removing product id from cookie
    total = 0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart = product_ids.split('|')
        product_id_in_cart = list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products = Products.objects.all().filter(id__in=product_id_in_cart)
        # for total price shown in cart after removing product
        for p in products:
            total = total + p.cost

        #  for update coookie value after removing product id in cart
        value = ""
        for i in range(len(product_id_in_cart)):
            if i == 0:
                value = value + product_id_in_cart[0]
            else:
                value = value + "|" + product_id_in_cart[i]
        response = render(request, 'core/cart.html',
                          {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart})
        if value == "":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids', value)
        return response
