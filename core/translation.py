from modeltranslation.translator import translator, TranslationOptions
from .models import *


class ProductsTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


translator.register(Products, ProductsTranslationOptions)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Category, CategoryTranslationOptions)
