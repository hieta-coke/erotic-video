from django import forms
from django.core.mail import send_mail
from django.conf import settings

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

    def send_mail(self):
        name = self.cleaned_data["name"]
        email = self.cleaned_data["email"]
        subject = self.cleaned_data["subject"]
        content = self.cleaned_data["content"]
        to = "escape3new@icloud.com"

        send_mail(
            subject=subject,
            message="名前:" + name + "Email:" + email + "内容:" + content,
            from_email=email,
            recipient_list = [
                to,
            ]
        )