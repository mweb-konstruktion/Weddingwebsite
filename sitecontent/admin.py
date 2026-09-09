from adminsortable2.admin import SortableAdminMixin
from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.html import format_html

from .models import (
    ContactPerson,
    FAQItem,
    GiftsSection,
    HotelRecommendation,
    LocationCard,
    RSVPGuest,
    RSVPSubmission,
    SiteImage,
    StoryItem,
    TextBlock,
    TimelineStep,
    TravelInfoCard,
)


class SingletonAdminMixin:
    """Erlaubt nur einen Eintrag; Listenansicht springt direkt zum Bearbeiten."""

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        if obj:
            return redirect('admin:%s_%s_change' % (self.model._meta.app_label, self.model._meta.model_name), obj.pk)
        return super().changelist_view(request, extra_context)


class ThumbnailAdminMixin:
    """Zeigt eine kleine Bildvorschau in der Listenansicht."""

    image_field = 'image'

    def thumbnail(self, obj):
        image = getattr(obj, self.image_field, None)
        if not image:
            return "–"
        return format_html('<img src="{}" style="height:40px;border-radius:4px;" />', image.url)

    thumbnail.short_description = "Vorschau"


@admin.register(TextBlock)
class TextBlockAdmin(admin.ModelAdmin):
    list_display = ('label', 'key', 'group')
    list_filter = ('group',)
    search_fields = ('key', 'label', 'text_de', 'text_it')
    fieldsets = (
        (None, {'fields': ('key', 'label', 'group')}),
        ('Deutsch', {'fields': ('text_de',)}),
        ('Italiano', {'fields': ('text_it',)}),
    )


@admin.register(SiteImage)
class SiteImageAdmin(ThumbnailAdminMixin, admin.ModelAdmin):
    list_display = ('label', 'key', 'thumbnail')
    fieldsets = (
        (None, {'fields': ('key', 'label', 'image')}),
        ('Alt-Text', {'fields': ('alt_de', 'alt_it')}),
    )


@admin.register(GiftsSection)
class GiftsSectionAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('title_de',)
    fieldsets = (
        ('Deutsch', {'fields': ('title_de', 'text_de')}),
        ('Italiano', {'fields': ('title_it', 'text_it')}),
    )


@admin.register(LocationCard)
class LocationCardAdmin(SortableAdminMixin, ThumbnailAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'thumbnail')
    fieldsets = (
        (None, {'fields': ('icon', 'icon_image', 'name', 'address', 'map_embed_url', 'image')}),
        ('Deutsch', {'fields': ('title_de', 'description_de')}),
        ('Italiano', {'fields': ('title_it', 'description_it')}),
    )


@admin.register(TimelineStep)
class TimelineStepAdmin(SortableAdminMixin, ThumbnailAdminMixin, admin.ModelAdmin):
    image_field = 'icon_image'
    list_display = ('time', 'title_de', 'thumbnail')
    fieldsets = (
        (None, {'fields': ('time', 'icon_image')}),
        ('Deutsch', {'fields': ('title_de', 'description_de')}),
        ('Italiano', {'fields': ('title_it', 'description_it')}),
    )


@admin.register(TravelInfoCard)
class TravelInfoCardAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('title_de',)
    fieldsets = (
        (None, {'fields': ('icon', 'icon_image')}),
        ('Deutsch', {'fields': ('title_de', 'body_de')}),
        ('Italiano', {'fields': ('title_it', 'body_it')}),
    )


class HotelRecommendationForm(forms.ModelForm):
    class Meta:
        model = HotelRecommendation
        fields = '__all__'
        widgets = {
            'description_de': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
            'description_it': forms.Textarea(attrs={'rows': 3, 'cols': 60}),
        }


@admin.register(HotelRecommendation)
class HotelRecommendationAdmin(SortableAdminMixin, admin.ModelAdmin):
    form = HotelRecommendationForm
    list_display = ('name', 'url')
    fieldsets = (
        (None, {'fields': ('name', 'url')}),
        ('Deutsch', {'fields': ('description_de',)}),
        ('Italiano', {'fields': ('description_it',)}),
    )


@admin.register(FAQItem)
class FAQItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('question_de',)
    fieldsets = (
        ('Deutsch', {'fields': ('question_de', 'answer_de')}),
        ('Italiano', {'fields': ('question_it', 'answer_it')}),
    )


@admin.register(StoryItem)
class StoryItemAdmin(SortableAdminMixin, ThumbnailAdminMixin, admin.ModelAdmin):
    list_display = ('title_de', 'thumbnail')
    fieldsets = (
        (None, {'fields': ('image',)}),
        ('Deutsch', {'fields': ('date_label_de', 'title_de', 'text_de')}),
        ('Italiano', {'fields': ('date_label_it', 'title_it', 'text_it')}),
    )


@admin.register(ContactPerson)
class ContactPersonAdmin(SortableAdminMixin, ThumbnailAdminMixin, admin.ModelAdmin):
    image_field = 'photo'
    list_display = ('name', 'phone', 'email', 'thumbnail')
    fieldsets = (
        (None, {'fields': ('name', 'phone', 'email', 'photo')}),
        ('Deutsch', {'fields': ('role_de',)}),
        ('Italiano', {'fields': ('role_it',)}),
    )


class RSVPGuestInline(admin.TabularInline):
    model = RSVPGuest
    extra = 0
    can_delete = False
    fields = ('name', 'is_child', 'age', 'meal', 'allergies')
    readonly_fields = ('name', 'is_child', 'age', 'meal', 'allergies')

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(RSVPSubmission)
class RSVPSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'no_of_guests', 'no_of_children', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('name', 'email')
    readonly_fields = ('submitted_at',)
    inlines = [RSVPGuestInline]

    def has_add_permission(self, request):
        return False
