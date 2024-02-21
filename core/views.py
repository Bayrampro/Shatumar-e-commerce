import os
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from Shatumar import settings
from .forms import FeedbackForm, UserLoginForm
from .models import *
from django.utils.translation import gettext_lazy as _
import random
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def home(request):
    adress = About.objects.get(pk=2)
    products = Products.objects.order_by('?')[0:9]
    categories = Category.objects.order_by('?')[0:3]
    return render(request, 'core/index.html', {'products': products, 'categories': categories, 'adress': adress})


def shop(request):
    adress = About.objects.get(pk=2)
    products = Products.objects.all()
    paginator = Paginator(products, 10)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    categories = Category.objects.annotate(cnt=Count('products')).filter(cnt__gt=0)
    return render(request, 'core/shop.html', {'page_obj': page_obj, 'categories': categories, 'adress': adress})


def about(request):
    adress = About.objects.get(pk=2)
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
    return render(request, 'core/about.html', {'form': form,  'about_us': about_us, 'adress': adress})


def product_detail(request, slug):
    adress = About.objects.get(pk=2)
    product = Products.objects.get(slug=slug)
    return render(request, 'core/product_detail.html', {'product': product, 'adress': adress})


def category_detail(request, slug):
    adress = About.objects.get(pk=2)
    category = Category.objects.get(slug=slug)
    products = Products.objects.filter(category__slug=slug)
    paginator = Paginator(products, 10)

    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    categories = Category.objects.annotate(cnt=Count('products')).filter(cnt__gt=0)
    return render(request, 'core/category_detail.html', {'category': category, 'page_obj': page_obj, 'categories': categories, 'adress': adress})


# any one can add product to cart, no need of signin
def add_to_cart_view(request, pk):
    adress = About.objects.get(pk=2)
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
                      {'products': products, 'product_count_in_cart': product_count_in_cart, 'page_obj': page_obj, 'categories': categories, 'adress': adress})

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
    adress = About.objects.get(pk=2)
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
                  {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart, 'adress': adress})


def remove_from_cart_view(request, pk):
    adress = About.objects.get(pk=2)
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
                          {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart, 'adress': adress})
        if value == "":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids', value)
        return response


"""

Здесь начинается логика кода подтверждение!!!

"""


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('core/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            # return HttpResponse('Please confirm your email address to complete the registration')
            return redirect('confirm')
    else:
        form = SignupForm()
    return render(request, 'core/register.html', {'form': form})


def confirm(request):
    return render(request, 'core/confirm.html')


def success(request):
    return render(request, 'core/success.html')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('success')
    else:
        return HttpResponse('Activation link is invalid!')


def signout(request):
    logout(request)
    return redirect('register')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'core/signin.html', {'form': form})