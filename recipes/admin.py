from django.contrib import admin
from .models import Category, Recipe

# Register your models here.



class CategoryAdmin(admin.ModelAdmin):
    ...

# Essa é uma segunda forma de registrar no painel
# adm do django também
@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...

# Isso é para aparecer na área administrativa do 
# django   (http://localhost:8000/admin)
admin.site.register(Category, CategoryAdmin)
