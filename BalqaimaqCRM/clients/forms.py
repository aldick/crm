from django import forms

from .models import Client


class ClientLoginForm(forms.Form):
    username = forms.CharField(label="Номер телефона")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        
        if username[0] == "+":
            username = username.replace("+", '', 1)
        
        elif username[0] == "8":
            username = username.replace("8", '7', 1)
            
        if len(username) != 11:
            raise forms.ValidationError("Введен неправильный номер")
		
        return username

class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "phone_number", "name", "address"
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        
        if phone_number[0] == "+":
            phone_number = phone_number.replace("+", '', 1)
        
        elif phone_number[0] == "8":
            phone_number = phone_number.replace("8", '7', 1)
            
        if len(phone_number) != 11:
            raise forms.ValidationError("Введен неправильный номер")
        
        if Client.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Номер телефона уже использовуется другим клиентом") 
		
        return phone_number
    
class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "name", "address"
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        
        if phone_number[0] == "+":
            phone_number = phone_number.replace("+", '', 1)
        
        elif phone_number[0] == "8":
            phone_number = phone_number.replace("8", '7', 1)
            
        if len(phone_number) != 11:
            raise forms.ValidationError("Введен неправильный номер")
		
        return phone_number
    
class ClientSelectForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = 'phone_number',
