from django.forms import CharField, ClearableFileInput, DateInput, ModelForm, PasswordInput, TextInput, Form, Select, CheckboxInput, Textarea, ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control mt-4'}),)
    password2 = forms.CharField(label=("Password confirmation"),
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Confirm Password', 'class': 'form-control mt-4'}),
                                help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = CustomUser
        fields = ("email",)

        widgets = {
            'email': TextInput({
                'class': 'form-control mt-4',
                'type': 'email',
                'id': 'Email1',
                'aria-describedby': 'emailHelp',
                'placeholder': 'Enter email',
                'required': 'required'
            })}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class LoginForm(Form):
    email = CharField(
        max_length=50,
        min_length=10,
        required=True,
        label='email',
        widget=TextInput({
            'class': 'form-control mt-4',
            'type': 'email',
            'id': 'Email1',
            'aria-describedby': 'emailHelp',
            'placeholder': 'Enter email',
            'required': 'required'
        })
    )

    password = CharField(
        max_length=15,
        min_length=4,
        required=True,
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control mt-4'}),)


class DetailsForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone',
                  'dob', 'gender', 'country', 'profile_photo']
        
        widgets = {
            'first_name': TextInput(attrs={
                'class': 'form-control ',
                'required': 'required'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control ',
            }),
            'phone': TextInput(attrs={
                'class': 'form-control ',
                'required': 'required'
            }),
            'dob': DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }),
            'gender': Select(attrs={
                'class': 'form-control ',
                'required': 'required'
            }),
            'country': Select(attrs={
                'class': 'form-control select2',
                'required': 'required'
            }),
            'profile_photo': ClearableFileInput(attrs={
                'class': 'form-control',
            })
        }
        
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        today = date.today()
        age_limit = 16
        if dob:
            age = (today - dob).days // 365
            if age < age_limit:
                raise ValidationError(
                    f'You must be at least {age_limit} years old.')
        return dob


class AddressCreateForm(ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        widgets = {
            'name': TextInput({
                'class': 'form-control'
            }),

            'address_line_1': TextInput({
                'class': 'form-control'
            }),

            'address_line_2': TextInput({
                'class': 'form-control'
            }),

            'address_line_3': TextInput({
                'class': 'form-control'
            }),

            'city': TextInput({
                'class': 'form-control'
            }),

            'state': TextInput({
                'class': 'form-control'
            }),

            'pincode': TextInput({
                'class': 'form-control'
            }),

            'country': Select({
                'class': 'form-control'
            }),

            'phone': TextInput({
                'class': 'form-control'
            }),

            'is_default': CheckboxInput(),
        }


class ActivitiesForm(ModelForm):
    class Meta:
        model = UserActivity
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hobbies'].widget.attrs.update({'class': 'col-8'})
        self.fields['Interest'].widget.attrs.update({'class': 'col-8'})
        self.fields['smoking_habit'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['drinking_habit'].widget.attrs.update({'class': 'form-check-input'})


class QualificationsForm(ModelForm):
    class Meta:
        model = UserQualifications
        exclude = ["user"]

        widgets = {
            'level': Select({
                'class': 'form-control',
                'required': 'required'
            }),

            'start_date': DateInput({
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }),

            'end_date': DateInput({
                'class': 'form-control',
                'type': 'date',
                'required': 'required'
            }),

            'course': TextInput({
                'class': 'form-control',
                'required': 'required'
            }),
            'institution': TextInput({
                'class': 'form-control',
                'required': 'required'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    "Start date must be earlier than end date.")
        return cleaned_data
