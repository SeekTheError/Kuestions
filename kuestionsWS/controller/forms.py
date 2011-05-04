from django import forms 

class ImageUploadForm(forms.Form):
    picture = forms.FileField()