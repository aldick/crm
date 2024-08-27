from django import forms

from .models import Client

class ClientCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "phone_number", "name", "address"
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        
        if phone_number[0] == "8":
            phone_number = "+" + phone_number.replace("8", '7', 1)
            
        if len(phone_number) != 12:
            raise forms.ValidationError("Введен неправильный номер")
        
        if Client.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Номер телефона уже использовуется другим клиентом") 
		
        return phone_number
    

class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "phone_number", "name", "address"
        
    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        
        if phone_number[0] == "8":
            phone_number = "+" + phone_number.replace("8", '7', 1)
            
        if len(phone_number) != 12:
            raise forms.ValidationError("Введен неправильный номер")
        
        return phone_number