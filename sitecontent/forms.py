from django import forms

MAX_GUESTS = 10
MAX_CHILDREN = 6


class RSVPForm(forms.Form):
    # Menü-Auswahl für Erwachsene.
    # ('Wert', 'Anzeige DE', 'Anzeige IT') – die dritte Spalte wird nur für die
    # zweisprachige Anzeige des Platzhalters verwendet (siehe MEAL_CHOICES unten).
    MEAL_CHOICES = [
        ('', 'Bitte wählen'),
        ('Fleisch', 'Fleisch'),
        ('Vegetarisch', 'Vegetarisch'),
        ('Fisch', 'Fisch'),
    ]

    # Zusätzliches Menü für Kinder (Anforderung 1).
    # Enthält ein eigenes "Kindermenü" sowie die Standardoptionen.
    CHILD_MEAL_CHOICES = [
        ('', 'Bitte wählen'),
        ('Kindermenü', 'Kindermenü'),
        ('Vegetarisch', 'Vegetarisch'),
        ('Fleisch', 'Fleisch'),
        ('Fisch', 'Fisch'),
    ]

    # Zweisprachige Texte für die leere Auswahl-Option ("Bitte wählen").
    # Werden per data-empty-* Attribut ins <select> geschrieben, damit nav.js
    # die Option-Beschriftung beim Sprachwechsel aktualisieren kann.
    SELECT_EMPTY_DE = 'Bitte wählen'
    SELECT_EMPTY_IT = 'Selezionare'

    name = forms.CharField(
        label='Anmeldende Person',
        max_length=120,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Vor- und Nachname',
                'data-placeholder-de': 'Vor- und Nachname',
                'data-placeholder-it': 'Nome e cognome',
                'id': 'id_name',
            }
        ),
    )

    email = forms.EmailField(
        label='E-Mail',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'name@beispiel.ch',
                'data-placeholder-de': 'name@beispiel.ch',
                'data-placeholder-it': 'nome@esempio.ch',
                'id': 'id_email',
            }
        ),
    )

    no_of_guests = forms.ChoiceField(
        label='Anzahl der Gäste',
        choices=[(str(i), str(i)) for i in range(1, MAX_GUESTS + 1)],
        widget=forms.Select(attrs={'id': 'id_no_of_guests'}),
    )

    no_of_children = forms.ChoiceField(
        label='Anzahl Kinder',
        choices=[(str(i), str(i)) for i in range(0, MAX_CHILDREN + 1)],
        initial='0',
        required=False,
        widget=forms.Select(attrs={'id': 'id_no_of_children'}),
    )

    message = forms.CharField(
        label='Nachricht',
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'placeholder': 'Möchtet ihr uns noch etwas mitteilen? (optional)',
                'data-placeholder-de': 'Möchtet ihr uns noch etwas mitteilen? (optional)',
                'data-placeholder-it': 'Volete comunicarci qualcosa? (facoltativo)',
                'id': 'id_message',
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ---- Erwachsene Gäste ----
        for i in range(1, MAX_GUESTS + 1):
            self.fields[f'guest_name_{i}'] = forms.CharField(
                label='Name',
                max_length=120,
                required=False,
                widget=forms.TextInput(
                    attrs={
                        'placeholder': 'Vor- und Nachname',
                        'data-placeholder-de': 'Vor- und Nachname',
                        'data-placeholder-it': 'Nome e cognome',
                        'class': 'guest-field',
                    }
                ),
            )
            self.fields[f'guest_meal_{i}'] = forms.ChoiceField(
                label='Menüwahl',
                choices=self.MEAL_CHOICES,
                required=False,
                widget=forms.Select(attrs={
                    'class': 'guest-field',
                    'data-empty-de': self.SELECT_EMPTY_DE,
                    'data-empty-it': self.SELECT_EMPTY_IT,
                }),
            )
            self.fields[f'guest_allergies_{i}'] = forms.CharField(
                label='Allergien / Unverträglichkeiten',
                required=False,
                widget=forms.Textarea(
                    attrs={
                        'rows': 2,
                        'placeholder': 'z.B. Laktose, Gluten, Nüsse ...',
                        'data-placeholder-de': 'z.B. Laktose, Gluten, Nüsse ...',
                        'data-placeholder-it': 'p.es. lattosio, glutine, noci ...',
                        'class': 'guest-field',
                    }
                ),
            )

        # ---- Kinder (Anforderung 1) ----
        for i in range(1, MAX_CHILDREN + 1):
            self.fields[f'child_name_{i}'] = forms.CharField(
                label='Name',
                max_length=120,
                required=False,
                widget=forms.TextInput(
                    attrs={
                        'placeholder': 'Vor- und Nachname',
                        'data-placeholder-de': 'Vor- und Nachname',
                        'data-placeholder-it': 'Nome e cognome',
                        'class': 'child-field',
                    }
                ),
            )
            self.fields[f'child_age_{i}'] = forms.CharField(
                label='Alter',
                max_length=20,
                required=False,
                widget=forms.TextInput(
                    attrs={
                        'placeholder': 'z.B. 5 Jahre',
                        'data-placeholder-de': 'z.B. 5 Jahre',
                        'data-placeholder-it': 'p.es. 5 anni',
                        'class': 'child-field',
                    }
                ),
            )
            self.fields[f'child_meal_{i}'] = forms.ChoiceField(
                label='Menü für Kinder',
                choices=self.CHILD_MEAL_CHOICES,
                required=False,
                widget=forms.Select(attrs={
                    'class': 'child-field',
                    'data-empty-de': self.SELECT_EMPTY_DE,
                    'data-empty-it': self.SELECT_EMPTY_IT,
                }),
            )
            self.fields[f'child_allergies_{i}'] = forms.CharField(
                label='Allergien / Unverträglichkeiten',
                required=False,
                widget=forms.Textarea(
                    attrs={
                        'rows': 2,
                        'placeholder': 'z.B. Laktose, Gluten, Nüsse ...',
                        'data-placeholder-de': 'z.B. Laktose, Gluten, Nüsse ...',
                        'data-placeholder-it': 'p.es. lattosio, glutine, noci ...',
                        'class': 'child-field',
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

    def child_rows(self):
        return [
            {
                'index': i,
                'name': self[f'child_name_{i}'],
                'age': self[f'child_age_{i}'],
                'meal': self[f'child_meal_{i}'],
                'allergies': self[f'child_allergies_{i}'],
            }
            for i in range(1, MAX_CHILDREN + 1)
        ]

    def clean(self):
        cleaned_data = super().clean()

        try:
            no_of_guests = int(cleaned_data.get('no_of_guests') or 0)
        except (TypeError, ValueError):
            no_of_guests = 0

        try:
            no_of_children = int(cleaned_data.get('no_of_children') or 0)
        except (TypeError, ValueError):
            no_of_children = 0
        cleaned_data['no_of_children'] = str(no_of_children)

        # ---- Erwachsene Gäste prüfen ----
        for i in range(1, MAX_GUESTS + 1):
            name_field = f'guest_name_{i}'
            meal_field = f'guest_meal_{i}'
            allergies_field = f'guest_allergies_{i}'

            if i <= no_of_guests:
                if not cleaned_data.get(name_field):
                    self.add_error(name_field, 'Bitte Namen angeben.')
                if not cleaned_data.get(meal_field):
                    self.add_error(meal_field, 'Bitte ein Menü wählen.')
            else:
                cleaned_data[name_field] = ''
                cleaned_data[meal_field] = ''
                cleaned_data[allergies_field] = ''

        # ---- Kinder prüfen ----
        for i in range(1, MAX_CHILDREN + 1):
            name_field = f'child_name_{i}'
            age_field = f'child_age_{i}'
            meal_field = f'child_meal_{i}'
            allergies_field = f'child_allergies_{i}'

            if i <= no_of_children:
                if not cleaned_data.get(name_field):
                    self.add_error(name_field, 'Bitte Namen angeben.')
                if not cleaned_data.get(meal_field):
                    self.add_error(meal_field, 'Bitte ein Menü wählen.')
            else:
                cleaned_data[name_field] = ''
                cleaned_data[age_field] = ''
                cleaned_data[meal_field] = ''
                cleaned_data[allergies_field] = ''

        return cleaned_data
