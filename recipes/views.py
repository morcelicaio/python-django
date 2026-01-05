from django.shortcuts import render

from utils.recipes.factory import make_recipe

# Create your views here.

# render recebe uma requisição e o caminho de
# um arquivo template onde está seu html
# render renderiza seu html
# os arquivos html ficam na pasta templates/recipes 
def home(request):
    return render(request, 'recipes/pages/home.html', 
                  context={
                      'recipes': [make_recipe() for _ in range(10)],
                    })

# Esse parâmetro 'id' vem lá do urls.py
def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', 
                  context={'recipe': make_recipe(),
                           'is_detail_page': True,
                           })