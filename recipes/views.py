from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404

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
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    return render(request, 'recipes/pages/home.html', 
                  context={ 'recipes': recipes,
                })

# Quando clica no link da categoria da receita  (Carnes Assadas, Aves)  cai aqui.
def category(request, category_id):
    # Faz a busca dos dados no BD antes de 
    # colocá-los na view. 
    #recipes = Recipe.objects.filter(
    #    category__id=category_id,
    #    is_published=True).order_by('-id')

    #if not recipes:
    #    raise Http404('Not found :(')

    # Outra forma de fazer parecido com o código comentado acima    
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id, 
            is_published=True
        ).order_by('-id')
    )

    return render(request, 'recipes/pages/category.html', 
                  context={ 'recipes': recipes,
                            'title': f'{recipes[0].category.name} - Category | '
                })

# Esse parâmetro 'id' vem lá do urls.py
def recipe(request, id):
    #recipe = Recipe.objects.filter(
    #        pk=id, 
    #        is_published=True
    #    ).order_by('-id').first()
    
    # Outra forma de fazer parecido com o código comentado acima
    recipe = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(request, 'recipes/pages/recipe-view.html', 
                  context={'recipe': recipe,
                           'is_detail_page': True,
                           })