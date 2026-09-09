from django.core.validators import FileExtensionValidator
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class TextBlock(models.Model):
    """Einzelner Textbaustein (Titel, Untertitel, Absatz), zweisprachig DE/IT."""

    key = models.SlugField(max_length=100, unique=True, help_text="Interner Bezeichner, z.B. 'hero_subtitle'.")
    label = models.CharField(max_length=200, help_text="Beschreibung für die Verwaltung, z.B. 'Hero – Untertitel'.")
    group = models.CharField(max_length=100, blank=True, help_text="Abschnitt, z.B. 'Hero', 'Geschenke'.")
    text_de = CKEditor5Field(verbose_name="Text (Deutsch)", config_name='default')
    text_it = CKEditor5Field(verbose_name="Text (Italienisch)", config_name='default')

    class Meta:
        ordering = ['group', 'key']
        verbose_name = "Textbaustein"
        verbose_name_plural = "Textbausteine"

    def __str__(self):
        return self.label


class SiteImage(models.Model):
    """Einzelnes Bild an einer festen Stelle der Website (z.B. Hero-Bild)."""

    key = models.SlugField(max_length=100, unique=True, help_text="Interner Bezeichner, z.B. 'hero'.")
    label = models.CharField(max_length=200)
    image = models.ImageField(upload_to='site/')
    alt_de = models.CharField(max_length=255, blank=True, verbose_name="Alt-Text (Deutsch)")
    alt_it = models.CharField(max_length=255, blank=True, verbose_name="Alt-Text (Italienisch)")

    class Meta:
        ordering = ['key']
        verbose_name = "Bild"
        verbose_name_plural = "Bilder"

    def __str__(self):
        return self.label


class GiftsSection(models.Model):
    """Inhalt der Geschenke-Sektion. Es wird nur ein Eintrag verwendet."""

    title_de = models.CharField(max_length=200, verbose_name="Titel (Deutsch)")
    title_it = models.CharField(max_length=200, verbose_name="Titel (Italienisch)")
    text_de = CKEditor5Field(verbose_name="Text (Deutsch)", config_name='default')
    text_it = CKEditor5Field(verbose_name="Text (Italienisch)", config_name='default')

    class Meta:
        verbose_name = "Geschenke-Inhalt"
        verbose_name_plural = "Geschenke-Inhalt"

    def __str__(self):
        return self.title_de


