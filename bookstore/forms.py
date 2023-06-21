from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from bookstore.models import CustomUser, DeliveryInfo, Book, Author, Category


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'
            field.label_tag(attrs={'style': 'color: #00563FFF;'})


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'role')


class DeliveryInfoForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"
        for field_name, field in self.fields.items():
            field.initial = ''

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'c'
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'ISBN', 'number_of_pages', 'description', 'available_copies', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude=('', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control mb-3'