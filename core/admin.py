from django.contrib import admin
from .models import *


class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ['user', 'email', 'subject']


admin.site.register(Products, ProductsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(About)
