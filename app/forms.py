from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import Booking, Event, Profile, SellerApplication, AvailableDate
from django.utils import timezone


class SignUpForm(UserCreationForm):

    phone_no = forms.CharField( required=True, label="Phone Number")

    class Meta:

        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_no')

        def clean_password1(self):
            password1 = self.cleaned_data.get('password1')
            validate_password(password1)
            return password1
        

        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')

            if password1 and password2 and password1 != password2:
                raise ValidationError("Passwords don't match")
            return password2
        
        def save(self, commit=True):
            user = super().save(commit=False)
            user.is_seller = self.cleaned_data["is_seller"]

            if commit:
                user.save()
                Profile.objects.update_or_create(user=user, defaults={
                    'phone_no': self.cleaned_data['phone_no'],
                    'is_seller': self.cleaned_data['is_seller']
                })
            return user
        
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name','image', 'description','category', 'price', 'location', ]

class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = Profile
        fields = ['profile_picture','first_name','last_name', 'phone_no']


class SellerUpgradeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_seller']



class SellerApplicationForm(forms.ModelForm):
    class Meta:
        model = SellerApplication
        fields = ['business_name', 'registration_number', 'tax_id', 'address', 'contact_number', 'documents']

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['participants', 'selected_date']

    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        if event:
            self.fields['selected_date'].queryset = AvailableDate.objects.filter(event=event, date__gte=timezone.now().date())

class OTPForm(forms.Form):
    otp_code = forms.CharField(label="Enter OTP", max_length=6)