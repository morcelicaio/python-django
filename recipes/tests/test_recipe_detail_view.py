from django.urls import reverse, resolve
from recipes import views

            # models importa User. Então dá para chamar ele daqui também.
#from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase

                    # RecipeTestBase está herdando de TestCase  (Efeito cascata aqui).
class RecipeDetailViewsTest(RecipeTestBase):

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

        # Testa se nosso template category.html exibe o erro 404 p/ receita não publicadas
    def test_recipe_detail_template_dont_loads_recipe_not_published(self):
        """Teste recipe is published False dont show"""
         
        # Cria a receita com  is_published = False
        recipe = self.make_recipe(is_published = False)

        response = self.client.get(reverse('recipes:recipe', kwargs = { 'id': recipe.id }))    

        # Checa se uma receita existe
        self.assertEqual(response.status_code, 404)