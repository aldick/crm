from django import forms

from .models import Client, Worker


class ClientLoginForm(forms.Form):
    username = forms.CharField(label="Номер телефона")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput, max_length=11)
    
    def clean_username(self):
        username = self.cleaned_data["username"]
        
        if username[0] == "+":
            username = username.replace("+", '', 1)
        
        elif username[0] == "8":
            username = username.replace("8", '7', 1)
		
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
        
class WorkerCreateForm(forms.ModelForm):
    class Meta:
        model = Worker
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
            raise forms.ValidationError("Номер телефона уже использовуется другим рабочим") 
		
        return phone_number
    
class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
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
