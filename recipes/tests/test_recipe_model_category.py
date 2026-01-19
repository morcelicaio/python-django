from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class RecipeCategoryModelTest(RecipeTestBase):
    
    def setUp(self):
        self.category = self.make_category(name = 'Category Testing')
        return super().setUp()
    
    def test_recipe_category_model_String_representation_is_name_field(self):
        self.assertEqual(str(self.category), self.category.name, msg = 'Precisa ter o mesmo name') 

    # Teste que (vai passar) levanta a exceção se houver mais de 65 caracteres.
    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
