from django.urls import reverse, resolve
from recipes import views
from unittest import skip

            # models importa User. Então dá para chamar ele daqui também.
#from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase

                    # RecipeTestBase está herdando de TestCase  (Efeito cascata aqui).
class RecipeViewsTest(RecipeTestBase): 

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




    def test_recipe_category_view_function_is_correct(self):        
        # fazendo de forma dinâminca
        view = resolve(reverse('recipes:category', kwargs={ 'category_id': 1000 }))
        
        # Checa se essa url da view que está sendo resolvida é a mesma em views.category.
        # Verifica se é a mesma referência.
        self.assertIs(view.func, views.category)        
    
    # Teste que verifica se a resposta da requisição é status 404
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={ 'category_id': 1000 }))

        self.assertEqual(response.status_code, 404)


    # Testa se nosso template category.html carrega as receitas (usando fixtures)
    def test_recipe_category_template_loads_recipes(self):
        # Cria a(s) receita(s)   (é necessário para esse teste)
        needed_title = 'This is a category test'
        self.make_recipe(title = needed_title)

        response = self.client.get(reverse('recipes:category', args=(1, )))                
        content = response.content.decode('utf-8')        

        # Checa se uma receita existe
        self.assertIn(needed_title, content)        




    def test_recipe_detail_view_function_is_correct(self):                
        view = resolve(reverse('recipes:recipe', kwargs={ 'id': 1 }))
                
        # Verifica se é a mesma referência.
        self.assertIs(view.func, views.recipe)

    # Teste que verifica se a resposta da requisição é status 404
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:recipe', kwargs={ 'id': 1000 }))

        self.assertEqual(response.status_code, 404)

    # Testa se nosso template recipe-view.html carrega a receita (usando fixtures)
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        # Cria a(s) receita(s)   (é necessário para esse teste)
        needed_title = 'This is a detail page - It load one recipe'

        # Precisa de uma receita para esse teste
        self.make_recipe(title = needed_title)   #Cria fixture de uma recipe

        response = self.client.get(reverse('recipes:recipe', kwargs={ 'id': 1 }))                
        content = response.content.decode('utf-8')        

        # Checa se uma receita existe
        self.assertIn(needed_title, content)     

    