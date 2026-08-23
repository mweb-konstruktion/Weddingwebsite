from .models import (
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


class TranslatedText:
    """Wrapper, damit Templates {{ texts.key.de }} / {{ texts.key.it }} nutzen können."""

    def __init__(self, de, it):
        self.de = de
        self.it = it


def site_content(request):
    texts = {
        block.key: TranslatedText(block.text_de, block.text_it)
        for block in TextBlock.objects.all()
    }
    images = {
        image.key: image
        for image in SiteImage.objects.all()
    }
    return {
        'texts': texts,
        'images': images,
        'gifts': GiftsSection.objects.first(),
        'location_cards': LocationCard.objects.all(),
        'timeline_steps': TimelineStep.objects.all(),
        'travel_info_cards': TravelInfoCard.objects.all(),
        'hotel_recommendations': HotelRecommendation.objects.all(),
        'faq_items': FAQItem.objects.all(),
        'story_items': StoryItem.objects.all(),
        'contact_persons': ContactPerson.objects.all(),
    }
