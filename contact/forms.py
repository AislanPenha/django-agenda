from django import forms
from contact.models import Contact
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    # 1/3: MEXER NO CAMPO
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'classe-a clhumaasse-b',
                'placeholder': 'Aqui veio da raiz'

            }
        ),
        label='Primeiro Nome',
        help_text='Texto de ajuda para seu usuário',
    )

    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accpet': 'image/*'
            }
        ),
        required=False
    )
    # 2/3: MEXER NO CAMPO
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['phone'].widget.attrs.update({
            'class': 'classe-a classe-b',
            'placeholder': 'Aqui veio do init'
        })

    class Meta:
        model = Contact
        fields = (
            'first_name', 'last_name', 'phone',
            'email', 'description', 'category', 'picture'
        )

        # 3/3: MEXER NO CAMPO
        widgets = {
            'last_name': forms.TextInput(
                attrs={
                    'class': 'classe-a classe-b',
                    'placeholder': 'Último Nome'
                }
            )
        }
    
    def clean(self):
        cleaned_data = self.cleaned_data
        print(cleaned_data)

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if first_name == last_name:
            msg = ValidationError('Nome e sobrenome não podem ser iguais', code='invalid')

            self.add_error('first_name', msg)
            self.add_error('last_name', msg)

        # self.add_error(
        #     None,
        #     ValidationError(
        #         'Mensagem de erro none',
        #         code='invalid'
        #     )
        # )
        # self.add_error(
        #     None,
        #     ValidationError(
        #         'Mensagem de erro no none 1',
        #         code='invalid'
        #     )
        # )
        # self.add_error(
        #     'last_name',
        #     ValidationError(
        #         'Mensagem de erro no last 2',
        #         code='invalid'
        #     )
        # )
        return super().clean()
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        print(f'Passsei na clean do {first_name}')

        if first_name == 'ABC':
            # raise ValidationError(
            #         'Não digite ABC neste campo',
            #         code = 'invalid'
            # )   No raise ele já dava o erro no add_error não acumula os erros

            self.add_error(
                'first_name',
                ValidationError(
                    'Não digite ABC neste campo',
                    code='invalid'
                )
            )

        return first_name # retorna exatamente isso no first_name, por isso é bom retornar só o campo first_name
    
    def clean_email(self):
        email_current = self.cleaned_data.get('email')

        if not email_current:
            self.add_error(
                'email',
                ValidationError('Email não pode ser nulo.')
            )
        elif Contact.objects.filter(email=email_current).exists():
            self.add_error(
                'email',
                ValidationError('Email já cadastrado.')
            )
        return email_current
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
        error_messages={
            'required': 'Preencha esse campo.',
            'min_length': 'Aumenta os caracteres aí siow',
        },
        label="Nome"
    )
    last_name = forms.CharField(
        required=True,
        min_length=3,
        error_messages={
            'required': 'Preencha esse campo.',
            'min_length': 'Aumenta os caracteres aí siow',
        },
        label="Sobrenome"
    )
    email = forms.EmailField(
        required=True,
        min_length=3,
        error_messages={
            'required': 'Preencha esse campo.',
            'min_length': 'Aumenta os caracteres aí siow',
        },
        label="Email"
    )
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Já existe este e-mail', code='invalid')
            )

        return email
    
class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Campo  obrigatório.',
        error_messages={
            'min_length': 'Por favor, mais de 2 letras.'
        },
        label="Nome"
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Campo  obrigatório..',
        label="Sobrenome"
    )

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Confirme a senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        password = self.cleaned_data.get('password1')
        user = super().save(commit=False)
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
            
        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_current = self.instance.email
        if email_current != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )
        return password1