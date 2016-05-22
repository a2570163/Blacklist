#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File: forms.py
# @Author: yan
# @Date:   2016/05/21 11:57
# @Last Modified by:   yan


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _trans


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'id': 'user_login',
                                   'placeholder': 'Username'
                               }),
                               error_messages={
                                   'required': 'Please enter your username'
                               })
    password = forms.CharField(label=_trans("Password"),
                               widget=forms.PasswordInput({
                                   'id': 'user_password',
                                   'placeholder': 'Password'}),
                               error_messages={'required': 'Please enter your password'})


# Type choices for add by manual
TYPE_CHOICES = (
    ('Bounce', 'Bounce'),
    ('Blacklist', 'Blacklist')
)


# Add blacklist by manual
class AddBlacklistFormByManual(forms.Form):
    email = forms.EmailField(max_length=128,
                             widget=forms.EmailInput({
                                 'id': 'blacklist_email',
                                 'placeholder': 'Blacklist email',
                                 'required': True
                             }),
                             error_messages={
                                 'required': 'Blacklist email must not be empty',
                             })
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    user_id = forms.CharField(widget=forms.HiddenInput({'id': 'user_id'}), initial=0)


# Add blacklist by CSV
class AddBlacklistFormByCSV(forms.Form):
    csvfile = forms.FileField(widget=forms.FileInput({'id': 'csvfile_id'}))
    user_id = forms.CharField(widget=forms.HiddenInput({'id': 'user_id'}), initial=0)
