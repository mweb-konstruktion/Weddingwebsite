from django import forms

MAX_GUESTS = 10


class RSVPForm(forms.Form):
    MEAL_CHOICES = [
        ('', 'Bitte waehlen'),
        ('Fleisch', 'Fleisch'),
        ('Vegetarisch', 'Vegetarisch'),
        ('Fisch', 'Fisch'),
    ]

    name = forms.CharField(
        label='Anmeldende Person',
        max_length=120,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Vor- und Nachname',
                'id': 'id_name',
            }
        ),
    )

    email = forms.EmailField(
        label='E-Mail',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'name@beispiel.ch',
                'id': 'id_email',
            }
        ),
    )

    no_of_guests = forms.ChoiceField(
        label='Anzahl der Gaeste',
        choices=[(str(i), str(i)) for i in range(1, MAX_GUESTS + 1)],
        widget=forms.Select(attrs={'id': 'id_no_of_guests'}),
    )

    message = forms.CharField(
        label='Nachricht',
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'placeholder': 'Moechtet ihr uns noch etwas mitteilen? (optional)',
                'id': 'id_message',
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(1, MAX_GUESTS + 1):
            self.fields[f'guest_name_{i}'] = forms.CharField(
                label='Name',
                max_length=120,
                required=False,
                widget=forms.TextInput(
                    attrs={
                        'placeholder': 'Vor- und Nachname',
                        'class': 'guest-field',
                    }
                ),
            )
            self.fields[f'guest_meal_{i}'] = forms.ChoiceField(
                label='Menuewahl',
                choices=self.MEAL_CHOICES,
                required=False,
                widget=forms.Select(attrs={'class': 'guest-field'}),
            )
            self.fields[f'guest_allergies_{i}'] = forms.CharField(
                label='Allergien / Unvertraeglichkeiten',
                required=False,
                widget=forms.Textarea(
                    attrs={
                        'rows': 2,
                        'placeholder': 'z.B. Laktose, Gluten, Nuesse ...',
                        'class': 'guest-field',
                    }
                ),
            )

    def guest_rows(self):
        return [
            {
                'index': i,
                'name': self[f'guest_name_{i}'],
                'meal': self[f'guest_meal_{i}'],
                'allergies': self[f'guest_allergies_{i}'],
            }
            for i in range(1, MAX_GUESTS + 1)
        ]

    def clean(self):
        cleaned_data = super().clean()
        try:
            no_of_guests = int(cleaned_data.get('no_of_guests') or 0)
        except (TypeError, ValueError):
            no_of_guests = 0

        for i in range(1, MAX_GUESTS + 1):
            name_field = f'guest_name_{i}'
            meal_field = f'guest_meal_{i}'
            allergies_field = f'guest_allergies_{i}'

            if i <= no_of_guests:
                if not cleaned_data.get(name_field):
                    self.add_error(name_field, 'Bitte Namen angeben.')
                if not cleaned_data.get(meal_field):
                    self.add_error(meal_field, 'Bitte ein Menue waehlen.')
            else:
                cleaned_data[name_field] = ''
                cleaned_data[meal_field] = ''
                cleaned_data[allergies_field] = ''

        return cleaned_data
