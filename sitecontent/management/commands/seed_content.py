from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from sitecontent.models import (
    ContactPerson,
    FAQItem,
    GiftsSection,
    HotelRecommendation,
    LocationCard,
    SiteImage,
    StoryItem,
    TextBlock,
    TimelineStep,
    TravelInfoCard,
)

IMAGES_DIR = settings.BASE_DIR / 'static' / 'images'

TEXT_BLOCKS = [
    # key, label, group, text_de, text_it
    ('hero_subtitle', 'Hero – Untertitel', 'Hero', 'Wir heiraten', 'Ci sposiamo'),
    ('hero_date', 'Hero – Datum', 'Hero', '15. Juli 2027 · Trani, Italien', '15 Luglio 2027 · Trani, Italia'),
    ('location_title', 'Orte – Titel', 'Orte', 'Orte', 'Luoghi'),
    ('timeline_title', 'Tagesablauf – Titel', 'Tagesablauf', 'Tagesablauf', 'Programma della Giornata'),
    ('timeline_subtitle', 'Tagesablauf – Untertitel', 'Tagesablauf',
     'So stellen wir uns unseren gemeinsamen Tag vor', 'Ecco come immaginiamo la nostra giornata insieme'),
    ('travel_title', 'Anreise – Titel', 'Anreise', 'Anreise & Unterkunft', 'Viaggio & Alloggio'),
    ('travel_hotel_title', 'Anreise – Hotel-Karte Titel', 'Anreise', 'Übernachtung', 'Alloggio'),
    ('travel_hotel_intro', 'Anreise – Hotel-Einleitung', 'Anreise',
     'Hier einige Empfehlungen in der Nähe:', 'Ecco alcuni suggerimenti nelle vicinanze:'),
    ('faq_title', 'FAQ – Titel', 'FAQ', 'Häufige Fragen', 'Domande Frequenti'),
    ('story_title', 'Geschichte – Titel', 'Geschichte', 'Unsere Geschichte', 'La Nostra Storia'),
    ('contact_title', 'Kontakt – Titel', 'Kontakt', 'Kontakt', 'Contatti'),
    ('contact_subtitle', 'Kontakt – Untertitel', 'Kontakt',
     'Bei Fragen wendet euch gerne an unsere Trauzeugen', 'Per domande, rivolgetevi ai nostri testimoni'),
    ('footer_note', 'Footer – Hinweis', 'Footer', 'Gemacht mit Liebe', 'Fatto con amore'),
    ('rsvp_success_message', 'Anmeldung – Erfolgsmeldung', 'Anmeldung',
     '<p><strong>Vielen Dank!</strong> Eure Antwort ist bei uns angekommen.</p>'
     '<p>Wir freuen uns auf euch!</p>',
     '<p><strong>Grazie mille!</strong> La vostra risposta ci è arrivata.</p>'
     '<p>Non vediamo l\'ora di festeggiare con voi!</p>'),
]

GIFTS_SECTION = dict(
    title_de='Geschenke', title_it='Regali',
    text_de='<p>Das grösste Geschenk ist eure Anwesenheit an unserem besonderen Tag.</p>'
            '<p>Wer uns trotzdem eine Freude machen möchte, darf gerne einen Beitrag '
            'in unser <strong>Reisekässeli</strong> legen — damit unterstützt ihr '
            'unsere Hochzeitsreise und schafft mit uns unvergessliche Erinnerungen.</p>'
            '<p>Details dazu findet ihr am Hochzeitstag oder sprecht uns einfach an.</p>',
    text_it='<p>Il regalo più grande è la vostra presenza nel nostro giorno speciale.</p>'
            '<p>Se desiderate comunque farci un regalo, potete contribuire al nostro '
            '<strong>fondo viaggio di nozze</strong> — ci aiuterete a creare '
            'ricordi indimenticabili durante la nostra luna di miele.</p>'
            '<p>Troverete i dettagli il giorno del matrimonio o parlatene direttamente con noi.</p>',
)

