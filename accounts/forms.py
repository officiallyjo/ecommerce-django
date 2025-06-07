from django import forms
from .models import Account



class RegistrationForm(forms.ModelForm):
    
    # password = forms.CharField(widget=forms.PasswordInput(attrs={
    #     'placeholder': 'Enter Password',
    #     'class': 'form-control',
    #     'required': True,
    # })) this how to add bootstrap class to each form but it would make the work bulky


    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
        'required': True,
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm Password',
    }))

    class Meta:
        model =Account
        fields = ['first_name', 'last_name', 'phone_number','email', 'password']


    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
       
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean() # the super() method is called to change the cleaned data before returning it back to the caller . it simply changes the way the data is being saved 
        password = cleaned_data.get('password')
        confirm_password =cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
                ) # raises a ValidationError if the password and confirm_password do not match
        return cleaned_data
    
    # def clean(self):
    #     cleaned_data = super(RegistrationForm, self).clean()
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get('confirm_password')
        
    #     if password and confirm_password and password != confirm_password:
    #         raise forms.ValidationError("Passwords do not match")
        
    #     return cleaned_data
