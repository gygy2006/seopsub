from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models

GENDER_CHOICE = (("MALE", "남자"), ("FEMALE", "여자"))


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is Wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User

        fields = ("first_name", "email")

        widgets = {
            "first_name": forms.TextInput(
                attrs={"placeholder": "First Name", "class": "signup_input"}
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email",
                    "required": "True",
                    "class": "signup_input",
                }
            ),
        }

    # first_name = forms.CharField(
    #     widget=forms.TextInput(attrs={"placeholder": "First Name"})
    # )
    # last_name = forms.CharField(
    #     widget=forms.TextInput(attrs={"placeholder": "Last Name"})
    # )
    # email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "signup_input"}
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Confirm Password", "class": "signup_input"}
        )
    )
    gender = forms.ChoiceField(
        label="Gender",
        widget=forms.Select(attrs={"class": "signup_input"}),
        choices=GENDER_CHOICE,
    )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        print(email)
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                " That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        print(password, password1)
        if password != password1:
            raise forms.ValidationError("Password confirmation does not math")
        else:
            return password

    def save(self, *args, **kwargs):
        user = super().save(commit=True)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        first_name = self.cleaned_data.get("first_name")
        user.username = email
        user.last_name = first_name[1:]
        user.set_password(password)
        user.save()
