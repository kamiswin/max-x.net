#encoding:utf-8
__author__ = 'seraph'
from django import forms
from models import UserProfile

class RegisterForm(forms.Form):
    username = forms.EmailField(label='信箱',help_text='请填写您的email')
    screen_name = forms.CharField(label='昵称',required=True,max_length=20,min_length=3,help_text='请正确填写')
    password = forms.CharField(label='密码',required=True,max_length=20,min_length=6,help_text='密码',widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.EmailField(label='信箱',required=True,max_length=30,min_length=3)
    password = forms.CharField(label='密码',required=True,max_length=128,min_length=6,
                               widget=forms.PasswordInput(),help_text='')