class LocationCard(models.Model):
    order = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=10, blank=True, help_text="Emoji/Symbol, z.B. ⛪ (Fallback, falls kein Icon-Bild hochgeladen ist)")
    icon_image = models.FileField(
        upload_to='location_icons/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])],
        verbose_name="Icon-Bild (PNG, JPEG oder SVG)",
        help_text="Optional — ersetzt das Emoji-Icon.",
    )
    title_de = models.CharField(max_length=200, verbose_name="Titel (Deutsch)")
    title_it = models.CharField(max_length=200, verbose_name="Titel (Italienisch)")
    name = models.CharField(max_length=200, help_text="Name des Ortes (nicht übersetzt).")
    description_de = CKEditor5Field(
        verbose_name="Beschreibung (Deutsch)", config_name='default', blank=True,
        help_text="Optional. Wird zwischen Titel und Adresse angezeigt.",
    )
    description_it = CKEditor5Field(
        verbose_name="Beschreibung (Italienisch)", config_name='default', blank=True,
        help_text="Optional. Wird zwischen Titel und Adresse angezeigt.",
    )
    address = models.CharField(max_length=255)
    map_embed_url = models.URLField(max_length=1000, blank=True, help_text="Google-Maps 'Embed a map' URL.")
    image = models.ImageField(upload_to='locations/', blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Ort"
        verbose_name_plural = "Orte"

    def __str__(self):
        return self.name


class TimelineStep(models.Model):
    order = models.PositiveIntegerField(default=0)
    time = models.CharField(max_length=20, help_text="z.B. 16:30")
    title_de = models.CharField(max_length=200, verbose_name="Titel (Deutsch)")
    title_it = models.CharField(max_length=200, verbose_name="Titel (Italienisch)")
    description_de = models.CharField(max_length=255, blank=True, verbose_name="Beschreibung (Deutsch)")
    description_it = models.CharField(max_length=255, blank=True, verbose_name="Beschreibung (Italienisch)")
    icon_image = models.FileField(
        upload_to='timeline_icons/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])],
        verbose_name="Icon-Bild (PNG, JPEG oder SVG)",
        help_text="Optional — ohne Upload wird ein Standard-Icon angezeigt.",
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Programmpunkt"
        verbose_name_plural = "Tagesablauf"

    def __str__(self):
        return f"{self.time} – {self.title_de}"


class TravelInfoCard(models.Model):
    order = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=10, blank=True, help_text="Emoji/Symbol, z.B. ✈ (Fallback, falls kein Icon-Bild hochgeladen ist)")
    icon_image = models.FileField(
        upload_to='travel_icons/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'svg'])],
        verbose_name="Icon-Bild (PNG, JPEG oder SVG)",
        help_text="Optional — ersetzt das Emoji-Icon.",
    )
    title_de = models.CharField(max_length=200, verbose_name="Titel (Deutsch)")
    title_it = models.CharField(max_length=200, verbose_name="Titel (Italienisch)")
    body_de = CKEditor5Field(verbose_name="Text (Deutsch)", config_name='default')
    body_it = CKEditor5Field(verbose_name="Text (Italienisch)", config_name='default')

    class Meta:
        ordering = ['order']
        verbose_name = "Reise-Info"
        verbose_name_plural = "Reise-Infos"

    def __str__(self):
        return self.title_de


class HotelRecommendation(models.Model):
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=200)
    description_de = models.CharField(max_length=255, verbose_name="Beschreibung (Deutsch)")
    description_it = models.CharField(max_length=255, verbose_name="Beschreibung (Italienisch)")
    url = models.URLField(blank=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Hotel-Empfehlung"
        verbose_name_plural = "Hotel-Empfehlungen"

    def __str__(self):
        return self.name


class FAQItem(models.Model):
    order = models.PositiveIntegerField(default=0)
    question_de = models.CharField(max_length=255, verbose_name="Frage (Deutsch)")
    question_it = models.CharField(max_length=255, verbose_name="Frage (Italienisch)")
    answer_de = CKEditor5Field(verbose_name="Antwort (Deutsch)", config_name='default')
    answer_it = CKEditor5Field(verbose_name="Antwort (Italienisch)", config_name='default')

    class Meta:
        ordering = ['order']
        verbose_name = "FAQ-Eintrag"
        verbose_name_plural = "FAQ"

    def __str__(self):
        return self.question_de


class StoryItem(models.Model):
    order = models.PositiveIntegerField(default=0)
    title_de = models.CharField(max_length=200, verbose_name="Titel (Deutsch)")
    title_it = models.CharField(max_length=200, verbose_name="Titel (Italienisch)")
    date_label_de = models.CharField(max_length=100, blank=True, verbose_name="Datum (Deutsch)", help_text="z.B. 'Sommer 2020'.")
    date_label_it = models.CharField(max_length=100, blank=True, verbose_name="Datum (Italienisch)", help_text="z.B. 'Estate 2020'.")
    text_de = CKEditor5Field(verbose_name="Text (Deutsch)", config_name='default')
    text_it = CKEditor5Field(verbose_name="Text (Italienisch)", config_name='default')
    image = models.ImageField(upload_to='story/', blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Story-Kapitel"
        verbose_name_plural = "Unsere Geschichte"

    def __str__(self):
        return self.title_de


class ContactPerson(models.Model):
    order = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=200)
    role_de = models.CharField(max_length=200, verbose_name="Rolle (Deutsch)")
    role_it = models.CharField(max_length=200, verbose_name="Rolle (Italienisch)")
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    photo = models.ImageField(upload_to='contacts/', blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Kontaktperson"
        verbose_name_plural = "Kontaktpersonen"

    def __str__(self):
        return self.name


class RSVPSubmission(models.Model):
    """Eine Anmeldung über das RSVP-Formular."""

    name = models.CharField(max_length=120, verbose_name="Anmeldende Person")
    email = models.EmailField(verbose_name="E-Mail")
    no_of_guests = models.PositiveSmallIntegerField(verbose_name="Anzahl Gäste")
    no_of_children = models.PositiveSmallIntegerField(default=0, verbose_name="Anzahl Kinder")
    message = models.TextField(blank=True, verbose_name="Nachricht")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Eingegangen am")

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Anmeldung"
        verbose_name_plural = "Anmeldungen"

    def __str__(self):
        return f"{self.name} ({self.no_of_guests} Gäste, {self.no_of_children} Kinder)"


class RSVPGuest(models.Model):
    """Ein einzelner Gast innerhalb einer Anmeldung.

    Kinder werden im selben Modell abgelegt und über ``is_child`` markiert.
    """

    submission = models.ForeignKey(RSVPSubmission, related_name='guests', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    is_child = models.BooleanField(default=False, verbose_name="Kind")
    age = models.CharField(max_length=20, blank=True, verbose_name="Alter")
    meal = models.CharField(max_length=50, blank=True, verbose_name="Menüwahl")
    allergies = models.CharField(max_length=255, blank=True, verbose_name="Allergien / Unverträglichkeiten")

    class Meta:
        ordering = ['is_child', 'id']
        verbose_name = "Gast"
        verbose_name_plural = "Gäste"

    def __str__(self):
        return f"{self.name} (Kind)" if self.is_child else self.name
