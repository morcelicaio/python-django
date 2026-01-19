from unittest import TestCase
from django.test import TestCase as DjangoTesteCase   
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Type your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        # Pega o form
        form = RegisterForm() 

        # Recupera o atributo placeholder do campo escolhido no form
        curent_placeholder = form[field].field.widget.attrs['placeholder']

        # Realiza o teste para ver se o placeholder está correto
        self.assertEqual(curent_placeholder, placeholder)

    
    @parameterized.expand([
        ('username', ('Username must have letters, numbers or one of those @/./+/-/_. The length should be between 4 and 50 characters.')),
        ('email', 'The e-mail must be valid.'),
        ('password', 
            ('Password must have at least one uppercase letter, '
                'one lowercase letter and one number. The length should be '
                'at least 8 characters.'
            )
        ),
    ])
    def test_fields_help_text(self, field, needed):
        # Pega o form
        form = RegisterForm() 

        # Recupera o atributo help_text do campo escolhido no form
        curent = form[field].field.help_text

        # Realiza o teste para ver se o hekp_text está correto
        self.assertEqual(curent, needed)


    @parameterized.expand([
        ('username', ('Username')),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Digite sua senha'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        # Pega o form
        form = RegisterForm() 

        # Recupera o atributo label do campo escolhido no form
        curent = form[field].field.label

        # Realiza o teste para ver se o label está correto
        self.assertEqual(curent, needed)


# Esse teste de integração integra view, form, template....Tudo em um lugar só.
class AuthorRegisterFormIntegrationTest(DjangoTesteCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }

        return super().setUp(*args, **kwargs)
    
    # Nesse teste, nenhum dos campos pode estar vazio. Se estiver vazio o teste falha.
    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat your password'),
        ('email', 'E-mail is required.'),
        
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''      # para testar se o campo é vazio,  atribuimos vazio para o campo.

        url = reverse('authors:register_create')

        #                      fazemos o post enviando o form_data
        response = self.client.post(url, data = self.form_data, follow = True)
        self.assertIn(msg, response.content.decode('utf-8'))


    # Testa se o comprimento mínimo digitado no campo é 4. Se for menos passa nesse teste de validação.
    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'

        url = reverse('authors:register_create')        

        #                      fazemos o post enviando o form_data
        response = self.client.post(url, data = self.form_data, follow = True)
        
        msg = 'Username must have at least 4 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))


    # Testa se o comprimento máximo digitado no campo é 150. Se for mais passa nesse teste de validação.
    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151 

        url = reverse('authors:register_create')        

        #                      fazemos o post enviando o form_data
        response = self.client.post(url, data = self.form_data, follow = True)
        
        msg = 'Username must have less than 151 characters'
        
        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))


    # Verifica se a senha é forte.  1o passa no teste se a senha for fraca.  depois passa no teste se senha for forte
    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'

        url = reverse('authors:register_create')        

        #                      fazemos o post enviando o form_data
        response = self.client.post(url, data = self.form_data, follow = True)
        
        msg = ('Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.')
        
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))


        # caso inverso de senha correta
        self.form_data['password'] = '@A123abc123'

        url = reverse('authors:register_create')        

        #                      fazemos o post enviando o form_data
        response = self.client.post(url, data = self.form_data, follow = True)
        
        self.assertNotIn(msg, response.context['form'].errors.get('password'))



    # Verifica se a senha e a confirmacao de senha são diferentes e depois se sao iguais
    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123xxx'

        url = reverse('authors:register_create')        

        #                      fazemos o post enviando o form_data
        response = self.client.post(url, data = self.form_data, follow = True)
        
        msg = 'Password and password2 must be equal'
        
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))


        self.form_data['password'] = '@A123abc123'
        self.form_data['password2'] = '@A123abc123'

        url = reverse('authors:register_create')        

        #                      fazemos o post enviando o form_data
        response = self.client.post(url, data = self.form_data, follow = True)
                                
        self.assertNotIn(msg, response.content.decode('utf-8'))
      
    # se enviar requisicao get deve retornar 404
    def test_send_get_request_to_registation_create_vew_returns_404(self):                
        url = reverse('authors:register_create')        
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    
    # Teste de e-mail único
    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')

        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'User e-mail is already in use'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    # Verifica se o usuário pode logar
    def test_author_created_can_login(self):
        url = reverse('authors:register_create')                

        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password2': '@Bc123456',
        })

        # O Django Test Client simula um navegador e faz um POST para /authors/register/create/
        # A view register_create é executada. Dentro da view: o RegisterForm é instanciado, o formulário é validado
        # o usuário é salvo no banco (User.objects.create_user(...))
        self.client.post(url, data = self.form_data, follow = True)

        is_authenticated = self.client.login(
            username = 'testuser',
            password = '@Bc123456',
        )

        self.assertTrue(is_authenticated)