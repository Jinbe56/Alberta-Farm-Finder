from django import forms
from .models import Farm, FarmPhoto


SALES_CHANNEL_CHOICES = [
    ('farm_gate', 'Farm Gate Sales'),
    ('u_pick', 'U-Pick'),
    ('delivery', 'Delivery'),
    ('farmers_market', "Farmers' Market"),
    ('online', 'Online Store'),
    ('csa', 'CSA Box'),
]

CERTIFICATION_CHOICES = [
    ('organic', 'Certified Organic'),
    ('grass_fed', 'Grass Fed'),
    ('free_range', 'Free Range'),
    ('pasture_raised', 'Pasture Raised'),
    ('no_spray', 'No Spray'),
    ('non_gmo', 'Non-GMO'),
]

DAY_CHOICES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


class FarmForm(forms.ModelForm):
    sales_channels = forms.MultipleChoiceField(
        choices=SALES_CHANNEL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    certifications = forms.MultipleChoiceField(
        choices=CERTIFICATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Farm
        fields = [
            'name', 'description', 'address_full', 'address_display',
            'categories', 'sales_channels', 'certifications',
            'contact_phone', 'contact_email', 'contact_website',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your farm name'}),
            'description': forms.Textarea(attrs={
                'placeholder': 'Tell people about your farm — what you grow, how you farm, what makes it special...',
                'rows': 5,
            }),
            'address_full': forms.TextInput(attrs={'placeholder': 'Full address (private — used for map placement)'}),
            'address_display': forms.TextInput(attrs={'placeholder': 'e.g. Lacombe, AB (shown publicly)'}),
            'categories': forms.CheckboxSelectMultiple,
            'contact_phone': forms.TextInput(attrs={'placeholder': '(403) 555-0123'}),
            'contact_email': forms.EmailInput(attrs={'placeholder': 'farm@example.com'}),
            'contact_website': forms.URLInput(attrs={'placeholder': 'https://yourfarm.ca'}),
        }


class FarmPhotoForm(forms.ModelForm):
    class Meta:
        model = FarmPhoto
        fields = ['image', 'is_primary']
