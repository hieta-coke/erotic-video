from django import forms

class SearchForm(forms.Form):
    squeeze = forms.CharField(required=True)

class CommentForm(forms.Form):
    name = forms.CharField(max_length=50, initial="名無し")
    comment = forms.CharField(required=True, widget=forms.Textarea())

class ContactForm(forms.Form):
    name = forms.CharField(label="お名前", required=True)
    email = forms.CharField(label="Email", required=True)
    subject = forms.CharField(label="件名", required=True)
    content = forms.CharField(label="内容", required=True, widget=forms.Textarea())