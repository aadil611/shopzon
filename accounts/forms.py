from .models import Account,UserProfile
from django import forms
from django.contrib import messages


class RegistrationForm(forms.ModelForm):

  class Meta:
    model = Account
    fields = ['first_name','last_name','email','phone_number','password']

  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data['password']
    confirm_password = self.data.get('confirm_password')
    if password != confirm_password:
      self.add_error('password','password does not match')


class UserForm(forms.ModelForm):
  class Meta:
    model = Account
    fields = ['first_name', 'last_name','phone_number']


class UserProfileForm(forms.ModelForm):
  class Meta:
    model = UserProfile
    fields = ['profile_picture','address','country','state','city']