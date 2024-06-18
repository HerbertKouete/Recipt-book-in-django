from django.contrib import admin

# Register your models here.

from .models import User, Category, Recipe

class RecipeAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'ingredients', 'instructions', 'category', 'tags', 'images']

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Recipe, RecipeAdmin)