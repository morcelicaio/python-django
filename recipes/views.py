from django.http import Http404
from django.shortcuts import render

from utils.recipes.factory import make_recipe

from recipes.models import Recipe

# Create your views here.

# render recebe uma requisição e o caminho de
# um arquivo template onde está seu html
# render renderiza seu html
# os arquivos html ficam na pasta templates/recipes 
def home(request):
    # Faz a busca dos dados no BD antes de 
    # colocá-los na view. 
    recipes = Recipe.objects.all().filter(is_published=True).order_by('-id')

    return render(request, 'recipes/pages/home.html', 
                  context={ 'recipes': recipes,
                })

def category(request, category_id):
    # Faz a busca dos dados no BD antes de 
    # colocá-los na view. 
    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True).order_by('-id')

    if not recipes:
        raise Http404('Not found :(')

    return render(request, 'recipes/pages/category.html', 
                  context={ 'recipes': recipes,
                            'title': f'{recipes.first().category.name} - Category | '
                })

# Esse parâmetro 'id' vem lá do urls.py
def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', 
                  context={'recipe': make_recipe(),
                           'is_detail_page': True,
                           })