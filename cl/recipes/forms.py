from django import forms


class Scale_Recipe(forms.Form):
    servings = forms.DecimalField(decimal_places=2, max_digits=4,
                                  widget=forms.TextInput(attrs={'class': 'input-small',
                                                                'placeholder':'Scale for'}))
