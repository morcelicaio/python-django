from django.urls import reverse, resolve
from recipes import views

            # models importa User. Então dá para chamar ele daqui também.
#from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase

                    # RecipeTestBase está herdando de TestCase  (Efeito cascata aqui).
class RecipeCategoryViewsTest(RecipeTestBase): 

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

        # Testa se nosso template category.html exibe o erro 404 p/ receita não publicadas
    def test_recipe_category_template_dont_loads_recipes_not_published(self):
        """Teste recipe is published False dont show"""
         
        # Cria a receita com  is_published = False
        recipe = self.make_recipe(is_published = False)

        response = self.client.get(reverse('recipes:recipe', kwargs = { 'id': recipe.category.id }))    

        # Checa se uma receita existe
        self.assertEqual(response.status_code, 404)