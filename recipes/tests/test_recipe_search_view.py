from django.urls import reverse, resolve
from recipes import views

            # models importa User. Então dá para chamar ele daqui também.
#from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase

                    # RecipeTestBase está herdando de TestCase  (Efeito cascata aqui).
class RecipeSearchViewsTest(RecipeTestBase): 

    # Cehca se a url recipe/search vai chamar/utilizar a view correta.
    def test_recipe_recipe_search_uses_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    # Checa se a resposta da requisição carregar o template search.html
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=teste')

        self.assertTemplateUsed(response, 'recipes/pages/search.html')


    # Verifica se na url do form de busca foi enviado um caracter válido. 
    # Esse teste verifica o envio de um caracter errado para passar.
    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')   # recebe /recipes/search/
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # Testa se o search está no título da página e se está com escape.
    def test_recipe_Search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=Teste'   # recebe /recipes/search/?q=teste
        
        response = self.client.get(url)
            # quando as aspas estão escapadas ele passa no teste        (Protege de XSS)
            # "Teste" = &quot;Teste&quot;
        self.assertIn('Search for &quot;Teste&quot;', response.content.decode('utf-8'))


    # Teste que encontra na busca pelo título
    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug = 'one', title = title1, author_data = { 'username': 'one' }
        )

        recipe2 = self.make_recipe(
            slug = 'two', title = title2, author_data = { 'username': 'two' }
        )
        
        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{ search_url }?q={ title1 }')     # busca pelo título
        response2 = self.client.get(f'{ search_url }?q={ title2 }')     # busca pelo título
        response_both = self.client.get(f'{ search_url }?q=this')       # busca por parte do título
        
        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])