# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"用户名",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"密码",
            }
        ),
    )

    def get(self, request):
        return render(request, 'ncrePay/login.html')

    def post(self, request):
        if self.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'ncrePay/login.html', {'errorMsg': u'用户名密码错误'})
        else:
            return render(request, 'ncrePay/login.html', {'errorMsg': u'输入错误'})
