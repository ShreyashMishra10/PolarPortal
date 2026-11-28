from django import forms
from .models import ContactMessage, Subscriber, Article, MediaItem


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
        fields = ['title', 'category', 'region', 'image', 'summary', 'content', 'source', 'source_url']
        labels = {
            'image': 'Cover image (optional)',
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


class MediaForm(forms.ModelForm):
    """Form logged-in users fill in to share a photo, video, podcast or document."""
    class Meta:
        model = MediaItem
        fields = ['title', 'media_type', 'region', 'file', 'link', 'description']
        labels = {
            'media_type': 'Type',
            'file': 'Upload a file (photo, MP4 video or PDF)',
            'link': 'Or paste a link (YouTube video or website)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Penguins at Bharati Station'}),
            'link': forms.URLInput(attrs={'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'What does it show? Who made it?'}),
        }

    def clean(self):
        # the user must give at least a file or a link
        data = super().clean()
        if not data.get('file') and not data.get('link'):
            raise forms.ValidationError('Please upload a file or paste a link.')
        return data

    def clean_file(self):
        # keep uploads small so the free hosting space does not fill up
        file = self.cleaned_data.get('file')
        if file and file.size > 20 * 1024 * 1024:
            raise forms.ValidationError('The file is too big. Please keep it under 20 MB.')
        return file
