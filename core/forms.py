from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Listing, Profile, Request

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("role", "phone", "city", "bio")
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ("title", "description", "category", "quantity", "city", "pickup_details")
        widgets = {"description": forms.Textarea(attrs={"rows": 5})}

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ("message",)
        widgets = {"message": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell the donor briefly why you need this item."})}
