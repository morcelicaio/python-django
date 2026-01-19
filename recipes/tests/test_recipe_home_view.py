from unittest.mock import patch

from django.urls import reverse, resolve
from recipes import views

            # models importa User. Então dá para chamar ele daqui também.
#from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase

                    # RecipeTestBase está herdando de TestCase  (Efeito cascata aqui).
class RecipeHomeViewsTest(RecipeTestBase): 

    # Responsável por ser executado depois de cada um dos testes.
    def tearDown(self):
        return super().tearDown()

    # Função para checar se a função de view da home está correta.
    def test_recipe_home_view_function_is_correct(self):
        # view = resolve('/')       passando Hard coded    

        # fazendo a linha de cima de forma dinâminca
        view = resolve(reverse('recipes:home'))

        # Checa se essaa url da view que está sendo resolvida é a mesma em views.home.
        # Verifica se é a mesma referência.
        self.assertIs(view.func, views.home)

    # Teste que verifica se a resposta da requisição é status 200
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))

        self.assertEqual(response.status_code, 200)

    # Teste que verifica se o template usado para renderizar a página na rota / 
    # é recipes/pages/home.html
    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # Teste que verifica quando nennhuma receita é mostrada na home.    
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))

        # O atributo content de response possui a resposta do html retornada da página.
        # Porém, ele vem no formato b'...  Ou seja, vem em bytes. .decode('utf-8')
        # converte de bytes para string.  Com isso, comparamos para saber se o valor escrito
        # em home.html <h1>No recipes found here !</h1>   está dentro dessa resposta.
        self.assertIn('<h1>No recipes found here !</h1>', response.content.decode('utf-8'))


    # Testa se nosso template home.html carrega as receitas (usando fixtures)
    def test_recipe_home_template_loads_recipes(self):
        # Cria a(s) receita(s)   (é necessário para esse teste)
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))                
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Checa se uma receita existe
        self.assertIn('Recipe Title', content)                        
        self.assertEqual(len(response_context_recipes), 1)

        # Testa se nosso template home.html exibe o html que pertence a quando não carrega as receitas
    def test_recipe_home_template_dont_loads_recipes_not_published(self):
        """Teste recipe is published False dont show"""
         
        # Cria a receita com  is_published = False
        self.make_recipe(is_published = False)

        response = self.client.get(reverse('recipes:home'))        

        # Checa se uma receita existe
        self.assertIn('<h1>No recipes found here !</h1>', response.content.decode('utf-8'))

    
    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    
    # Teste para verificar número de página inválida.
    def test_invalid_page_query_uses_page_one(self):
        for i in range(8):
            kwargs = {'slug': f'r{i}', 'author_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=12A')
            self.assertEqual(
                response.context['recipes'].number,
                1
            )
            response = self.client.get(reverse('recipes:home') + '?page=2')
            self.assertEqual(
                response.context['recipes'].number,
                2
            )
            response = self.client.get(reverse('recipes:home') + '?page=3')
            self.assertEqual(
                response.context['recipes'].number,
                3
            )