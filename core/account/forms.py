from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User=get_user_model()

class RegisterUserForm(forms.ModelForm):
    password1=forms.CharField(label='رمزعبور',widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور','required':'required','class':'form-control'}))
    password2=forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput(attrs={'placeholder':'تکرار رمز عبور','required':'required','class':'form-control'}))

    class Meta:
        model=User
        fields=["email","password1","password2"]
        widgets={
            'email':forms.EmailInput(attrs={
                'placeholder':'ایمیل خود را وارد کنید',
                'required':'required',
                'class':'form-control',
                
            })
        }
        labels={
            'email':'ایمیل'
        }

    def clean(self):
        cleaned_data=super().clean()
        password1=cleaned_data.get("password1")
        password2=cleaned_data.get("password2")

        if password1!=password2:
            raise forms.ValidationError("رمز عبور و تکرار آن یکی نیستند!")
        
        return cleaned_data
    
    def save(self, commit = True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    email=forms.EmailField(label='ایمیل',widget=forms.EmailInput(attrs={'placeholder':'ایمیل خود را وارد کنید','required':'required','class':'form-control'}))
    password=forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور خود را وارد کنید','required':'required','class':'form-control'}))
    
    def __init__(self,*args,**kwargs):
        self.request=kwargs.pop('request',None)
        super().__init__(*args,**kwargs)

    def clean(self):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        user=authenticate(email=email,password=password)
        if user is None:
            raise forms.ValidationError('چنین کاربری وجود ندارد')
        
        self.user=user
        return self.cleaned_data
    
    def get_user(self):
        return self.user
