from .models import Comment, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm





class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'text']





class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter a valid email address.')


    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2'
        ]



class NewsSearchForm(forms.Form):
    search_query = forms.CharField(label='Поиск по заголовку', max_length=100)
