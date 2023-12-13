from django import forms
from django_countries.fields import CountryField
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

from account.models import Customer, Profile, Address, Review
from mptt.forms import TreeNodeChoiceField

import phonenumbers
from phonenumbers import is_valid_number, PhoneNumberFormat


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Full Name"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address line 1"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Address Line 2"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "town/city"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Post Code"}
        )

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):

    name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    mobile = forms.CharField(
        label='phone number',  widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'phone_number'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('name', 'email','mobile')

    def clean_user_name(self):
        name = self.cleaned_data['user_name'].lower()
        r = Customer.objects.filter(name=name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email
    
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        print(f"Mobile number: {mobile}")

        if mobile:
            try:
                default_region = 'IN'
                # Parse the phone number
                parsed_number = phonenumbers.parse(mobile, default_region)
                print(f"Parsed number: {parsed_number}")

                # Check if the parsed phone number is valid
                if not phonenumbers.is_valid_number(parsed_number):
                    raise forms.ValidationError('Invalid phone number.')

                # Check if the phone number is already taken in the database
                if Customer.objects.filter(mobile=mobile).exists():
                    raise forms.ValidationError('This phone number is already taken. Please use another number.')

                # Format the parsed number to its international format
                formatted_number = phonenumbers.format_number(parsed_number, PhoneNumberFormat.INTERNATIONAL)
                print(f"Formatted number: {formatted_number}")

                # Check if the formatted number is at most 13 characters long
                if len(formatted_number) > 15:
                    raise forms.ValidationError('Phone number is too long.')

            except phonenumbers.phonenumberutil.NumberParseException as e:
                raise forms.ValidationError(str(e))       
        
        return mobile


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})
        self.fields['mobile'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Phone number'})  


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

 
    name = forms.CharField(
        label='first name', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'name', 'id': 'form-name'}))
    
    mobile = forms.IntegerField(
        label='phone number',  widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'phone_number', 'id': 'form-mobile'}))
    

    class Meta:
        model = Customer
        fields = ('email', 'name', 'mobile')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['mobile'].required = True





class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['bio','avatar']
        
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '5'})
        }
        

class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset = Review.objects.all())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'}
        )
        self.fields['parent'].label =''
        self.fields['parent'].required = False
        self.fields['rate'].required = False
    class Meta:
        model = Review
        fields = ['content','parent','rate', 'post']
        
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '2', 'placeholder':'Enter your comment...'}),
        }
        
    def save(self, *args, **kwarsgs):
        Review.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwarsgs)
    