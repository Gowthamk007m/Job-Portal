from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from jobs.models import Job
from .models import *
from django.core.validators import MinLengthValidator
from django.forms import EmailInput, Select, CheckboxInput,CharField
from django.forms import TextInput, PasswordInput, Textarea, FileInput, DateInput
from .validators import validate_video_file
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from django_select2.forms import Select2Widget

def validate_age(dob):
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age < 18:
        raise ValidationError('You must be at least 18 years old.')


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleImageField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

    def to_python(self, data):
        if data in self.empty_values:
            return None

        if isinstance(data, list):
            return [self.check_and_store_image(d) for d in data]
        else:
            return self.check_and_store_image(data)

    def check_and_store_image(self, data):
        file = super().to_python(data)
        if file is None:
            return None
        if not file.content_type.startswith('image'):
            raise ValidationError(_('File type is not supported.'), code='invalid')
        return file

    
    
# user registration
class UserRegistrationForm(forms.ModelForm):
    confirm_password = CharField(
        max_length = 25,
        min_length = 8,
        required = True,
        validators = [
            MinLengthValidator(8, 'The password is too short.')
        ],
        widget = PasswordInput({
            'class': 'form-control'
        }),
        label='Confirm Password'
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'phone',
        ]
        
        widgets = {
            'username': TextInput({
                'class': 'form-control',
            }),

            'email': EmailInput({
                'class': 'form-control'
            }),
            
            'first_name': TextInput({
                'class': 'form-control',
                'autocomplete': 'first_name'
            }),

            'last_name': TextInput({
                'class': 'form-control'
            }),
            
            'password': PasswordInput({
                'class': 'form-control'
            }),

            'phone': TextInput({
                'class': 'form-control',
                'minlength': '10',
                'maxlength': '10' 
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please enter the same password in both fields.")

        return cleaned_data
    

# Profile Add
class UserDetailAddForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'profile_photo',
            'dob',
            'qualification',
            'smoking_habit',
            'drinking_habit',
            'short_reel'
        ]

        widgets = {
            'dob': DateInput({
                'class': 'form-control',
                'type': 'date'
            }),
            'qualification': Select({
                'class': 'form-control'
            }),
            'smoking_habit': Select({
                'class': 'form-control'
            }),

            'drinking_habit': Select({
                'class': 'form-control'
            }),
            'profile_photo': FileInput({
                'class': 'form-control'
            }),

            'short_reel': FileInput({
                'class': 'form-control',
                'accept': 'video/mp4, video/avi, video/mkv, video/mov, video/wmv'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field_instance in self.fields.items():
            field_instance.required = True
    
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        validate_age(dob)
        return dob
   
    def clean_short_reel(self):
        short_reel = self.cleaned_data.get('short_reel', False)
        if not short_reel:
            raise forms.ValidationError("No file chosen!")

        validate_video_file(short_reel)
        return short_reel


class UserImageForm(forms.ModelForm):
    image = MultipleImageField(label='Image Files')

    class Meta:
        model = UserImages
        fields = ['image']
        widgets = {
            'image': MultipleImageInput(attrs={'class': 'form-control', 'multiple': True,'accept': 'image/*'}),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance


             

# user login
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        max_length=254
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    

# Forgot Password Email Form 
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        })
    )
    

# Reset Password Form
class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        label='New Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        label='Confirm Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match")

        return cleaned_data


# Profile Update
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'profile_photo',
            'dob',
            'qualification',
            'smoking_habit',
            'drinking_habit',
            'short_reel'
        ]

        widgets = {
            'username': TextInput({
                'class': 'form-control'
            }),

            'email': EmailInput({
                'class': 'form-control'
            }),
            
            'first_name': TextInput({
                'class': 'form-control'
            }),

            'last_name': TextInput({
                'class': 'form-control'
            }),

            'phone': TextInput({
                'class': 'form-control'
            }),

            'dob': DateInput({
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),

            'qualification': Select({
                'class': 'form-control'
            }),

            'smoking_habit': Select({
                'class': 'form-control'
            }),

            'drinking_habit': Select({
                'class': 'form-control'
            }),

            'profile_photo': FileInput({
                'class': 'form-control'
            }),

            'short_reel': FileInput({
                'class': 'form-control',
                'accept': 'video/mp4, video/avi, video/mkv, video/mov, video/wmv'
            })
        }
    def clean_short_reel(self):
        short_reel = self.cleaned_data.get('short_reel', False)
        if not short_reel:
            raise forms.ValidationError("No file chosen!")

        validate_video_file(short_reel)
        return short_reel
    
    
# Change Password
class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter old password'})
    )
    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'})
    )
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'})
    )

    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']


# Address
class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user']
        widgets = {
            'name': TextInput({
                'class': 'form-control',
                'autocomplete': 'name'
            }),

            'address_line_1': TextInput({
                'class': 'form-control',
                'autocomplete': 'address_line_1'
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


# Experience
class ExperienceUpsertForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ['user']
        widgets = {
            'title': TextInput({
                'class': 'form-control',
                'autocomplete': 'title'
            }),

            'company': TextInput({
                'class': 'form-control',
                'autocomplete': 'company'
            }),

            'location': TextInput({
                'class': 'form-control'
            }),

            'description': Textarea({
                'class': 'form-control',
                'rows':'4'
            }),

            'start_date': DateInput({
                'class': 'form-control',
                'type': 'date'
            }),

            'end_date': DateInput({
                'class': 'form-control',
                'required':False,
                'type': 'date'
            }),
        }


# Education
class EducationUpsertForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ['user']
        widgets = {
            'institution': TextInput({
                'class' : 'form-control',
            }),

            'degree': Select({
                'class': 'form-control',
            }),

            'field_of_study': TextInput({
                'class': 'form-control',
            }),

            'start_date': DateInput({
                'class': 'form-control',
                'type': 'date',
            }),

            'end_date': DateInput({
                'class': 'form-control',
                'required':False,
                'type': 'date'
            }),
        }    


# UserSkill
class UserSkillUpsertForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        exclude = ['user']
        widgets = {
            'skill': Select({
                'class' : 'form-control',
                'autocomplete': 'skill',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        


class UserHobbyForm(forms.ModelForm):
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = UserHobby
        fields = []

class UserInterestForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = UserInterest
        fields = []


class ImageForm(forms.ModelForm):
    
    class Meta:
        model = UserImages
        fields = ['image']
        
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'required':True}),
        }
        
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if not image:
            raise forms.ValidationError("File is required.")
        return image


 
# Jobs
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['job_title', 'job_description', 'salary_from', 'salary_to', 'location', 'expected_joining_date']
        
        widgets = {
            'job_title': Select2Widget(attrs={'class': 'form-control', 'placeholder': 'Enter job title', 'required':True}),
            'job_description': TinyMCE(attrs={'cols': 80, 'rows': 50}),
            'location': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter job location', 'required':True}),
            'expected_joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Enter expected joining date', 'required':True}),
            'salary_from': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter job salary', 'required':True}),
            'salary_to': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter job salary', 'required':False})
        }
        

class UserHobbyAddForm(forms.ModelForm):
    class Meta:
        model = UserHobby
        fields = ['hobby']
        
        widgets = {
            'hobby': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter hobby', 'required':True}),
        }
        

class UserInterestAddForm(forms.ModelForm):
    class Meta:
        model = UserInterest
        fields = ['interest']
        
        widgets = {
            'interest': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter interest', 'required':True}),
        }