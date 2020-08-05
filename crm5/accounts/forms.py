from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



from .models import *


class ProductForm(ModelForm):
	class Meta:
		model = Product #link to model's Product table
		fields = '__all__' # fill all of the Product 替换['name','price']
		exclude = ['seller','filt_p']
# class CreateUserForm(UserCreationForm):
# 	class Meta:
# 		model = User
# 		fields = ['username', 'email', 'password1', 'password2']