# Alte, jetzt durch GiftsSection ersetzte TextBlock-Keys (werden beim Seed entfernt).
OBSOLETE_TEXT_BLOCK_KEYS = ['gifts_title', 'gifts_text_1', 'gifts_text_2', 'gifts_note']

LOCATION_CARDS = [
    dict(
        order=1, icon='⛩', name='Basilica Cattedrale Maria Santissima Assunta',
        title_de='Zeremonie — 16:30 Uhr', title_it='Cerimonia — ore 16:30',
        address='Piazza Duomo, 1, 76125 Trani BT, Italy',
        map_embed_url='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d36072.38596536503!2d16.381452495380987!3d41.282222856511275!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1338040b58cc7ce3%3A0x880f0c96b60233ee!2sKathedrale%20von%20Trani!5e1!3m2!1sde!2sch!4v1774987056075!5m2!1sde!2sch',
        image_file='cathedral-trani.jpg',
    ),
    dict(
        order=2, icon='🍾', name='Villa Carafa',
        title_de='Empfang & Festa', title_it='Ricevimento & Festa',
        address='Contrada Monte Carafa, km 2000, 76123 Andria BT, Italy',
        map_embed_url='https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d36132.15496158362!2d16.07610916672714!3d41.17397709683162!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x13383f3e3027d02d%3A0x82f42f15c3759f21!2sVilla%20Carafa!5e1!3m2!1sde!2sch!4v1774986946491!5m2!1sde!2sch',
        image_file='villa-carafa.jpg',
    ),
]

TIMELINE_STEPS = [
    dict(order=1, time='16:00', title_de='Ankunft der Gäste', title_it='Arrivo degli ospiti',
         description_de='Empfang vor der Kathedrale von Trani', description_it='Accoglienza davanti alla Cattedrale di Trani'),
    dict(order=2, time='16:30', title_de='Trauung', title_it='Cerimonia',
         description_de='Zeremonie in der Basilica Cattedrale', description_it='Cerimonia nella Basilica Cattedrale'),
    dict(order=3, time='17:30', title_de='Aperitivo', title_it='Aperitivo',
         description_de='Drinks und Häppchen im Garten der Villa Carafa', description_it='Drink e stuzzichini nel giardino di Villa Carafa'),
    dict(order=4, time='19:30', title_de='Abendessen', title_it='Cena',
         description_de='Mehrgängiges Dinner unter den Sternen', description_it='Cena a più portate sotto le stelle'),
    dict(order=5, time='22:00', title_de='Tortenanschnitt & Erster Tanz', title_it='Taglio della torta & Primo ballo',
         description_de='', description_it=''),
    dict(order=6, time='23:00', title_de='Party & Tanz', title_it='Festa & Ballo',
         description_de='Feiert mit uns bis in die Nacht!', description_it='Festeggiate con noi fino a tarda notte!'),
]

TRAVEL_INFO_CARDS = [
    dict(
        order=1, icon='✈', title_de='Flüge', title_it='Voli',
        body_de='<p>Ab <strong>Basel (BSL)</strong> fliegt <strong>EasyJet</strong> direkt nach '
                '<strong>Bari (BRI)</strong> und <strong>Brindisi (BDS)</strong>. '
                'Von dort sind es ca. 1–1.5 Stunden mit dem Auto nach Trani.</p>'
                '<p>Wir empfehlen, Flüge frühzeitig zu buchen — die Sommerflüge sind beliebt!</p>',
        body_it='<p>Da <strong>Basilea (BSL)</strong>, <strong>EasyJet</strong> vola direttamente a '
                '<strong>Bari (BRI)</strong> e <strong>Brindisi (BDS)</strong>. '
                'Da lì, Trani dista circa 1–1,5 ore in auto.</p>'
                '<p>Vi consigliamo di prenotare i voli in anticipo — i voli estivi sono molto richiesti!</p>',
    ),
]

