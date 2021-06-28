from django.db import models
from django.db.models.deletion import SET_NULL
from django.core.exceptions import ValidationError
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, PageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel


# Create your models here.
class ServiceListingPage(Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["services.ServicePage"]
    template = "services/service_listing_page.html"
    max_count = 1
    subtitle = models.TextField(
        blank=True,
        max_length=500,
    )
    
    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['services'] = ServicePage.objects.live().public()
        
        return context 
        
class ServicePage(Page):
    parent_page_types = ["services.ServiceListingPage"]
    template = "services/service_page.html"

    description=models.TextField(
        blank=True,
        max_length=500,
    )
    internal_page=models.ForeignKey(
        'wagtailcore.Page',
        blank=True,
        null=True,
        related_name='+',
        help_text="Select an internal Page",
        on_delete=models.SET_NULL,
    )
    external_page=models.URLField(blank=True)
    button_text = models.CharField(blank=True,max_length=50)
    service_image= models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        help_text= "Image will be used on Service Listing Page",
        related_name='+',
    )

    content_panels = Page.content_panels + [
        PageChooserPanel("internal_page"),
        FieldPanel("description"),
        FieldPanel("external_page"),
        FieldPanel("button_text"),
        ImageChooserPanel("service_image"),
    ]

    def clean(self):
        super().clean()

        if self.internal_page and self.external_page:
            raise ValidationError({
                'internal_page': ValidationError("Please only select a page or enter an external url"),
                'external_page': ValidationError('Please enter only a page or enter an external url'),
            })

        if not self.internal_page and not self.external_page:
            raise ValidationError({
                'internal_page': ValidationError("Please enter a valid internal page or enter a valid external url"),
                'external_page': ValidationError("Please enter a valid internal page or enter a valid external url")
            })
