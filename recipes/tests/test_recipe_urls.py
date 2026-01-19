from django.test import TestCase
from django.urls import reverse

# Classe que vai ter todos os testes
class RecipeURLsTest(TestCase):    
    def test_recipe_home_url_is_correct(self): 
        # testando a url reversa. Ou seja, Lá da view ele tenta descobrir qual url está sendo chamado
        # através do url recipes:home que tem á no arquivo header.html por exemplo       
        url = reverse('recipes:home')

        # checa se a url da home eh '/'
        self.assertEqual(url, '/')


    def test_recipe_category_url_is_correct(self): 
        # passando o parâmetro com args (é passado uma tupla de argumentos na sequência)
        #url = reverse('recipes:category', args=(1,))

        # passando o parâmetro com kwargs (é passado um dicionário com argumentos nomeados)
        url = reverse('recipes:category', kwargs={'category_id': 1})

        self.assertEqual(url, '/recipes/category/1/')

    def test_recipe_deail_url_is_correct(self):
        url = reverse('recipes:recipe', args=(1,))
        self.assertEqual(url, '/recipes/1/')


    # Aqui a url é passada por query string.
    def test_recipe_search_url_is_correct(self):
        url = reverse('recipes:search')
        self.assertEqual(url, '/recipes/search/')