HOTEL_RECOMMENDATIONS = [
    dict(order=1, name='Hotel Mare Resort', url='#',
         description_de='Direkt am Meer, 5 Minuten zur Kathedrale',
         description_it='Direttamente sul mare, 5 minuti dalla Cattedrale'),
    dict(order=2, name='Palazzo Filisio', url='#',
         description_de='Boutique-Hotel in der Altstadt von Trani',
         description_it='Boutique hotel nel centro storico di Trani'),
    dict(order=3, name='B&B San Nicola', url='#',
         description_de='Gemütliche Unterkunft, preiswert',
         description_it='Alloggio accogliente ed economico'),
]

FAQ_ITEMS = [
    dict(order=1, question_de='Gibt es einen Dresscode?', question_it="C'è un dress code?",
         answer_de='Wir freuen uns über elegante Sommerkleidung. Denkt an die italienische Hitze '
                    '— leichte Stoffe und bequeme Schuhe sind empfohlen. Bitte vermeidet Weiss '
                    'und Cremefarben (das ist der Braut vorbehalten!).',
         answer_it='Vi invitiamo a indossare un abbigliamento elegante estivo. Ricordate il caldo '
                    'italiano — tessuti leggeri e scarpe comode sono consigliati. Per favore evitate '
                    'il bianco e il panna (riservati alla sposa!).'),
    dict(order=2, question_de='Wo kann ich parkieren?', question_it='Dove posso parcheggiare?',
         answer_de='Bei der Kathedrale gibt es öffentliche Parkplätze in der Nähe. '
                    'Zur Villa Carafa steht ein privater Parkplatz zur Verfügung.',
         answer_it='Vicino alla Cattedrale ci sono parcheggi pubblici nelle vicinanze. '
                    'A Villa Carafa è disponibile un parcheggio privato.'),
    dict(order=3, question_de='Kann ich eine Begleitperson mitbringen?', question_it='Posso portare un accompagnatore?',
         answer_de='Auf eurer Einladung ist vermerkt, ob ein «Plus One» eingeladen ist. '
                    'Bei Fragen sprecht uns bitte direkt an.',
         answer_it='Sul vostro invito è indicato se è previsto un «Plus One». '
                    'Per domande, non esitate a contattarci direttamente.'),
    dict(order=4, question_de='Sind Kinder willkommen?', question_it='I bambini sono benvenuti?',
         answer_de='Selbstverständlich! Kinder sind herzlich willkommen. Bitte gebt uns '
                    'im RSVP-Formular Bescheid, damit wir planen können.',
         answer_it='Certamente! I bambini sono i benvenuti. Vi preghiamo di comunicarcelo '
                    'nel modulo RSVP, in modo da poter organizzare al meglio.'),
    dict(order=5, question_de='Was passiert bei schlechtem Wetter?', question_it='Cosa succede in caso di maltempo?',
         answer_de='Die Villa Carafa verfügt über überdachte Bereiche — die Feier findet '
                    'bei jedem Wetter statt. Im Juli ist Regen in Apulien aber sehr selten!',
         answer_it='Villa Carafa dispone di aree coperte — la festa si svolgerà con qualsiasi '
                    'tempo. A luglio la pioggia in Puglia è comunque molto rara!'),
    dict(order=6, question_de='Bis wann muss ich Zusage/Absage geben?', question_it='Entro quando devo confermare?',
         answer_de='Bitte meldet euch bis spätestens <strong>15. Mai 2027</strong> über unser '
                    '<a href="#rsvp">RSVP-Formular</a> an.',
         answer_it='Vi preghiamo di rispondere entro il <strong>15 maggio 2027</strong> tramite il nostro '
                    '<a href="#rsvp">modulo RSVP</a>.'),
]

