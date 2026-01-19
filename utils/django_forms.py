import re

from django.core.exceptions import ValidationError

def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


# Recebe qual campo do meu form quero alterar, recebe qual atributo quero add, recebe o novo valor do atributo
def add_placeholder(field, placeholder_val):    
    add_attr(field, 'placeholder', placeholder_val)


def strong_passowrd(password):
    # Usando os validators do django
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')    # regex que valida a senha

    if not regex.match(password):
        raise ValidationError(
            ('Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'),

            code = 'invalid'
        )