from django import forms
from .models import BlogModel, Choice

class BlogForm(forms.ModelForm):
    choice1 = forms.CharField(label='First Choice',
                                            min_length=2,
                                            max_length=100,
                                            widget=forms.TextInput(attrs={'class':'form-control'}))
    choice2 = forms.CharField(label='Second Choice',
                                            min_length=2,
                                            max_length=100,
                                            widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = BlogModel
        fields = ('text','choice1','choice2')
        widgets = {'text': forms.Textarea(attrs={'class':'form-control','row':10,'col':20})}

class EditBlogForm(forms.ModelForm):

    class Meta:
        model = BlogModel
        fields = ('text',)
        widgets = {'text': forms.Textarea(attrs={'class':'form-control','row':10,'col':20})}

class EditChoiceForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ('choice_text',)
