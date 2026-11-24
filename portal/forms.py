from django import forms
from .models import ContactMessage, Subscriber, Article


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'subject': forms.TextInput(attrs={'placeholder': 'What is it about?'}),
            'message': forms.Textarea(attrs={'placeholder': 'Write your message...', 'rows': 5}),
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        }


class ArticleForm(forms.ModelForm):
    """Form logged-in users fill in to submit a new article."""
    class Meta:
        model = Article
        fields = ['title', 'category', 'region', 'summary', 'content', 'source', 'source_url']
        labels = {
            'source': 'Source (the research your article is based on)',
            'source_url': 'Source link',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. How Seals Survive Under the Ice'}),
            'source': forms.TextInput(attrs={'placeholder': 'Author(s) (Year). Title of paper. Journal name.'}),
            'source_url': forms.URLInput(attrs={'placeholder': 'https://doi.org/...'}),
            'summary': forms.TextInput(attrs={'placeholder': 'One or two lines about your article'}),
            'content': forms.Textarea(attrs={'rows': 12, 'placeholder': 'Write your article here. Leave an empty line between paragraphs.'}),
        }