STORY_ITEMS = [
    dict(order=1, title_de='Wie alles begann', title_it='Come tutto è iniziato', date_label_de='', date_label_it='',
         text_de='Hier könnt ihr unser erstes gemeinsames Foto sehen. '
                  'Was war der erste Eindruck? Wo habt ihr euch getroffen?',
         text_it='Qui potete raccontare come vi siete conosciuti. '
                  'Qual è stata la prima impressione? Dove vi siete incontrati?',
         image_file='story-1.svg'),
    dict(order=2, title_de='Das erste Date', title_it='Il primo appuntamento', date_label_de='', date_label_it='',
         text_de='Beschreibt euer erstes Date — wohin seid ihr gegangen? '
                  'Was habt ihr gemacht? Was hat euch am anderen beeindruckt?',
         text_it='Descrivete il vostro primo appuntamento — dove siete andati? '
                  "Cosa avete fatto? Cosa vi ha colpito dell'altro?",
         image_file='story-2.svg'),
    dict(order=3, title_de='Der Antrag', title_it='La Proposta', date_label_de='', date_label_it='',
         text_de='Erzählt die Geschichte eures Antrags. Wo ist es passiert? Wie hat er/sie reagiert?',
         text_it='Raccontate la storia della proposta. Dove è successo? Come ha reagito?',
         image_file='proposal.png'),
]

CONTACT_PERSONS = [
    dict(order=1, name='Severin', role_de='Trauzeuge', role_it='Testimone dello Sposo',
         phone='+41 79 925 01 44', email='severin@beispiel.ch', photo_file='trauzeuge-severin.svg'),
    dict(order=2, name='Daniel', role_de='Trauzeuge', role_it='Testimone dello Sposo',
         phone='+41 79 370 63 58', email='daniel@beispiel.ch', photo_file='trauzeuge-daniel.svg'),
    dict(order=3, name='Cinzia', role_de='Trauzeugin', role_it='Testimone della Sposa',
         phone='+41 78 871 78 82', email='cinzia@beispiel.ch', photo_file='trauzeugin-cinzia.svg'),
    dict(order=4, name='Anouk', role_de='Trauzeugin', role_it='Testimone della Sposa',
         phone='+41 76 211 27 81', email='anouk@beispiel.ch', photo_file='trauzeugin-anouk.svg'),
]

SITE_IMAGES = [
    dict(key='hero', label='Hero-Bild', file='hero.jpg',
         alt_de='Villa Carafa in Apulien', alt_it='Villa Carafa in Puglia'),
]


def attach_image(instance, field_name, filename):
    path = IMAGES_DIR / filename
    if not path.exists():
        return
    with open(path, 'rb') as f:
        getattr(instance, field_name).save(filename, File(f), save=True)


