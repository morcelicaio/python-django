import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404

from utils.pagination import make_pagination

from recipes.models import Recipe

PER_PAGE = int(os.environ.get('PER_PAGE', 6))   # valor da variável PER_PAGE senao usar o valor padrão 6

# Create your views here.

# render recebe uma requisição e o caminho de
# um arquivo template onde está seu html
# render renderiza seu html
# os arquivos html ficam na pasta templates/recipes 
def home(request):
    # Faz a busca dos dados no BD antes de 
    # colocá-los na view. 
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')


    # paginação    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)


    return render(request, 'recipes/pages/home.html', 
                  context={ 'recipes': page_obj, 'pagination_range': pagination_range
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

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/category.html', 
                  context={ 'recipes': page_obj,
                            'pagination_range': pagination_range,
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


def search(request):
    #Em .GET, caso a url não venha com o parâmetro q, isso pode estourar um erro http 500.
    # Com .GET.get()    o .get acessa o dicionário (QueryDict: {}) que está em .GET e tentar procurar ['q'].
    # Se não houver essa chave é retornado None e esse None é possível tratar aqui. 
    search_term = request.GET.get('q', '').strip() # strip remove espaços em branco(ou outros caracs) d início e d fim de 1 str.

    # Se não houver nada em search_term, ou seja, se for None.
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        # title__contains   isso faz uma busca  usando LIKE na base de dados.
        Q(
            Q(title__contains = search_term) | Q(description__contains = search_term)
        ),
        is_published = True
        #Q é uma biblioteca do django que serve para avisar ao framework que isso é uma consulta OR no BD   usa-se o |
        # Em is_published   ele faz um AND. 
    ).order_by('-id') 

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/search.html', { 
        'page_title': f'Search for "{ search_term }" |', 
        'search_term': search_term ,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',      
    })