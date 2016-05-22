# -*- coding: utf-8 -*-
# @File: forms.py
# @Author: yan
# @Date:   2016/05/21 11:57
# @Last Modified by:   yan


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _trans


class LoginForm(AuthenticationForm):
    """
    This class works for the login page.
    In this class, we can configure our login form.
    """
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


# Type choices for add by manual form
TYPE_CHOICES = (
    ('Bounce', 'Bounce'),
    ('Blacklist', 'Blacklist')
)


# Add blacklist by manual form
class AddBlacklistFormByManual(forms.Form):
    """
    This class works for the edit page.
    In this class, we can configure our 'AddBlacklistFormByManual' form.
    That contains 3 fields: email, type and user_id,
                    - email and type is filled by users.
                    - user_id will be automatically taken, according to the login account
    """
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
    """
    This class works for the edit page.
    In this class, we can configure our 'AddBlacklistFormByCSV' form.
    That contains 2 fields: csv file and user_id,
                    - the csv file should be 'email,type', and selected by users
                    - user_id will be automatically taken, according to the login account
    """
    csvfile = forms.FileField(widget=forms.FileInput({'id': 'csvfile_id'}))
    user_id = forms.CharField(widget=forms.HiddenInput({'id': 'user_id'}), initial=0)
