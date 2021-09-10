from django import forms


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=11,required=True)
    message = forms.CharField(widget=forms.Textarea)

