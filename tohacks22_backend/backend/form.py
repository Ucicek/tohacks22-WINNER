
from django import forms


class ImageForm(forms.Form):
    image_file = forms.ImageField(label='Select an image')