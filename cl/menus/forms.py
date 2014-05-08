from django import newforms as forms


class lateplates(forms.Form):
    servings = forms.DecimalField(decimal_places=2, max_digits=4,
                                  widget=forms.TextInput(attrs={'size': '5'}))
