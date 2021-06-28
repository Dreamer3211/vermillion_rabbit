from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.admin.edit_handlers import FieldPanel, RichTextFieldPanel, PageChooserPanel
from wagtail.core.fields import RichTextField


@register_setting
class HoursSettings(BaseSetting):

    hours = RichTextField(
        blank = True,
        features = [],
        null = True
    )

    panels = [
        FieldPanel("hours")
    ]

    def save(self, *args, **kwargs):
        key = make_template_fragment_key("footer_hours_settings")
        cache.delete(key)
        return super().save(*args, **kwargs)


@register_setting
class ContactSettings(BaseSetting):

    contact = RichTextField(
        blank = True,
        features = ["link"],
        null = True
    )

    panels = [
        FieldPanel("contact")
    ]

    def save(self, *args, **kwargs):
        key = make_template_fragment_key("footer_contact_settings")
        cache.delete(key)
        return super().save(*args, **kwargs)

@register_setting
class SocialMediaSettings(BaseSetting):

    linkedin = models.URLField(
        blank= True,
        help_text = "Enter your social links") 
    discord = models.URLField(
        blank= True,
        help_text = "Enter your social links") 
    github = models.URLField( 
        blank= True,
        help_text = "Enter your social links")

    panels = [
        FieldPanel("linkedin"),
        FieldPanel("discord"),
        FieldPanel("github"),
    ] 

    def save(self, *args, **kwargs):
        key = make_template_fragment_key("footer_social_settings")
        cache.delete(key)
        return super().save(*args, **kwargs)

@register_setting
class FooterCTASettings(BaseSetting):

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=250)
    button_text = models.CharField(max_length=25, default='Contact Us')
    button_internal_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='If an internal page is selected, it will be used before the external page.'
    )
    button_external_page = models.URLField(blank=True, help_text='If an internal page is selected, it will be used before the external page.')

    panels = [
        FieldPanel("title"),
        FieldPanel("subtitle"),
        FieldPanel("button_text"),
        PageChooserPanel("button_internal_page"),
        FieldPanel("button_external_page"),
    ]

    def save(self, *args, **kwargs):
        key = make_template_fragment_key("footer_cta_settings")
        cache.delete(key)
        return super().save(*args, **kwargs)
