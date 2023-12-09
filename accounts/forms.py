from django import forms
from .models import Account

#We are creating the model registration form 

class RegistrationForm(forms.ModelForm):
    # creating the field that stores the password and confirm password
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
    }))
    class Meta:
        model = Account #we are using the Account model to create the form 
        fields = ['first_name','last_name','phone_number','email','password']
    
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self). __init__(*args,**kwargs) # calling the constructor of super class
        self.fields['first_name'].widget.attrs['placeholder']='Enter first name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter last name'
        self.fields['email'].widget.attrs['placeholder']='Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter Phone Number'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control' # setting the css class form-control to all the fields
    
    def clean(self): 
        cleaned_data = super(RegistrationForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password: #to check if password and confirm password matches 
            raise forms.ValidationError(
                "password does not match!"
            )
        
