from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from django.core import validators
from django.core.validators import MaxLengthValidator
 

class RegisterForm(UserCreationForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Enter Full Name'}))
    user_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' Enter UserName'}))
    matric_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matric Number*'}))
    email = forms.EmailField( widget=forms.EmailInput( attrs={'class': 'form-control', 'placeholder': 'aa@gmail.com'}))
    gender = forms.ChoiceField(choices=CustomUser.GENDER_OPTIONS,widget=forms.Select(attrs={'class': 'form-control'}))
    department = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department*'}))
    password1 = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField( widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            message = "Passwords do not match"
            raise forms.ValidationError(message)

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            message = "Please enter your email address"
            raise forms.ValidationError(message)

        return email

    class Meta:
        model = CustomUser
        fields = ['name', 'user_name', 'matric_number', 'email', 'gender', 'department', 'password1', 'password2']

        
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter Old Password'}))
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter New  Password'}))
    new_password2= forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Confirm New Password'}))
    botfield = forms.CharField(required=False, widget=forms.HiddenInput(),
                               validators=[validators.MaxLengthValidator(0)])

    class Meta():
        model = User
        fields = ['password1', 'password2']

class EditUserForm(UserChangeForm):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Enter Name'}))
    matric_number = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder':'Matric Number'}))
    
   
    class Meta:
        model = CustomUser
        fields = ('name', 'matric_number', 'gender', 'department')  


class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = ['borrowed_date', 'returned_date','reason_for_borrowing']  

    def __init__(self, *args, **kwargs):
        super(BorrowingForm, self).__init__(*args, **kwargs)
        # Customize form fields here if needed
        self.fields['borrowed_date'].widget = forms.DateInput(attrs={'type': 'date','class': 'form-control',})  # Example: Change widget to date input
        self.fields['returned_date'].widget = forms.DateInput(attrs={'type': 'date','class': 'form-control',})  # Example: Change widget to date input