class Command(BaseCommand):
    help = (
        "Befuellt die Content-Modelle mit Startdaten (fuer eine leere Datenbank). "
        "Bereits vorhandene Eintraege werden NICHT ueberschrieben. Muss explizit "
        "bestaetigt werden (--yes) oder interaktiv beantwortet werden — laeuft nie "
        "automatisch oder als Nebeneffekt eines anderen Befehls."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--yes',
            action='store_true',
            help="Bestaetigung ueberspringen (fuer nicht-interaktive Ausfuehrung, z.B. Skripte).",
        )

    def handle(self, *args, **options):
        if not options['yes']:
            confirm = input(
                "Dies legt fehlende Start-Inhalte an (bestehende Eintraege bleiben unangetastet).\n"
                "Nur ausfuehren, wenn du das wirklich willst. Fortfahren? [y/N]: "
            )
            if confirm.strip().lower() not in ('y', 'yes', 'j', 'ja'):
                self.stdout.write(self.style.WARNING("Abgebrochen — es wurde nichts veraendert."))
                return

        created_count = 0
        for key, label, group, text_de, text_it in TEXT_BLOCKS:
            _, created = TextBlock.objects.get_or_create(
                key=key, defaults=dict(label=label, group=group, text_de=text_de, text_it=text_it),
            )
            created_count += created
        self.stdout.write(self.style.SUCCESS(f'{created_count} von {len(TEXT_BLOCKS)} Textbausteinen neu angelegt.'))

        removed, _ = TextBlock.objects.filter(key__in=OBSOLETE_TEXT_BLOCK_KEYS).delete()
        if removed:
            self.stdout.write(self.style.SUCCESS(f'{removed} veraltete Textbausteine entfernt.'))

        if not GiftsSection.objects.exists():
            GiftsSection.objects.create(**GIFTS_SECTION)
            self.stdout.write(self.style.SUCCESS('Geschenke-Inhalt angelegt.'))
        else:
            self.stdout.write('Geschenke-Inhalt existiert bereits, übersprungen.')

        img_created = 0
        for data in SITE_IMAGES:
            image, created = SiteImage.objects.get_or_create(
                key=data['key'],
                defaults=dict(label=data['label'], alt_de=data['alt_de'], alt_it=data['alt_it']),
            )
            img_created += created
            if not image.image:
                attach_image(image, 'image', data['file'])
        self.stdout.write(self.style.SUCCESS(f'{img_created} von {len(SITE_IMAGES)} Bildern neu angelegt.'))

        loc_created = 0
        for data in LOCATION_CARDS:
            image_file = data.pop('image_file')
            obj, created = LocationCard.objects.get_or_create(order=data['order'], defaults=data)
            loc_created += created
            if not obj.image:
                attach_image(obj, 'image', image_file)
        self.stdout.write(self.style.SUCCESS(f'{loc_created} von {len(LOCATION_CARDS)} Orten neu angelegt.'))

        step_created = 0
        for data in TIMELINE_STEPS:
            _, created = TimelineStep.objects.get_or_create(order=data['order'], defaults=data)
            step_created += created
        self.stdout.write(self.style.SUCCESS(f'{step_created} von {len(TIMELINE_STEPS)} Tagesablauf-Punkten neu angelegt.'))

        travel_created = 0
        for data in TRAVEL_INFO_CARDS:
            _, created = TravelInfoCard.objects.get_or_create(order=data['order'], defaults=data)
            travel_created += created
        self.stdout.write(self.style.SUCCESS(f'{travel_created} von {len(TRAVEL_INFO_CARDS)} Reise-Infos neu angelegt.'))

        hotel_created = 0
        for data in HOTEL_RECOMMENDATIONS:
            _, created = HotelRecommendation.objects.get_or_create(order=data['order'], defaults=data)
            hotel_created += created
        self.stdout.write(self.style.SUCCESS(f'{hotel_created} von {len(HOTEL_RECOMMENDATIONS)} Hotel-Empfehlungen neu angelegt.'))

        faq_created = 0
        for data in FAQ_ITEMS:
            _, created = FAQItem.objects.get_or_create(order=data['order'], defaults=data)
            faq_created += created
        self.stdout.write(self.style.SUCCESS(f'{faq_created} von {len(FAQ_ITEMS)} FAQ-Eintraegen neu angelegt.'))

        story_created = 0
        for data in STORY_ITEMS:
            image_file = data.pop('image_file')
            obj, created = StoryItem.objects.get_or_create(order=data['order'], defaults=data)
            story_created += created
            if not obj.image:
                attach_image(obj, 'image', image_file)
        self.stdout.write(self.style.SUCCESS(f'{story_created} von {len(STORY_ITEMS)} Story-Kapiteln neu angelegt.'))

        contact_created = 0
        for data in CONTACT_PERSONS:
            photo_file = data.pop('photo_file')
            obj, created = ContactPerson.objects.get_or_create(order=data['order'], defaults=data)
            contact_created += created
            if not obj.photo:
                attach_image(obj, 'photo', photo_file)
        self.stdout.write(self.style.SUCCESS(f'{contact_created} von {len(CONTACT_PERSONS)} Kontaktpersonen neu angelegt.'))

        self.stdout.write(self.style.SUCCESS('Seed abgeschlossen.'))
