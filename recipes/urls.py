from django.urls import path

#Esses dois imports abaixo são a mesma coisa
#from recipes.views import home
from . import views

# recipes:recipe
app_name = 'recipes'

urlpatterns = [    
    path('', views.home, name='home'),

    path('recipes/category/<int:category_id>/', views.category, name='category'),
    # colocando a sintaxe de parâmetro da url <>,
    # o django já consegue passar automaticamente
    ## esse parâmetro lá na chamada de views.recipe
    path('recipes/<int:id>/', views.recipe, name='recipe'),    

]