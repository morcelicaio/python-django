from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()
    
    
    def make_recipe_no_defaults(self):
        recipe = Recipe(
        category = self.make_category(name = 'Test default Category'),
        author = self.make_author(username = 'newuser'),
        title = 'Recipe Title',
        description = 'Recipe Description',
        slug = 'recipe-slug',
        preparation_time = 10,
        preparation_time_unit = 'Minutos',
        servings = 5,
        servings_unit = 'Porções',
        preparation_step = 'Recipe Preparation Steps',
    )

        recipe.full_clean()
        recipe.save()
        return recipe 

    # Teste que checa se vai ser lançada uma exceção se o usuário inserir um title com + de xx caracs
    # Faz um for para testar o lenght para cada atributo (para não ficar repetindo código fazendo 
    # vários testes só mudando o nome do atributo)
    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_length(self, field, max_length):                    
        setattr(self.recipe, field, 'A' * (max_length + 1))
       
        # assertRaises precisa estar no contextManager para poder funcionar.
        with self.assertRaises(ValidationError):
            # Aqui a validação do django ocorre p ñ deixar passar de xx caracteres o title (ValidatiorError)
            self.recipe.full_clean()            

    
    def test_recipe_preparation_step_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
                
        self.assertFalse(recipe.preparation_step_is_html,
                         msg = 'Recipe preparation_step_is_html is not False - caio')
        
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
                
        self.assertFalse(recipe.is_published,
                         msg = 'Recipe is_published is not False - caio')


