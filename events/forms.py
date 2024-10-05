# events/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # 添加邮箱字段

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # 定义表单字段
