from django import forms
from django.forms import ModelForm
from .models import Topic, Project, Reply

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['topic_id', 'title', 'text']

    # def save(self, commit=True):
    #     user = super(UserCreationForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #     return user

    # class FooMultipleChoiceForm(forms.Form):
    #     foo_select = forms.ModelMultipleChoiceField(queryset=None)

    #     def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         self.fields['foo_select'].queryset = ...