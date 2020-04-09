from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div
from django.forms import ModelForm
from .models import Profile
from .models import Track


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('image', )


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id_register_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Div(
                Div(
                    Div('first_name', css_class="form-group"),
                    Div('last_name', css_class="form-group"),
                    Div('username', css_class="form-group"),
                    Div('email', css_class="form-group"),
                    css_class='col-md-6'),
                Div(
                    Div('password1', css_class="form-group"),
                    Div('password2', css_class="form-group"),
                    css_class='col-md-6'),
                css_class='row'
            )
        )


class SongForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ('track_title', 'Artist_name', 'song')

