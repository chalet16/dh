from django import forms

TO_CHOICES = (
    ('web', 'Webmaster'),
    ('cooking', 'Cooking Steward'),
    ('cleaning', 'Cleaning Steward'),
)


class ContactForm(forms.Form):
    who = forms.ChoiceField(choices=TO_CHOICES)
    topic = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea())
    sender = forms.EmailField(required=False)
